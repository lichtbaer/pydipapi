"""
Person parser for extracting structured data from person/member responses.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from .base_parser import BaseParser


class PersonParser(BaseParser):
    """
    Parser for extracting structured data from person/member responses.

    Extracts information like party affiliation, committees, roles,
    contact information, and biographical data from person API responses.
    """

    def __init__(self):
        """Initialize the person parser."""
        super().__init__()

        # Role patterns
        self._role_patterns = {
            "president": r"präsident",
            "vice_president": r"vizepräsident",
            "minister": r"minister",
            "secretary": r"staatssekretär",
            "committee_chair": r"vorsitzender",
            "committee_member": r"mitglied",
            "faction_leader": r"fraktionsvorsitzender",
            "faction_member": r"fraktionsmitglied",
        }

    def parse(
        self, data: Union[Dict[str, Any], List[Dict[str, Any]]]
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Parse person data and extract structured information.

        Args:
            data: Raw person data from API

        Returns:
            Parsed person data with extracted information
        """
        if isinstance(data, list):
            return [self._parse_single_person(person) for person in data]
        else:
            return self._parse_single_person(data)

    def _parse_single_person(self, person: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse a single person.

        Args:
            person: Single person data

        Returns:
            Parsed person with extracted information
        """
        if not person:
            return {}

        parsed = person.copy()

        # Extract basic information
        parsed["parsed"] = {
            "basic_info": self._extract_basic_info(person),
            "party_info": self._extract_party_info(person),
            "committee_info": self._extract_committee_info(person),
            "role_info": self._extract_role_info(person),
            "contact_info": self._extract_contact_info(person),
            "biographical_info": self._extract_biographical_info(person),
            "constituency_info": self._extract_constituency_info(person),
            "dates": self._extract_dates(person),
        }

        return parsed

    def _extract_basic_info(self, person: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract basic person information.

        Args:
            person: Person data

        Returns:
            Basic information dictionary
        """
        return {
            "name": person.get("name", ""),
            "first_name": person.get("vorname", ""),
            "last_name": person.get("nachname", ""),
            "title": person.get("titel", ""),
            "gender": person.get("geschlecht", ""),
            "id": person.get("id", ""),
        }

    def _extract_party_info(self, person: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract party affiliation information.

        Args:
            person: Person data

        Returns:
            Party information dictionary
        """
        party_info = {
            "current_party": person.get("fraktion", ""),
            "party_history": [],
            "faction_role": "",
        }

        # Extract from text content
        text = person.get("biografie", "") + " " + person.get("beschreibung", "")
        if text:
            # Look for party mentions
            parties = self.extract_parties(text)
            if parties:
                party_info["mentioned_parties"] = parties

        return party_info

    def _extract_committee_info(self, person: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract committee information.

        Args:
            person: Person data

        Returns:
            Committee information dictionary
        """
        committee_info = {
            "current_committees": [],
            "committee_history": [],
            "committee_roles": [],
        }

        # Extract from explicit committee fields
        if "ausschuesse" in person:
            for committee in person["ausschuesse"]:
                if isinstance(committee, dict):
                    committee_info["current_committees"].append(
                        {
                            "name": committee.get("name", ""),
                            "role": committee.get("rolle", ""),
                            "start_date": self.parse_date(
                                committee.get("start_datum", "")
                            ),
                            "end_date": self.parse_date(committee.get("end_datum", "")),
                        }
                    )
                elif isinstance(committee, str):
                    committee_info["current_committees"].append({"name": committee})

        # Extract from text content
        text = person.get("biografie", "") + " " + person.get("beschreibung", "")
        if text:
            committees = self.extract_committees(text)
            if committees:
                committee_info["mentioned_committees"] = committees

        return committee_info

    def _extract_role_info(self, person: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract role information.

        Args:
            person: Person data

        Returns:
            Role information dictionary
        """
        role_info = {
            "current_roles": [],
            "role_history": [],
            "is_president": False,
            "is_vice_president": False,
            "is_minister": False,
            "is_secretary": False,
        }

        # Extract from explicit role fields
        if "rollen" in person:
            for role in person["rollen"]:
                if isinstance(role, dict):
                    role_info["current_roles"].append(
                        {
                            "name": role.get("name", ""),
                            "start_date": self.parse_date(role.get("start_datum", "")),
                            "end_date": self.parse_date(role.get("end_datum", "")),
                        }
                    )
                elif isinstance(role, str):
                    role_info["current_roles"].append({"name": role})

        # Extract from text content
        text = person.get("biografie", "") + " " + person.get("beschreibung", "")
        if text:
            for role_type, pattern in self._role_patterns.items():
                if self.extract_text(text, pattern):
                    role_info[f"is_{role_type}"] = True

        return role_info

    def _extract_contact_info(self, person: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract contact information.

        Args:
            person: Person data

        Returns:
            Contact information dictionary
        """
        contact_info = {
            "email": person.get("email", ""),
            "phone": person.get("telefon", ""),
            "fax": person.get("fax", ""),
            "website": person.get("website", ""),
            "address": person.get("adresse", ""),
        }

        # Extract from text content
        text = person.get("biografie", "") + " " + person.get("beschreibung", "")
        if text:
            emails = self.extract_emails(text)
            if emails:
                contact_info["extracted_emails"] = emails

            phones = self.extract_phone_numbers(text)
            if phones:
                contact_info["extracted_phones"] = phones

            links = self.extract_links(text)
            if links:
                contact_info["extracted_links"] = links

        return contact_info

    def _extract_biographical_info(self, person: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract biographical information.

        Args:
            person: Person data

        Returns:
            Biographical information dictionary
        """
        bio_info = {
            "birth_date": self.parse_date(person.get("geburtsdatum", "")),
            "birth_place": person.get("geburtsort", ""),
            "education": person.get("ausbildung", ""),
            "profession": person.get("beruf", ""),
            "biography": self.clean_text(person.get("biografie", "")),
        }

        # Extract from text content
        text = person.get("biografie", "") + " " + person.get("beschreibung", "")
        if text:
            # Extract numbers (could be years, percentages, etc.)
            numbers = self.extract_numbers(text)
            if numbers:
                bio_info["extracted_numbers"] = numbers

        return bio_info

    def _extract_constituency_info(self, person: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract constituency information.

        Args:
            person: Person data

        Returns:
            Constituency information dictionary
        """
        constituency_info = {
            "constituency": person.get("wahlkreis", ""),
            "state": person.get("bundesland", ""),
            "list_position": person.get("listenplatz", ""),
            "election_type": person.get("wahlart", ""),
        }

        return constituency_info

    def _extract_dates(self, person: Dict[str, Any]) -> Dict[str, Optional[datetime]]:
        """
        Extract date information from person data.

        Args:
            person: Person data

        Returns:
            Dictionary of date types and their values
        """
        dates = {}

        # Extract from explicit date fields
        date_fields = ["geburtsdatum", "eintrittsdatum", "austrittsdatum", "wahl_datum"]
        for field in date_fields:
            if field in person:
                dates[field] = self.parse_date(str(person[field]))

        return dates
