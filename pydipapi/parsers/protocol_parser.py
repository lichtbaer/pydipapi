"""
Protocol parser for extracting structured data from protocol/transcript responses.
"""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from .base_parser import BaseParser


class ProtocolParser(BaseParser):
    """
    Parser for extracting structured data from protocol/transcript responses.
    
    Extracts information like speakers, topics, interventions,
    procedural elements, and voting records from protocol API responses.
    """

    def __init__(self):
        """Initialize the protocol parser."""
        super().__init__()
        
        # Speaker patterns
        self._speaker_patterns = {
            'president': r'präsident',
            'vice_president': r'vizepräsident',
            'minister': r'minister',
            'secretary': r'staatssekretär',
            'member': r'abgeordneter',
            'faction_leader': r'fraktionsvorsitzender',
        }

    def parse(self, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Parse protocol data and extract structured information.
        
        Args:
            data: Raw protocol data from API
            
        Returns:
            Parsed protocol data with extracted information
        """
        if isinstance(data, list):
            return [self._parse_single_protocol(protocol) for protocol in data]
        else:
            return self._parse_single_protocol(data)

    def _parse_single_protocol(self, protocol: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse a single protocol.
        
        Args:
            protocol: Single protocol data
            
        Returns:
            Parsed protocol with extracted information
        """
        if not protocol:
            return {}
            
        parsed = protocol.copy()
        
        # Extract basic information
        parsed['parsed'] = {
            'session_info': self._extract_session_info(protocol),
            'speakers': self._extract_speakers(protocol),
            'topics': self._extract_topics(protocol),
            'interventions': self._extract_interventions(protocol),
            'votes': self._extract_votes(protocol),
            'procedural_elements': self._extract_procedural_elements(protocol),
            'dates': self._extract_dates(protocol),
            'references': self._extract_references(protocol),
        }
        
        return parsed

    def _extract_session_info(self, protocol: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract session information.
        
        Args:
            protocol: Protocol data
            
        Returns:
            Session information dictionary
        """
        session_info = {
            'session_number': protocol.get('sitzungsnummer', ''),
            'legislative_period': protocol.get('wahlperiode', ''),
            'session_date': self.parse_date(protocol.get('sitzungsdatum', '')),
            'start_time': protocol.get('startzeit', ''),
            'end_time': protocol.get('endzeit', ''),
            'location': protocol.get('ort', ''),
            'session_chair': protocol.get('sitzungsleiter', ''),
            'secretary': protocol.get('protokollfuehrer', ''),
        }
        
        return session_info

    def _extract_speakers(self, protocol: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract speaker information.
        
        Args:
            protocol: Protocol data
            
        Returns:
            Speaker information dictionary
        """
        speakers = {
            'speakers_list': [],
            'parties_present': [],
            'ministers_present': [],
            'total_speakers': 0,
            'speaking_times': {},
        }
        
        # Extract from explicit speaker fields
        if 'sprecher' in protocol:
            for speaker in protocol['sprecher']:
                if isinstance(speaker, dict):
                    speaker_info = {
                        'name': speaker.get('name', ''),
                        'party': speaker.get('fraktion', ''),
                        'role': speaker.get('rolle', ''),
                        'speaking_time': speaker.get('redezeit', ''),
                        'interventions': speaker.get('interventionen', 0),
                    }
                    speakers['speakers_list'].append(speaker_info)
                    
                    # Track speaking time
                    if speaker_info['speaking_time']:
                        speakers['speaking_times'][speaker_info['name']] = speaker_info['speaking_time']
                        
                elif isinstance(speaker, str):
                    speakers['speakers_list'].append({'name': speaker})
                    
        # Extract from text content
        text = protocol.get('text', '') + ' ' + protocol.get('protokoll', '')
        if text:
            # Extract party mentions
            parties = self.extract_parties(text)
            if parties:
                speakers['parties_present'] = parties
                
            # Count speakers by looking for patterns like "Herr/Frau [Name]"
            speaker_patterns = [
                r'Herr\s+([A-Za-zäöüß\s]+)',
                r'Frau\s+([A-Za-zäöüß\s]+)',
                r'([A-Za-zäöüß\s]+)\s+\([^)]+\):',
            ]
            
            for pattern in speaker_patterns:
                matches = self.extract_all_text(text, pattern)
                speakers['total_speakers'] += len(matches)
                
        return speakers

    def _extract_topics(self, protocol: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract topic information.
        
        Args:
            protocol: Protocol data
            
        Returns:
            Topic information dictionary
        """
        topics = {
            'agenda_items': [],
            'main_topics': [],
            'laws_discussed': [],
            'documents_referenced': [],
        }
        
        # Extract from explicit topic fields
        if 'themen' in protocol:
            for topic in protocol['themen']:
                if isinstance(topic, dict):
                    topic_info = {
                        'title': topic.get('titel', ''),
                        'description': topic.get('beschreibung', ''),
                        'start_time': topic.get('startzeit', ''),
                        'end_time': topic.get('endzeit', ''),
                        'speakers': topic.get('sprecher', []),
                    }
                    topics['agenda_items'].append(topic_info)
                elif isinstance(topic, str):
                    topics['agenda_items'].append({'title': topic})
                    
        # Extract from text content
        text = protocol.get('text', '') + ' ' + protocol.get('protokoll', '')
        if text:
            # Extract law references
            laws = self.extract_laws(text)
            if laws:
                topics['laws_discussed'] = laws
                
            # Look for topic patterns
            topic_patterns = [
                r'Punkt\s+(\d+):\s+([^\.]+)',
                r'Thema:\s+([^\.]+)',
                r'Beratung\s+über\s+([^\.]+)',
            ]
            
            for pattern in topic_patterns:
                matches = self.extract_all_text(text, pattern)
                for match in matches:
                    if isinstance(match, tuple) and len(match) >= 2:
                        topics['main_topics'].append(match[1].strip())
                    elif isinstance(match, str):
                        topics['main_topics'].append(match.strip())
                        
        return topics

    def _extract_interventions(self, protocol: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract intervention information.
        
        Args:
            protocol: Protocol data
            
        Returns:
            Intervention information dictionary
        """
        interventions = {
            'interventions_list': [],
            'total_interventions': 0,
            'intervention_types': {},
            'speaker_interventions': {},
        }
        
        # Extract from text content
        text = protocol.get('text', '') + ' ' + protocol.get('protokoll', '')
        if text:
            # Look for intervention patterns
            intervention_patterns = [
                r'([A-Za-zäöüß\s]+):\s+([^\.]+)',
                r'([A-Za-zäöüß\s]+)\s+\([^)]+\):\s+([^\.]+)',
            ]
            
            for pattern in intervention_patterns:
                matches = self.extract_all_text(text, pattern)
                for match in matches:
                    if isinstance(match, tuple) and len(match) >= 2:
                        speaker = match[0].strip()
                        content = match[1].strip()
                        
                        intervention_info = {
                            'speaker': speaker,
                            'content': content,
                            'length': len(content),
                        }
                        interventions['interventions_list'].append(intervention_info)
                        
                        # Track by speaker
                        if speaker not in interventions['speaker_interventions']:
                            interventions['speaker_interventions'][speaker] = []
                        interventions['speaker_interventions'][speaker].append(intervention_info)
                        
            interventions['total_interventions'] = len(interventions['interventions_list'])
            
        return interventions

    def _extract_votes(self, protocol: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract voting information.
        
        Args:
            protocol: Protocol data
            
        Returns:
            Voting information dictionary
        """
        votes = {
            'vote_results': [],
            'total_votes': 0,
            'yes_votes': 0,
            'no_votes': 0,
            'abstentions': 0,
            'absent': 0,
        }
        
        # Extract from explicit vote fields
        if 'abstimmungen' in protocol:
            for vote in protocol['abstimmungen']:
                if isinstance(vote, dict):
                    vote_info = {
                        'topic': vote.get('thema', ''),
                        'result': vote.get('ergebnis', ''),
                        'yes': vote.get('ja', 0),
                        'no': vote.get('nein', 0),
                        'abstentions': vote.get('enthaltungen', 0),
                        'absent': vote.get('abwesend', 0),
                    }
                    votes['vote_results'].append(vote_info)
                    
                    # Update totals
                    votes['yes_votes'] += vote_info['yes']
                    votes['no_votes'] += vote_info['no']
                    votes['abstentions'] += vote_info['abstentions']
                    votes['absent'] += vote_info['absent']
                    
        # Extract from text content
        text = protocol.get('text', '') + ' ' + protocol.get('protokoll', '')
        if text:
            # Look for vote patterns
            vote_patterns = [
                r'(\d+)\s+ja\s+stimmen',
                r'(\d+)\s+nein\s+stimmen',
                r'(\d+)\s+enthaltungen',
                r'(\d+)\s+abwesend',
                r'Abstimmung:\s+Ja:\s+(\d+),\s+Nein:\s+(\d+),\s+Enthaltungen:\s+(\d+)',
            ]
            
            for pattern in vote_patterns:
                match = self.extract_text(text, pattern)
                if match:
                    if 'Abstimmung:' in pattern:
                        # Complex vote pattern
                        numbers = self.extract_numbers(match)
                        if len(numbers) >= 3:
                            votes['yes_votes'] = numbers[0]
                            votes['no_votes'] = numbers[1]
                            votes['abstentions'] = numbers[2]
                    else:
                        # Simple vote pattern
                        number = int(match)
                        if 'ja' in pattern:
                            votes['yes_votes'] = number
                        elif 'nein' in pattern:
                            votes['no_votes'] = number
                        elif 'enthaltungen' in pattern:
                            votes['abstentions'] = number
                        elif 'abwesend' in pattern:
                            votes['absent'] = number
                            
        votes['total_votes'] = votes['yes_votes'] + votes['no_votes'] + votes['abstentions']
        
        return votes

    def _extract_procedural_elements(self, protocol: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract procedural elements.
        
        Args:
            protocol: Protocol data
            
        Returns:
            Procedural elements dictionary
        """
        procedural_elements = {
            'interruptions': [],
            'procedural_motions': [],
            'points_of_order': [],
            'adjournments': [],
            'has_interruptions': False,
            'has_procedural_motions': False,
        }
        
        # Extract from text content
        text = protocol.get('text', '') + ' ' + protocol.get('protokoll', '')
        if text:
            # Look for procedural elements
            if 'unterbrechung' in text.lower():
                procedural_elements['has_interruptions'] = True
                
            if 'geschäftsordnung' in text.lower():
                procedural_elements['has_procedural_motions'] = True
                
            # Look for specific procedural patterns
            procedural_patterns = [
                r'Unterbrechung\s+([^\.]+)',
                r'Geschäftsordnung\s+([^\.]+)',
                r'Punkt\s+der\s+Geschäftsordnung\s+([^\.]+)',
            ]
            
            for pattern in procedural_patterns:
                matches = self.extract_all_text(text, pattern)
                for match in matches:
                    if isinstance(match, str):
                        procedural_elements['procedural_motions'].append(match.strip())
                        
        return procedural_elements

    def _extract_dates(self, protocol: Dict[str, Any]) -> Dict[str, Optional[datetime]]:
        """
        Extract date information from protocol data.
        
        Args:
            protocol: Protocol data
            
        Returns:
            Dictionary of date types and their values
        """
        dates = {}
        
        # Extract from explicit date fields
        date_fields = ['datum', 'sitzungsdatum', 'start_datum', 'end_datum']
        for field in date_fields:
            if field in protocol:
                dates[field] = self.parse_date(str(protocol[field]))
                
        # Extract from text content
        text = protocol.get('text', '') + ' ' + protocol.get('protokoll', '')
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

    def _extract_references(self, protocol: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Extract references from protocol data.
        
        Args:
            protocol: Protocol data
            
        Returns:
            Dictionary of reference types and their values
        """
        text = protocol.get('text', '') + ' ' + protocol.get('protokoll', '')
        if not text:
            return {}
            
        return {
            'links': self.extract_links(text),
            'laws': self.extract_laws(text),
            'emails': self.extract_emails(text),
            'phone_numbers': self.extract_phone_numbers(text),
        } 