from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, constr


class Vorgangsbezug(BaseModel):
    """
    Represents a reference to a legislative process.
    """
    id: constr(strict=True, pattern=r'^\d+$') = Field(..., json_schema_extra={"example": "84393", "description": "ID eines verknüpften Vorgangs"})
    titel: str = Field(..., json_schema_extra={"example": "Eröffnung der 1. Sitzung des 19. Deutschen Bundestages", "description": "Title of the process"})
    vorgangstyp: str = Field(..., json_schema_extra={"example": "Ansprache/Erklärung/Mitteilung", "description": "Type of the process"})


class Vorgangspositionbezug(Vorgangsbezug):
    """
    Represents a specific position within a legislative process.
    """
    vorgangsposition: str = Field(..., json_schema_extra={"example": "Ansprache", "description": "Position within the process"})


class VorgangVerlinkung(BaseModel):
    """
    Represents a link to a legislative process.
    """
    id: constr(strict=True, pattern=r'^\d+$') = Field(..., json_schema_extra={"example": "282237", "description": "ID eines verknüpften Vorgangs"})
    verweisung: str = Field(..., json_schema_extra={"example": "Bericht", "description": "Reference type"})
    titel: str = Field(..., json_schema_extra={"example": "Zwischenbericht zur Reform des Bundeswahlrechts und zur Modernisierung der Parlamentsarbeit", "description": "Title of the reference"})
    wahlperiode: int = Field(..., json_schema_extra={"example": 19, "description": "Legislative period"})
    gesta: Optional[str] = Field(None, json_schema_extra={"description": "GESTA code if available"})


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
    datum: date = Field(..., json_schema_extra={"description": "The date in YYYY-MM-DD format"})


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
