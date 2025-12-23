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

from typing import Any, Dict, List, Optional, Union
import xml.etree.ElementTree as ET

from .base_parser import BaseParser


def _norm(text: str) -> str:
    return " ".join(text.split())


def _all_text(el: ET.Element) -> str:
    return _norm("".join(el.itertext()))


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
        root = ET.fromstring(xml_bytes)

        session_info = {
            "wahlperiode": root.attrib.get("wahlperiode"),
            "sitzungsnummer": root.attrib.get("sitzung-nr"),
            "sitzungsdatum": root.attrib.get("sitzung-datum"),
            "startzeit": root.attrib.get("sitzung-start-uhrzeit"),
            "endzeit": root.attrib.get("sitzung-ende-uhrzeit"),
            "ort": root.attrib.get("sitzung-ort"),
            "herausgeber": root.attrib.get("herausgeber"),
        }

        agenda: List[Dict[str, Any]] = []
        speeches: List[Dict[str, Any]] = []

        sitzungsverlauf = root.find("sitzungsverlauf")
        if sitzungsverlauf is not None:
            for child in list(sitzungsverlauf):
                if child.tag == "sitzungsbeginn":
                    agenda.append(self._parse_sitzungsbeginn(child))
                elif child.tag == "tagesordnungspunkt":
                    agenda.append(self._parse_tagesordnungspunkt(child, speeches))

        return {
            "parsed": {
                "session_info": session_info,
                "agenda": agenda,
                "speeches": speeches,
            }
        }

    def _parse_sitzungsbeginn(self, el: ET.Element) -> Dict[str, Any]:
        name_el = el.find("name")
        chair = _all_text(name_el) if name_el is not None else None

        paragraphs = []
        comments = []
        for node in list(el):
            if node.tag == "p":
                paragraphs.append(
                    {"klasse": node.attrib.get("klasse"), "text": _all_text(node)}
                )
            elif node.tag == "kommentar":
                comments.append({"text": _all_text(node)})

        return {
            "type": "sitzungsbeginn",
            "chair": chair,
            "startzeit": el.attrib.get("sitzung-start-uhrzeit"),
            "paragraphs": paragraphs,
            "comments": comments,
        }

    def _parse_tagesordnungspunkt(
        self, el: ET.Element, speeches_out: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        top_id = el.attrib.get("top-id")

        # Titles are usually in <p klasse="T_fett"> (may occur multiple times)
        titles = [
            _all_text(p)
            for p in el.findall("p")
            if p.attrib.get("klasse") in {"T_fett", "T_NaS"}
        ]
        title = " / ".join([t for t in titles if t]) if titles else None

        speech_ids: List[str] = []
        for rede in el.findall("rede"):
            speech = self._parse_rede(rede)
            speeches_out.append(speech)
            if speech.get("id"):
                speech_ids.append(speech["id"])

        return {
            "type": "tagesordnungspunkt",
            "top_id": top_id,
            "title": title,
            "speech_ids": speech_ids,
        }

    def _parse_rede(self, el: ET.Element) -> Dict[str, Any]:
        rede_id = el.attrib.get("id")

        speaker = self._extract_speaker(el)
        paragraphs: List[Dict[str, Any]] = []
        comments: List[Dict[str, Any]] = []

        for node in list(el):
            if node.tag == "p":
                # Skip the redner line; we already parse it as speaker meta
                if node.attrib.get("klasse") == "redner":
                    continue
                paragraphs.append(
                    {"klasse": node.attrib.get("klasse"), "text": _all_text(node)}
                )
            elif node.tag == "kommentar":
                comments.append({"text": _all_text(node)})

        return {
            "id": rede_id,
            "speaker": speaker,
            "paragraphs": paragraphs,
            "comments": comments,
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

