from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Vorgangsbezug(BaseModel):
    """
    Represents a reference to a legislative process.
    """

    id: str = Field(
        ...,
        json_schema_extra={
            "example": "84393",
            "description": "ID eines verknüpften Vorgangs",
        },
    )
    titel: str = Field(
        ...,
        json_schema_extra={
            "example": "Eröffnung der 1. Sitzung des 19. Deutschen Bundestages",
            "description": "Title of the process",
        },
    )
    vorgangstyp: str = Field(
        ...,
        json_schema_extra={
            "example": "Ansprache/Erklärung/Mitteilung",
            "description": "Type of the process",
        },
    )


class Vorgangspositionbezug(Vorgangsbezug):
    """
    Represents a specific position within a legislative process.
    """

    vorgangsposition: str = Field(
        ...,
        json_schema_extra={
            "example": "Ansprache",
            "description": "Position within the process",
        },
    )


class VorgangVerlinkung(BaseModel):
    """
    Represents a link to a legislative process.
    """

    id: str = Field(
        ...,
        json_schema_extra={
            "example": "282237",
            "description": "ID eines verknüpften Vorgangs",
        },
    )
    verweisung: str = Field(
        ..., json_schema_extra={"example": "Bericht", "description": "Reference type"}
    )
    titel: str = Field(
        ...,
        json_schema_extra={
            "example": "Zwischenbericht zur Reform des Bundeswahlrechts und zur Modernisierung der Parlamentsarbeit",
            "description": "Title of the reference",
        },
    )
    wahlperiode: int = Field(
        ..., json_schema_extra={"example": 19, "description": "Legislative period"}
    )
    gesta: Optional[str] = Field(
        None, json_schema_extra={"description": "GESTA code if available"}
    )


class Bundesland(str, Enum):
    """
    Enumeration of German federal states.
    """

    BADEN_WUERTTEMBERG = "Baden-Württemberg"
    BAYERN = "Bayern"
    BERLIN = "Berlin"
    BRANDENBURG = "Brandenburg"
    BREMEN = "Bremen"
    HAMBURG = "Hamburg"
    HESSEN = "Hessen"
    MECKLENBURG_VORPOMMERN = "Mecklenburg-Vorpommern"
    NIEDERSACHSEN = "Niedersachsen"
    NORDRHEIN_WESTFALEN = "Nordrhein-Westfalen"
    RHEINLAND_PFALZ = "Rheinland-Pfalz"
    SAARLAND = "Saarland"
    SACHSEN = "Sachsen"
    SACHSEN_ANHALT = "Sachsen-Anhalt"
    SCHLESWIG_HOLSTEIN = "Schleswig-Holstein"
    THUERINGEN = "Thüringen"


class Datum(BaseModel):
    """
    Represents a date.
    """

    datum: date = Field(
        ..., json_schema_extra={"description": "The date in YYYY-MM-DD format"}
    )


class Quadrant(str, Enum):
    """
    Enumeration of quadrants.
    """

    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Zuordnung(str, Enum):
    """
    Enumeration of assignments.
    """

    BT = "BT"
    BR = "BR"
    BV = "BV"
    EK = "EK"


# New domain models
class Person(BaseModel):
    """
    Typed representation of a person (parliament member).
    """

    id: Optional[str] = Field(None, description="DIP person ID")
    name: Optional[str] = Field(None, description="Full name")
    vorname: Optional[str] = Field(None, description="First name")
    nachname: Optional[str] = Field(None, description="Last name")
    titel: Optional[str] = Field(None, description="Title e.g. Dr.")
    fraktion: Optional[str] = Field(None, description="Parliamentary group")
    partei: Optional[str] = Field(None, description="Party")
    wahlkreis: Optional[str] = Field(None, description="Constituency")
    email: Optional[str] = Field(None, description="Email address")


class Document(BaseModel):
    """
    Typed representation of a document (Drucksache).
    """

    id: Optional[str] = Field(None, description="DIP document ID")
    titel: Optional[str] = Field(None, description="Title")
    dokumentart: Optional[str] = Field(None, description="Document type raw")
    datum: Optional[date] = Field(None, description="Publication date")
    text: Optional[str] = Field(None, description="Extract or full text if available")


class Activity(BaseModel):
    """
    Typed representation of an activity (Aktivität / Plenarereignis).
    """

    id: Optional[str] = Field(None, description="DIP activity ID")
    titel: Optional[str] = Field(None, description="Activity title")
    sitzungsnummer: Optional[str] = Field(None, description="Session number")
    wahlperiode: Optional[int] = Field(None, description="Legislative period")
    sitzungsdatum: Optional[date] = Field(None, description="Session date")
    beschreibung: Optional[str] = Field(None, description="Description")


class Protocol(BaseModel):
    """
    Typed representation of a plenary protocol (Plenarprotokoll).
    """

    id: Optional[str] = Field(None, description="DIP protocol ID")
    sitzungsnummer: Optional[str] = Field(None, description="Session number")
    wahlperiode: Optional[int] = Field(None, description="Legislative period")
    sitzungsdatum: Optional[date] = Field(None, description="Session date")
    text: Optional[str] = Field(None, description="Protocol text")


class StageDirectionType(str, Enum):
    """
    High-level classification for non-spoken protocol annotations.
    """

    APPLAUSE = "applause"
    HECKLE = "heckle"
    LAUGHTER = "laughter"
    PROCEDURAL = "procedural"
    OTHER = "other"


class ProtocolXmlReference(BaseModel):
    """
    Reference from an IVZ `xref` to a speech (`rid`).
    """

    rid: str = Field(..., description="Speech ID referenced by xref (rid)")
    pnr: Optional[str] = Field(None, description="Printed page number (pnr)")
    div: Optional[str] = Field(None, description="Page quadrant/division (div)")
    href: Optional[str] = Field(None, description="Anchor reference like S22848")
    seite: Optional[str] = Field(None, description="Printed page (seite)")
    seitenbereich: Optional[str] = Field(None, description="Quadrant as text (seitenbereich)")


class ProtocolXmlSpeaker(BaseModel):
    """
    Speaker metadata in BT protocol XML.
    """

    id: Optional[str] = Field(None, description="Speaker ID from <redner id=...>")
    titel: Optional[str] = Field(None, description="Academic title, e.g. Dr.")
    vorname: Optional[str] = Field(None, description="First name")
    nachname: Optional[str] = Field(None, description="Last name")
    fraktion: Optional[str] = Field(None, description="Faction")
    ortszusatz: Optional[str] = Field(None, description="Constituency add-on")
    rolle_lang: Optional[str] = Field(None, description="Long role label")
    rolle_kurz: Optional[str] = Field(None, description="Short role label")


class ProtocolXmlParagraph(BaseModel):
    """
    A paragraph in a speech or agenda section.
    """

    klasse: Optional[str] = Field(None, description="BT XML 'klasse' attribute")
    text: str = Field(..., description="Normalized paragraph text")


class ProtocolXmlStageDirection(BaseModel):
    """
    A non-spoken annotation like applause, heckles, etc.
    """

    type: StageDirectionType = Field(..., description="Classification")
    text: str = Field(..., description="Raw text (normalized)")


class ProtocolXmlSpeech(BaseModel):
    """
    A single speech (<rede>) with speaker and content.
    """

    id: Optional[str] = Field(None, description="Speech ID from <rede id=...>")
    top_id: Optional[str] = Field(None, description="Agenda item id (top-id)")
    top_title: Optional[str] = Field(None, description="Agenda title")
    reference: Optional[ProtocolXmlReference] = Field(None, description="IVZ reference")
    speaker: Optional[ProtocolXmlSpeaker] = Field(None, description="Speaker metadata")
    paragraphs: List[ProtocolXmlParagraph] = Field(default_factory=list)
    stage_directions: List[ProtocolXmlStageDirection] = Field(default_factory=list)
    text: str = Field("", description="Full speech text (joined paragraphs)")


class ProtocolXmlAgendaItem(BaseModel):
    """
    High-level agenda item extracted from <sitzungsverlauf>.
    """

    type: str = Field(..., description="sitzungsbeginn|tagesordnungspunkt|...")
    top_id: Optional[str] = Field(None, description="Agenda identifier (top-id)")
    top_number: Optional[int] = Field(None, description="Agenda item number if parseable")
    title: Optional[str] = Field(None, description="Agenda title if available")
    speech_ids: List[str] = Field(default_factory=list, description="Speech IDs under this item")


class Vorgang(BaseModel):
    """
    Typed representation of a legislative process (Vorgang).
    """

    id: Optional[str] = Field(None, description="DIP process ID")
    titel: Optional[str] = Field(None, description="Process title")
    vorgangstyp: Optional[str] = Field(None, description="Process type")
    wahlperiode: Optional[int] = Field(None, description="Legislative period")
    gesta: Optional[str] = Field(None, description="GESTA code if available")
    datum: Optional[date] = Field(None, description="Process date")
