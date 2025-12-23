"""
XML parser for Bundestag plenary session protocols (BT-Plenarprotokolle).

The DIP API delivers a plain-text extraction via `plenarprotokoll-text`.
For BT plenary protocols (WP >= 18), the metadata may also contain
`fundstelle.xml_url` pointing to the structured XML version hosted on dserver.

This parser consumes that XML and extracts a first, stable structure:
- session metadata (wahlperiode, sitzungsnummer, datum, times, location)
- agenda items (sitzungsbeginn + tagesordnungspunkt blocks)
- speeches (rede blocks with speaker info, paragraphs, and comments)
"""

from __future__ import annotations

from io import BytesIO
import re
from typing import Any, Dict, List, Optional, Tuple, Union
import xml.etree.ElementTree as ET

from .base_parser import BaseParser


def _norm(text: str) -> str:
    return " ".join(text.split())


def _all_text(el: ET.Element) -> str:
    return _norm("".join(el.itertext()))


def _extract_int(text: Optional[str]) -> Optional[int]:
    if not text:
        return None
    m = re.search(r"(\d+)", text)
    return int(m.group(1)) if m else None


def _classify_stage_direction(text: str) -> str:
    t = text.lower()
    if "beifall" in t:
        return "applause"
    if "zwischenruf" in t or "zuruf" in t:
        return "heckle"
    if "lachen" in t:
        return "laughter"
    if "unruhe" in t or "ruhe" in t or "ordnung" in t:
        return "procedural"
    return "other"


class ProtocolXmlParser(BaseParser):
    """
    Parse BT plenary protocol XML (`dbtplenarprotokoll`) into a structured dict.

    Notes:
    - The official XML includes a DOCTYPE + external DTD reference.
      Python's stdlib ElementTree parses this without fetching the DTD.
    - Output is designed to be JSON-serializable and stable for downstream use.
    """

    def parse(self, data: Union[str, bytes]) -> Dict[str, Any]:
        if not data:
            return {}

        xml_bytes = data.encode("utf-8") if isinstance(data, str) else data

        # Streaming parse for large protocols; clear processed subtrees.
        session_info: Dict[str, Any] = {}
        agenda: List[Dict[str, Any]] = []
        speeches: List[Dict[str, Any]] = []
        xref_by_rid: Dict[str, Dict[str, Any]] = {}

        in_sitzungsverlauf = False
        for event, elem in ET.iterparse(
            BytesIO(xml_bytes), events=("start", "end")
        ):
            if event == "start" and elem.tag == "dbtplenarprotokoll" and not session_info:
                session_info = {
                    "wahlperiode": elem.attrib.get("wahlperiode"),
                    "sitzungsnummer": elem.attrib.get("sitzung-nr"),
                    "sitzungsdatum": elem.attrib.get("sitzung-datum"),
                    "startzeit": elem.attrib.get("sitzung-start-uhrzeit"),
                    "endzeit": elem.attrib.get("sitzung-ende-uhrzeit"),
                    "ort": elem.attrib.get("sitzung-ort"),
                    "herausgeber": elem.attrib.get("herausgeber"),
                }
            elif event == "start" and elem.tag == "sitzungsverlauf":
                in_sitzungsverlauf = True

            if event != "end":
                continue

            if elem.tag == "xref":
                rid = elem.attrib.get("rid")
                if rid and elem.attrib.get("ref-type") == "rede":
                    xref_by_rid[rid] = self._parse_xref(elem)
                elem.clear()
                continue

            if not in_sitzungsverlauf:
                continue

            if elem.tag == "sitzungsbeginn":
                agenda.append(self._parse_sitzungsbeginn(elem))
                elem.clear()
            elif elem.tag == "tagesordnungspunkt":
                item, item_speeches = self._parse_tagesordnungspunkt(elem, xref_by_rid)
                agenda.append(item)
                speeches.extend(item_speeches)
                elem.clear()
            elif elem.tag == "sitzungsverlauf":
                in_sitzungsverlauf = False
                elem.clear()

        return {
            "parsed": {
                "session_info": session_info,
                "agenda": agenda,
                "speeches": speeches,
                "references": {"xref_by_rid": xref_by_rid},
            }
        }

    def _parse_xref(self, el: ET.Element) -> Dict[str, Any]:
        # <xref div="C" pnr="22848" ref-type="rede" rid="ID..."><a href="S22848"...>...</a></xref>
        a = el.find("a")
        seite = None
        seitenbereich = None
        if a is not None:
            seite_el = a.find("seite")
            sb_el = a.find("seitenbereich")
            seite = _all_text(seite_el) if seite_el is not None else None
            seitenbereich = _all_text(sb_el) if sb_el is not None else None

        return {
            "rid": el.attrib.get("rid"),
            "pnr": el.attrib.get("pnr"),
            "div": el.attrib.get("div"),
            "href": a.attrib.get("href") if a is not None else None,
            "seite": seite,
            "seitenbereich": seitenbereich,
        }

    def _parse_sitzungsbeginn(self, el: ET.Element) -> Dict[str, Any]:
        name_el = el.find("name")
        chair = _all_text(name_el) if name_el is not None else None

        paragraphs = []
        stage_directions = []
        for node in list(el):
            if node.tag == "p":
                paragraphs.append(
                    {"klasse": node.attrib.get("klasse"), "text": _all_text(node)}
                )
            elif node.tag == "kommentar":
                txt = _all_text(node)
                stage_directions.append({"type": _classify_stage_direction(txt), "text": txt})

        return {
            "type": "sitzungsbeginn",
            "chair": chair,
            "startzeit": el.attrib.get("sitzung-start-uhrzeit"),
            "paragraphs": paragraphs,
            "stage_directions": stage_directions,
        }

    def _parse_tagesordnungspunkt(
        self, el: ET.Element, xref_by_rid: Dict[str, Dict[str, Any]]
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        top_id = el.attrib.get("top-id")
        top_number = _extract_int(top_id)

        # Titles are usually in direct-child <p klasse="T_fett"> (may occur multiple times)
        titles = [
            _all_text(p)
            for p in list(el)
            if p.attrib.get("klasse") in {"T_fett", "T_NaS"}
        ]
        title = " / ".join([t for t in titles if t]) if titles else None

        intro_paragraphs = []
        for node in list(el):
            if node.tag != "p":
                continue
            if node.attrib.get("klasse") in {"J", "J_1"}:
                intro_paragraphs.append({"klasse": node.attrib.get("klasse"), "text": _all_text(node)})

        speech_ids: List[str] = []
        speeches: List[Dict[str, Any]] = []
        for node in list(el):
            if node.tag != "rede":
                continue
            speech = self._parse_rede(node, top_id=top_id, top_title=title, xref_by_rid=xref_by_rid)
            speeches.append(speech)
            if speech.get("id"):
                speech_ids.append(speech["id"])

        return (
            {
                "type": "tagesordnungspunkt",
                "top_id": top_id,
                "top_number": top_number,
                "title": title,
                "intro_paragraphs": intro_paragraphs,
                "speech_ids": speech_ids,
            },
            speeches,
        )

    def _parse_rede(
        self,
        el: ET.Element,
        *,
        top_id: Optional[str],
        top_title: Optional[str],
        xref_by_rid: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        rede_id = el.attrib.get("id")

        speaker = self._extract_speaker(el)
        paragraphs: List[Dict[str, Any]] = []
        stage_directions: List[Dict[str, Any]] = []

        for node in list(el):
            if node.tag == "p":
                # Skip the redner line; we already parse it as speaker meta
                if node.attrib.get("klasse") == "redner":
                    continue
                paragraphs.append(
                    {"klasse": node.attrib.get("klasse"), "text": _all_text(node)}
                )
            elif node.tag == "kommentar":
                txt = _all_text(node)
                stage_directions.append({"type": _classify_stage_direction(txt), "text": txt})

        full_text = "\n\n".join([p["text"] for p in paragraphs if p.get("text")])

        return {
            "id": rede_id,
            "top_id": top_id,
            "top_title": top_title,
            "reference": xref_by_rid.get(rede_id) if rede_id else None,
            "speaker": speaker,
            "paragraphs": paragraphs,
            "stage_directions": stage_directions,
            "text": full_text,
        }

    def _extract_speaker(self, rede_el: ET.Element) -> Optional[Dict[str, Any]]:
        """
        Extract speaker info from the first <p klasse="redner"> in a <rede>.
        """
        redner_p = None
        for p in rede_el.findall("p"):
            if p.attrib.get("klasse") == "redner":
                redner_p = p
                break

        if redner_p is None:
            return None

        redner_el = redner_p.find("redner")
        if redner_el is None:
            return None

        name_el = redner_el.find("name")
        if name_el is None:
            return {"id": redner_el.attrib.get("id")}

        rolle_lang = None
        rolle_kurz = None
        rolle_el = name_el.find("rolle")
        if rolle_el is not None:
            rl = rolle_el.find("rolle_lang")
            rk = rolle_el.find("rolle_kurz")
            rolle_lang = _all_text(rl) if rl is not None else None
            rolle_kurz = _all_text(rk) if rk is not None else None

        return {
            "id": redner_el.attrib.get("id"),
            "titel": _all_text(name_el.find("titel")) if name_el.find("titel") is not None else None,
            "vorname": _all_text(name_el.find("vorname")) if name_el.find("vorname") is not None else None,
            "nachname": _all_text(name_el.find("nachname")) if name_el.find("nachname") is not None else None,
            "fraktion": _all_text(name_el.find("fraktion")) if name_el.find("fraktion") is not None else None,
            "ortszusatz": _all_text(name_el.find("ortszusatz")) if name_el.find("ortszusatz") is not None else None,
            "rolle_lang": rolle_lang,
            "rolle_kurz": rolle_kurz,
        }

