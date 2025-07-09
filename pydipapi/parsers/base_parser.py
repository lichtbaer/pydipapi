"""
Base class for all content parsers.

Provides common functionality for parsing API responses and extracting
structured data.
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


class BaseParser:
    """Base class for all content parsers."""

    def parse(self, data: Union[Dict, List[Dict]]) -> Union[Dict, List[Dict]]:
        """
        Parse the input data and return structured information.

        Args:
            data: Raw API response data

        Returns:
            Parsed structured data
        """
        if isinstance(data, list):
            return [self._parse_single(item) for item in data]
        return self._parse_single(data)

    def _parse_single(self, data: Dict) -> Dict:
        """Parse a single item."""
        return {"parsed": data}

    def extract_text(self, text: str, pattern: str) -> Optional[str]:
        """
        Extract text using a regex pattern.

        Args:
            text: Text to search in
            pattern: Regex pattern to match

        Returns:
            Matched text or None
        """
        if not text or not pattern:
            return None

        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            return None
        # Return group(1) if it exists, else group(0)
        if match.lastindex and match.lastindex >= 1:
            return match.group(1)
        return match.group(0)

    def extract_all_text(self, text: str, pattern: str) -> List[str]:
        """
        Extract all matches using a regex pattern.

        Args:
            text: Text to search in
            pattern: Regex pattern to match

        Returns:
            List of matched strings
        """
        if not text or not pattern:
            return []

        matches = re.findall(pattern, text, re.IGNORECASE)
        return [match for match in matches if match]

    def parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse a date string into a datetime object.

        Args:
            date_str: Date string to parse

        Returns:
            Parsed datetime or None
        """
        if not date_str:
            return None

        # Common date formats
        date_formats = [
            "%Y-%m-%d",
            "%d.%m.%Y",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
        ]

        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        return None

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text content.

        Args:
            text: Raw text to clean

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Remove HTML tags
        text = re.sub(r"<[^>]+>", "", text)
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)
        # Remove leading/trailing whitespace
        text = text.strip()

        return text

    def extract_numbers(self, text: str) -> List[Union[int, float]]:
        """
        Extract numbers from text.

        Args:
            text: Text to extract numbers from

        Returns:
            List of numbers found
        """
        if not text:
            return []

        # Find all numbers (integers and floats)
        numbers = re.findall(r"\b\d+(?:\.\d+)?\b", text)
        result = []

        for num_str in numbers:
            try:
                if "." in num_str:
                    result.append(float(num_str))
                else:
                    result.append(int(num_str))
            except ValueError:
                continue

        return result

    def extract_links(self, text: str) -> List[str]:
        """
        Extract URLs from text.

        Args:
            text: Text to extract URLs from

        Returns:
            List of URLs found
        """
        if not text:
            return []

        # URL pattern
        url_pattern = r"https?://[^\s<>\"{}|\\^`\[\]]+"
        return re.findall(url_pattern, text, re.IGNORECASE)

    def extract_emails(self, text: str) -> List[str]:
        """
        Extract email addresses from text.

        Args:
            text: Text to extract emails from

        Returns:
            List of email addresses found
        """
        if not text:
            return []

        # Email pattern
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return re.findall(email_pattern, text)

    def extract_phone_numbers(self, text: str) -> List[str]:
        """
        Extract phone numbers from text.

        Args:
            text: Text to extract phone numbers from

        Returns:
            List of phone numbers found
        """
        if not text:
            return []

        # German phone number patterns
        phone_patterns = [
            r"\+49\s*\d{2,4}\s*\d{3,8}",  # +49 format
            r"0\d{2,4}\s*\d{3,8}",  # 0xx format
            r"\(\d{2,4}\)\s*\d{3,8}",  # (xx) format
        ]

        numbers = []
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            numbers.extend(matches)

        return numbers

    def extract_parties(self, text: str) -> List[str]:
        """
        Extract political party names from text.

        Args:
            text: Text to extract party names from

        Returns:
            List of party names found
        """
        if not text:
            return []

        # German political parties
        parties = [
            "CDU",
            "CSU",
            "CDU/CSU",
            "SPD",
            "FDP",
            "Grüne",
            "Bündnis 90/Die Grünen",
            "Die Linke",
            "AfD",
            "Alternative für Deutschland",
            "PDS",
            "Piraten",
            "Die Piraten",
            "Freie Wähler",
            "Tierschutzpartei",
            "NPD",
            "Die Republikaner",
            "REP",
        ]

        found_parties = []
        for party in parties:
            if re.search(rf"\b{re.escape(party)}\b", text, re.IGNORECASE):
                found_parties.append(party)

        return found_parties

    def extract_committees(self, text: str) -> List[str]:
        """
        Extract committee names from text.

        Args:
            text: Text to extract committee names from

        Returns:
            List of committee names found
        """
        if not text:
            return []

        # Common German parliamentary committees
        committees = [
            "Haushaltsausschuss",
            "Rechtsausschuss",
            "Innenausschuss",
            "Auswärtiger Ausschuss",
            "Verteidigungsausschuss",
            "Ausschuss für Arbeit und Soziales",
            "Ausschuss für Familie, Senioren, Frauen und Jugend",
            "Ausschuss für Gesundheit",
            "Ausschuss für Bildung, Forschung und Technikfolgenabschätzung",
            "Ausschuss für wirtschaftliche Zusammenarbeit und Entwicklung",
            "Ausschuss für Umwelt, Naturschutz und nukleare Sicherheit",
            "Ausschuss für Verkehr und digitale Infrastruktur",
            "Ausschuss für Ernährung und Landwirtschaft",
            "Ausschuss für wirtschaftliche Zusammenarbeit und Entwicklung",
            "Petitionsausschuss",
            "Ausschuss für Wahlprüfung, Immunität und Geschäftsordnung",
            "Ausschuss für Menschenrechte und humanitäre Hilfe",
            "Ausschuss für Tourismus",
            "Ausschuss für Sport",
            "Ausschuss für Kultur und Medien",
        ]

        found_committees = []
        for committee in committees:
            if re.search(rf"\b{re.escape(committee)}\b", text, re.IGNORECASE):
                found_committees.append(committee)

        return found_committees

    def extract_laws(self, text: str) -> List[str]:
        """
        Extract law references from text.

        Args:
            text: Text to extract law references from

        Returns:
            List of law references found
        """
        if not text:
            return []

        # Law reference patterns
        law_patterns = [
            r"§\s*\d+[a-zA-Z]*\s+[A-Za-zäöüßÄÖÜ\s]+",  # § 123 StGB
            r"Artikel\s+\d+\s+[A-Za-zäöüßÄÖÜ\s]+",  # Artikel 1 GG
            r"Art\.\s*\d+\s+[A-Za-zäöüßÄÖÜ\s]+",  # Art. 1 GG
            r"[A-Za-zäöüßÄÖÜ\s]+gesetz",  # Any law ending with "gesetz"
            r"BGB|StGB|GG|GGG|VwGO|ZPO|StPO",  # Common law abbreviations
        ]

        laws = []
        for pattern in law_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            laws.extend(matches)

        return laws
