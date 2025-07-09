"""
Base parser for extracting structured data from API responses.
"""

import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


class BaseParser(ABC):
    """
    Base class for all content parsers.
    
    Provides common functionality for parsing API responses and extracting
    structured data.
    """

    def __init__(self):
        """Initialize the base parser."""
        self._text_patterns = {}
        self._date_patterns = {}
        self._number_patterns = {}

    @abstractmethod
    def parse(self, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Parse the input data and return structured information.
        
        Args:
            data: Raw API response data
            
        Returns:
            Parsed structured data
        """
        pass

    def extract_text(self, text: str, pattern: str) -> Optional[str]:
        """
        Extract text using a regex pattern.
        
        Args:
            text: Text to search in
            pattern: Regex pattern to match
            
        Returns:
            Matched text or None
        """
        if not text:
            return None
            
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            # If the pattern has capture groups, return the first group
            if match.groups():
                return match.group(1)
            # Otherwise return the entire match
            return match.group(0)
        return None

    def extract_all_text(self, text: str, pattern: str) -> List[str]:
        """
        Extract all matches using a regex pattern.
        
        Args:
            text: Text to search in
            pattern: Regex pattern to match
            
        Returns:
            List of matched strings
        """
        if not text:
            return []
            
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
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
            "%d.%m.%Y %H:%M",
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
            
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Remove control characters
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        return text.strip()

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
            
        # Match integers and floats
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
        result = []
        
        for num_str in numbers:
            try:
                if '.' in num_str:
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
            
        # Match URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        return re.findall(url_pattern, text)

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
            
        # Match email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
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
            
        # Match German phone numbers
        phone_patterns = [
            r'\+49\s*\d{2,4}\s*\d{3,8}',  # +49 format
            r'0\d{2,4}\s*\d{3,8}',         # 0 format
            r'\(\d{2,4}\)\s*\d{3,8}',      # (area) format
        ]
        
        results = []
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            results.extend(matches)
            
        return results

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
            
        # Common German political parties
        parties = [
            'CDU', 'CSU', 'SPD', 'FDP', 'Grüne', 'Bündnis 90/Die Grünen',
            'Die Linke', 'AfD', 'PDS', 'Piraten', 'NPD', 'REP',
            'Christlich Demokratische Union', 'Christlich-Soziale Union',
            'Sozialdemokratische Partei Deutschlands', 'Freie Demokratische Partei',
            'Alternative für Deutschland', 'Die Linke'
        ]
        
        found_parties = []
        for party in parties:
            if re.search(rf'\b{re.escape(party)}\b', text, re.IGNORECASE):
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
            'Ausschuss für', 'Ausschuss für', 'Haushaltsausschuss',
            'Rechtsausschuss', 'Innenausschuss', 'Auswärtiger Ausschuss',
            'Verteidigungsausschuss', 'Ausschuss für Arbeit und Soziales',
            'Ausschuss für Familie, Senioren, Frauen und Jugend',
            'Ausschuss für Gesundheit', 'Ausschuss für Bildung, Forschung und Technikfolgenabschätzung',
            'Ausschuss für wirtschaftliche Zusammenarbeit und Entwicklung',
            'Ausschuss für Tourismus', 'Ausschuss für Sport',
            'Ausschuss für Menschenrechte und humanitäre Hilfe',
            'Ausschuss für die Angelegenheiten der Europäischen Union',
            'Petitionsausschuss', 'Ausschuss für Wahlprüfung, Immunität und Geschäftsordnung'
        ]
        
        found_committees = []
        for committee in committees:
            if re.search(rf'\b{re.escape(committee)}\b', text, re.IGNORECASE):
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
            
        # Match law references like "§ 123 StGB" or "Artikel 1 GG"
        law_patterns = [
            r'§\s*\d+[a-z]?\s+[A-Za-z]+',  # § 123 StGB
            r'Artikel\s+\d+\s+[A-Za-z]+',   # Artikel 1 GG
            r'Gesetz\s+über\s+[^,\.]+',     # Gesetz über...
            r'Verordnung\s+über\s+[^,\.]+', # Verordnung über...
        ]
        
        results = []
        for pattern in law_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            results.extend(matches)
            
        return results 