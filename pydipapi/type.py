from typing import List, Optional
from pydantic import BaseModel, Field, constr

class Vorgangsbezug(BaseModel):
    id: constr(regex=r'^\d+$') = Field(..., example="84393", description="ID eines verknüpften Vorgangs")
    titel: str = Field(..., example="Eröffnung der 1. Sitzung des 19. Deutschen Bundestages")
    vorgangstyp: str = Field(..., example="Ansprache/Erklärung/Mitteilung")

class Vorgangspositionbezug(Vorgangsbezug):
    vorgangsposition: str = Field(..., example="Ansprache")

class VorgangVerlinkung(BaseModel):
    id: constr(regex=r'^\d+$') = Field(..., example="282237", description="ID eines verknüpften Vorgangs")
    verweisung: str = Field(..., example="Bericht")
    titel: str = Field(..., example="Zwischenbericht zur Reform des Bundeswahlrechts und zur Modernisierung der Parlamentsarbeit")
    wahlperiode: int = Field(..., example=19)
    gesta: Optional[str]

class Bundesland(str, Enum):
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
    datum: date

class Quadrant(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

class Zuordnung(str, Enum):
    BT = "BT"
    BR = "BR"
    BV = "BV"
    EK = "EK"