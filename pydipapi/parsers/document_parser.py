"""
Document parser for extracting structured data from document responses.
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from .base_parser import BaseParser


class DocumentParser(BaseParser):
    """
    Parser for extracting structured data from document responses.
    
    Extracts information like document type, authors, dates, content,
    references, and metadata from document API responses.
    """

    def __init__(self):
        """Initialize the document parser."""
        super().__init__()

        # Document type patterns
        self._doc_type_patterns = {
            'kleine_anfrage': r'kleine\s+anfrage',
            'grosse_anfrage': r'große\s+anfrage',
            'antrag': r'antrag',
            'gesetzentwurf': r'gesetzentwurf',
            'bericht': r'bericht',
            'beschlussempfehlung': r'beschlussempfehlung',
            'stellungnahme': r'stellungnahme',
            'protokoll': r'protokoll',
        }

    def parse(self, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Parse document data and extract structured information.
        
        Args:
            data: Raw document data from API
            
        Returns:
            Parsed document data with extracted information
        """
        if isinstance(data, list):
            return [self._parse_single_document(doc) for doc in data]
        else:
            return self._parse_single_document(data)

    def _parse_single_document(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse a single document.
        
        Args:
            doc: Single document data
            
        Returns:
            Parsed document with extracted information
        """
        if not doc:
            return {}

        parsed = doc.copy()

        # Extract basic information
        parsed['parsed'] = {
            'document_type': self._extract_document_type(doc),
            'authors': self._extract_authors(doc),
            'dates': self._extract_dates(doc),
            'content_summary': self._extract_content_summary(doc),
            'references': self._extract_references(doc),
            'parties': self._extract_parties_from_doc(doc),
            'committees': self._extract_committees_from_doc(doc),
            'laws': self._extract_laws_from_doc(doc),
            'links': self._extract_links_from_doc(doc),
            'emails': self._extract_emails_from_doc(doc),
            'phone_numbers': self._extract_phone_numbers_from_doc(doc),
            'numbers': self._extract_numbers_from_doc(doc),
        }

        return parsed

    def _extract_document_type(self, doc: Dict[str, Any]) -> Optional[str]:
        """
        Extract document type from document data.
        
        Args:
            doc: Document data
            
        Returns:
            Document type or None
        """
        # Check explicit document type field
        doc_type = doc.get('dokumentart', doc.get('type', ''))
        if doc_type:
            return doc_type.lower().replace(' ', '_')

        # Extract from title or content
        title = doc.get('titel', '')
        content = doc.get('text', '')
        combined_text = f"{title} {content}".lower()

        for doc_type, pattern in self._doc_type_patterns.items():
            if self.extract_text(combined_text, pattern):
                return doc_type

        return None

    def _extract_authors(self, doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract author information from document.
        
        Args:
            doc: Document data
            
        Returns:
            List of author dictionaries
        """
        authors = []

        # Check for explicit author fields
        if 'autoren' in doc:
            for author in doc['autoren']:
                if isinstance(author, dict):
                    authors.append({
                        'name': author.get('name', ''),
                        'party': author.get('fraktion', ''),
                        'constituency': author.get('wahlkreis', ''),
                        'role': author.get('rolle', ''),
                    })
                elif isinstance(author, str):
                    authors.append({'name': author})

        # Extract from text content
        text = doc.get('text', '')
        title = doc.get('titel', '')
        combined_text = f"{title} {text}"

        if combined_text:
            # Look for patterns like "von [Name] (CDU/CSU)" or "der Abgeordneten [Name] (CDU/CSU)"
            author_patterns = [
                r'von\s+([^\(\)]+?)\s*\(([^\)]+)\)',
                r'der\s+Abgeordneten\s+([^\(\)]+?)\s*\(([^\)]+)\)',
                r'([^\(\)]+?)\s*\(([^\)]+)\)'  # General pattern
            ]

            for pattern in author_patterns:
                matches = re.findall(pattern, combined_text, re.IGNORECASE | re.MULTILINE)

                for match in matches:
                    if isinstance(match, tuple) and len(match) >= 2:
                        name = match[0].strip()
                        party = match[1].strip()

                        # Skip if it's already added
                        if not any(a['name'] == name for a in authors):
                            authors.append({
                                'name': name,
                                'party': party,
                            })

        return authors

    def _extract_dates(self, doc: Dict[str, Any]) -> Dict[str, Optional[datetime]]:
        """
        Extract date information from document.
        
        Args:
            doc: Document data
            
        Returns:
            Dictionary of date types and their values
        """
        dates = {}

        # Extract from explicit date fields
        date_fields = ['datum', 'erstellt', 'veröffentlicht', 'eingereicht']
        for field in date_fields:
            if field in doc:
                dates[field] = self.parse_date(str(doc[field]))

        # Extract from text content
        text = doc.get('text', '')
        if text:
            # Look for date patterns
            date_patterns = [
                r'(\d{1,2}\.\d{1,2}\.\d{4})',  # DD.MM.YYYY
                r'(\d{4}-\d{1,2}-\d{1,2})',    # YYYY-MM-DD
            ]

            for pattern in date_patterns:
                matches = self.extract_all_text(text, pattern)
                for match in matches:
                    parsed_date = self.parse_date(match)
                    if parsed_date:
                        dates['extracted_date'] = parsed_date
                        break

        return dates

    def _extract_content_summary(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract content summary from document.
        
        Args:
            doc: Document data
            
        Returns:
            Content summary dictionary
        """
        text = doc.get('text', '')
        if not text:
            return {}

        # Clean the text
        cleaned_text = self.clean_text(text)

        # Extract key information
        summary = {
            'word_count': len(cleaned_text.split()),
            'character_count': len(cleaned_text),
            'has_tables': 'tabelle' in cleaned_text.lower(),
            'has_figures': any(word in cleaned_text.lower() for word in ['abbildung', 'grafik', 'diagramm']),
            'has_references': len(self.extract_links(cleaned_text)) > 0,
            'has_law_references': len(self.extract_laws(cleaned_text)) > 0,
        }

        # Extract first few sentences as preview
        sentences = cleaned_text.split('.')
        if sentences:
            summary['preview'] = '. '.join(sentences[:3]).strip()

        return summary

    def _extract_references(self, doc: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Extract references from document.
        
        Args:
            doc: Document data
            
        Returns:
            Dictionary of reference types and their values
        """
        text = doc.get('text', '')
        if not text:
            return {}

        return {
            'links': self.extract_links(text),
            'laws': self.extract_laws(text),
            'emails': self.extract_emails(text),
            'phone_numbers': self.extract_phone_numbers(text),
        }

    def _extract_parties_from_doc(self, doc: Dict[str, Any]) -> List[str]:
        """Extract political parties mentioned in document."""
        text = doc.get('text', '')
        title = doc.get('titel', '')
        combined_text = f"{title} {text}"
        return self.extract_parties(combined_text)

    def _extract_committees_from_doc(self, doc: Dict[str, Any]) -> List[str]:
        """Extract committees mentioned in document."""
        text = doc.get('text', '')
        title = doc.get('titel', '')
        combined_text = f"{title} {text}"
        return self.extract_committees(combined_text)

    def _extract_laws_from_doc(self, doc: Dict[str, Any]) -> List[str]:
        """Extract law references from document."""
        text = doc.get('text', '')
        title = doc.get('titel', '')
        combined_text = f"{title} {text}"
        return self.extract_laws(combined_text)

    def _extract_links_from_doc(self, doc: Dict[str, Any]) -> List[str]:
        """Extract links from document."""
        text = doc.get('text', '')
        return self.extract_links(text)

    def _extract_emails_from_doc(self, doc: Dict[str, Any]) -> List[str]:
        """Extract email addresses from document."""
        text = doc.get('text', '')
        return self.extract_emails(text)

    def _extract_phone_numbers_from_doc(self, doc: Dict[str, Any]) -> List[str]:
        """Extract phone numbers from document."""
        text = doc.get('text', '')
        return self.extract_phone_numbers(text)

    def _extract_numbers_from_doc(self, doc: Dict[str, Any]) -> List[Union[int, float]]:
        """Extract numbers from document."""
        text = doc.get('text', '')
        return self.extract_numbers(text)
