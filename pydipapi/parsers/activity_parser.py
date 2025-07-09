"""
Activity parser for extracting structured data from activity/plenary session responses.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from .base_parser import BaseParser


class ActivityParser(BaseParser):
    """
    Parser for extracting structured data from activity/plenary session responses.
    
    Extracts information like session details, participants, topics,
    votes, and procedural information from activity API responses.
    """

    def __init__(self):
        """Initialize the activity parser."""
        super().__init__()

        # Activity type patterns
        self._activity_patterns = {
            'plenary_session': r'plenarsitzung',
            'committee_meeting': r'ausschusssitzung',
            'vote': r'abstimmung',
            'debate': r'debatte',
            'question_time': r'fragestunde',
            'government_statement': r'regierungserklärung',
            'oral_question': r'mündliche\s+anfrage',
            'written_question': r'schriftliche\s+anfrage',
        }

    def parse(self, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Parse activity data and extract structured information.
        
        Args:
            data: Raw activity data from API
            
        Returns:
            Parsed activity data with extracted information
        """
        if isinstance(data, list):
            return [self._parse_single_activity(activity) for activity in data]
        else:
            return self._parse_single_activity(data)

    def _parse_single_activity(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse a single activity.
        
        Args:
            activity: Single activity data
            
        Returns:
            Parsed activity with extracted information
        """
        if not activity:
            return {}

        parsed = activity.copy()

        # Extract basic information
        parsed['parsed'] = {
            'activity_type': self._extract_activity_type(activity),
            'session_info': self._extract_session_info(activity),
            'participants': self._extract_participants(activity),
            'topics': self._extract_topics(activity),
            'votes': self._extract_votes(activity),
            'procedural_info': self._extract_procedural_info(activity),
            'dates': self._extract_dates(activity),
            'references': self._extract_references(activity),
        }

        return parsed

    def _extract_activity_type(self, activity: Dict[str, Any]) -> Optional[str]:
        """
        Extract activity type from activity data.
        
        Args:
            activity: Activity data
            
        Returns:
            Activity type or None
        """
        # Check explicit activity type field
        activity_type = activity.get('aktivitaetstyp', activity.get('type', ''))
        if activity_type:
            return activity_type.lower().replace(' ', '_')

        # Extract from title or description
        title = activity.get('titel', '')
        description = activity.get('beschreibung', '')
        combined_text = f"{title} {description}".lower()

        for activity_type, pattern in self._activity_patterns.items():
            if self.extract_text(combined_text, pattern):
                return activity_type

        return None

    def _extract_session_info(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract session information.
        
        Args:
            activity: Activity data
            
        Returns:
            Session information dictionary
        """
        session_info = {
            'session_number': activity.get('sitzungsnummer', ''),
            'legislative_period': activity.get('wahlperiode', ''),
            'session_date': self.parse_date(activity.get('sitzungsdatum', '')),
            'start_time': activity.get('startzeit', ''),
            'end_time': activity.get('endzeit', ''),
            'location': activity.get('ort', ''),
            'status': activity.get('status', ''),
        }

        return session_info

    def _extract_participants(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract participant information.
        
        Args:
            activity: Activity data
            
        Returns:
            Participant information dictionary
        """
        participants = {
            'speakers': [],
            'attendees': [],
            'parties_present': [],
            'ministers_present': [],
        }

        # Extract from explicit participant fields
        if 'teilnehmer' in activity:
            for participant in activity['teilnehmer']:
                if isinstance(participant, dict):
                    participant_info = {
                        'name': participant.get('name', ''),
                        'party': participant.get('fraktion', ''),
                        'role': participant.get('rolle', ''),
                        'speaking_time': participant.get('redezeit', ''),
                    }
                    participants['speakers'].append(participant_info)
                elif isinstance(participant, str):
                    participants['speakers'].append({'name': participant})

        # Extract from text content
        text = activity.get('beschreibung', '') + ' ' + activity.get('protokoll', '')
        if text:
            # Extract party mentions
            parties = self.extract_parties(text)
            if parties:
                participants['parties_present'] = parties

        return participants

    def _extract_topics(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract topic information.
        
        Args:
            activity: Activity data
            
        Returns:
            Topic information dictionary
        """
        topics = {
            'main_topics': [],
            'agenda_items': [],
            'documents_discussed': [],
            'laws_discussed': [],
        }

        # Extract from explicit topic fields
        if 'themen' in activity:
            for topic in activity['themen']:
                if isinstance(topic, dict):
                    topic_info = {
                        'title': topic.get('titel', ''),
                        'description': topic.get('beschreibung', ''),
                        'start_time': topic.get('startzeit', ''),
                        'end_time': topic.get('endzeit', ''),
                    }
                    topics['main_topics'].append(topic_info)
                elif isinstance(topic, str):
                    topics['main_topics'].append({'title': topic})

        # Extract from text content
        text = activity.get('beschreibung', '') + ' ' + activity.get('protokoll', '')
        if text:
            # Extract law references
            laws = self.extract_laws(text)
            if laws:
                topics['laws_discussed'] = laws

        return topics

    def _extract_votes(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract voting information.
        
        Args:
            activity: Activity data
            
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
        if 'abstimmungen' in activity:
            for vote in activity['abstimmungen']:
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
        text = activity.get('beschreibung', '') + ' ' + activity.get('protokoll', '')
        if text:
            # Look for vote patterns
            vote_patterns = [
                r'(\d+)\s+ja\s+stimmen',
                r'(\d+)\s+nein\s+stimmen',
                r'(\d+)\s+enthaltungen',
                r'(\d+)\s+abwesend',
            ]

            for pattern in vote_patterns:
                match = self.extract_text(text, pattern)
                if match:
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

    def _extract_procedural_info(self, activity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract procedural information.
        
        Args:
            activity: Activity data
            
        Returns:
            Procedural information dictionary
        """
        procedural_info = {
            'session_chair': activity.get('sitzungsleiter', ''),
            'secretary': activity.get('protokollfuehrer', ''),
            'agenda_items': [],
            'procedural_motions': [],
            'interruptions': [],
        }

        # Extract from text content
        text = activity.get('beschreibung', '') + ' ' + activity.get('protokoll', '')
        if text:
            # Look for procedural elements
            if 'unterbrechung' in text.lower():
                procedural_info['has_interruptions'] = True

            if 'geschäftsordnung' in text.lower():
                procedural_info['has_procedural_motions'] = True

        return procedural_info

    def _extract_dates(self, activity: Dict[str, Any]) -> Dict[str, Optional[datetime]]:
        """
        Extract date information from activity data.
        
        Args:
            activity: Activity data
            
        Returns:
            Dictionary of date types and their values
        """
        dates = {}

        # Extract from explicit date fields
        date_fields = ['datum', 'sitzungsdatum', 'start_datum', 'end_datum']
        for field in date_fields:
            if field in activity:
                dates[field] = self.parse_date(str(activity[field]))

        # Extract from text content
        text = activity.get('beschreibung', '') + ' ' + activity.get('protokoll', '')
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

    def _extract_references(self, activity: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Extract references from activity data.
        
        Args:
            activity: Activity data
            
        Returns:
            Dictionary of reference types and their values
        """
        text = activity.get('beschreibung', '') + ' ' + activity.get('protokoll', '')
        if not text:
            return {}

        return {
            'links': self.extract_links(text),
            'laws': self.extract_laws(text),
            'emails': self.extract_emails(text),
            'phone_numbers': self.extract_phone_numbers(text),
        }
