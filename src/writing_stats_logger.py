"""Writing Statistics Logger Module
This module handles logging daily writing statistics including word counts,
page summaries, and other metrics for tracking writing progress over time.
"""
import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

class WritingStatsLogger:
    """Logger for tracking daily writing statistics and progress.
    
    This class manages persistent logging of writing sessions, including
    word counts, page summaries, and metadata for analytics and progress tracking.
    """
    
    def __init__(self, log_file: str = "daily_writing_log.json", csv_log: str = "daily_writing_log.csv"):
        """Initialize the Writing Statistics Logger.
        
        Args:
            log_file: Path to JSON log file for detailed statistics
            csv_log: Path to CSV log file for simplified analytics
        """
        self.json_log_file = Path(log_file)
        self.csv_log_file = Path(csv_log)
        
        # Ensure log files exist
        self._initialize_log_files()
        
    def _initialize_log_files(self) -> None:
        """Initialize log files if they don't exist."""
        # Initialize JSON log file
        if not self.json_log_file.exists():
            with open(self.json_log_file, 'w') as f:
                json.dump([], f, indent=2)
        
        # Initialize CSV log file with headers
        if not self.csv_log_file.exists():
            with open(self.csv_log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'date', 'word_count', 'page_summary', 'total_words', 
                    'chapter', 'inspiration_sources', 'writing_duration_minutes'
                ])
    
    def log_writing_session(self, 
                           word_count: int,
                           page_summary: str,
                           total_words: int = 0,
                           chapter: int = 1,
                           inspiration_sources: Optional[List[str]] = None,
                           writing_duration_minutes: Optional[int] = None,
                           metadata: Optional[Dict[str, Any]] = None,
                           date: Optional[datetime] = None) -> None:
        """Log a writing session with comprehensive statistics.
        
        Args:
            word_count: Number of words written in this session
            page_summary: Brief summary of the page content
            total_words: Total word count in the novel so far
            chapter: Current chapter number
            inspiration_sources: List of sources that inspired this session
            writing_duration_minutes: How long the writing session took
            metadata: Additional metadata for the session
            date: Date of the writing session (defaults to now)
        """
        session_date = date or datetime.now()
        inspiration_sources = inspiration_sources or []
        metadata = metadata or {}
        
        # Create detailed log entry
        log_entry = {
            "date": session_date.isoformat(),
            "word_count": word_count,
            "page_summary": page_summary,
            "total_words": total_words,
            "chapter": chapter,
            "inspiration_sources": inspiration_sources,
            "writing_duration_minutes": writing_duration_minutes,
            "metadata": metadata
        }
        
        # Append to JSON log
        self._append_to_json_log(log_entry)
        
        # Append to CSV log
        self._append_to_csv_log(log_entry)
    
    def _append_to_json_log(self, log_entry: Dict[str, Any]) -> None:
        """Append entry to JSON log file.
        
        Args:
            log_entry: Dictionary containing log entry data
        """
        try:
            # Read existing data
            with open(self.json_log_file, 'r') as f:
                data = json.load(f)
            
            # Append new entry
            data.append(log_entry)
            
            # Write back to file
            with open(self.json_log_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error writing to JSON log: {e}")
    
    def _append_to_csv_log(self, log_entry: Dict[str, Any]) -> None:
        """Append entry to CSV log file.
        
        Args:
            log_entry: Dictionary containing log entry data
        """
        try:
            with open(self.csv_log_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    log_entry['date'],
                    log_entry['word_count'],
                    log_entry['page_summary'],
                    log_entry['total_words'],
                    log_entry['chapter'],
                    '; '.join(log_entry['inspiration_sources']),
                    log_entry['writing_duration_minutes']
                ])
        except Exception as e:
            print(f"Error writing to CSV log: {e}")
    
    def get_writing_history(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get writing history for the specified number of days.
        
        Args:
            days: Number of days to retrieve history for
            
        Returns:
            List of writing session entries
        """
        try:
            with open(self.json_log_file, 'r') as f:
                data = json.load(f)
            
            # Filter by date if needed
            if days > 0:
                cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                cutoff_date = cutoff_date.replace(day=cutoff_date.day - days)
                
                filtered_data = []
                for entry in data:
                    entry_date = datetime.fromisoformat(entry['date'].replace('Z', '+00:00'))
                    if entry_date >= cutoff_date:
                        filtered_data.append(entry)
                return filtered_data
            
            return data
        except Exception as e:
            print(f"Error reading writing history: {e}")
            return []
    
    def get_writing_statistics(self) -> Dict[str, Any]:
        """Calculate comprehensive writing statistics.
        
        Returns:
            Dictionary containing various writing metrics
        """
        history = self.get_writing_history(0)  # Get all history
        
        if not history:
            return {
                "total_sessions": 0,
                "total_words_written": 0,
                "average_words_per_session": 0,
                "total_writing_days": 0,
                "current_streak": 0,
                "longest_streak": 0,
                "most_productive_day": None,
                "average_session_duration": 0
            }
        
        # Basic statistics
        total_sessions = len(history)
        total_words_written = sum(entry['word_count'] for entry in history)
        average_words = total_words_written // total_sessions if total_sessions > 0 else 0
        
        # Calculate streaks
        current_streak = self._calculate_current_streak(history)
        longest_streak = self._calculate_longest_streak(history)
        
        # Find most productive day
        most_productive = max(history, key=lambda x: x['word_count']) if history else None
        most_productive_day = {
            "date": most_productive['date'],
            "word_count": most_productive['word_count']
        } if most_productive else None
        
        # Calculate average session duration
        durations = [entry['writing_duration_minutes'] for entry in history 
                    if entry['writing_duration_minutes'] is not None]
        avg_duration = sum(durations) // len(durations) if durations else 0
        
        return {
            "total_sessions": total_sessions,
            "total_words_written": total_words_written,
            "average_words_per_session": average_words,
            "total_writing_days": len(set(entry['date'][:10] for entry in history)),
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "most_productive_day": most_productive_day,
            "average_session_duration": avg_duration
        }
    
    def _calculate_current_streak(self, history: List[Dict[str, Any]]) -> int:
        """Calculate the current consecutive writing streak.
        
        Args:
            history: List of writing session entries
            
        Returns:
            Number of consecutive days with writing sessions
        """
        if not history:
            return 0
        
        # Sort by date (most recent first)
        sorted_history = sorted(history, key=lambda x: x['date'], reverse=True)
        
        streak = 0
        current_date = datetime.now().date()
        
        # Get unique days with writing sessions
        writing_days = set()
        for entry in sorted_history:
            entry_date = datetime.fromisoformat(entry['date'].replace('Z', '+00:00')).date()
            writing_days.add(entry_date)
        
        writing_days = sorted(writing_days, reverse=True)
        
        for day in writing_days:
            if day == current_date or (current_date - day).days == streak:
                streak += 1
                current_date = day
            else:
                break
        
        return streak
    
    def _calculate_longest_streak(self, history: List[Dict[str, Any]]) -> int:
        """Calculate the longest consecutive writing streak.
        
        Args:
            history: List of writing session entries
            
        Returns:
            Longest number of consecutive days with writing sessions
        """
        if not history:
            return 0
        
        # Get unique writing days
        writing_days = set()
        for entry in history:
            entry_date = datetime.fromisoformat(entry['date'].replace('Z', '+00:00')).date()
            writing_days.add(entry_date)
        
        writing_days = sorted(writing_days)
        
        if not writing_days:
            return 0
        
        longest_streak = 1
        current_streak = 1
        
        for i in range(1, len(writing_days)):
            if (writing_days[i] - writing_days[i-1]).days == 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1
        
        return longest_streak
    
    def export_to_csv(self, output_file: str, days: int = 0) -> None:
        """Export writing statistics to a CSV file.
        
        Args:
            output_file: Path to output CSV file
            days: Number of days to export (0 for all)
        """
        history = self.get_writing_history(days)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'date', 'word_count', 'page_summary', 'total_words', 
                'chapter', 'inspiration_sources', 'writing_duration_minutes'
            ])
            
            # Write data
            for entry in history:
                writer.writerow([
                    entry['date'],
                    entry['word_count'],
                    entry['page_summary'],
                    entry['total_words'],
                    entry['chapter'],
                    '; '.join(entry['inspiration_sources']),
                    entry['writing_duration_minutes']
                ])
    
    def get_daily_summary(self, date: Union[str, datetime] = None) -> Optional[Dict[str, Any]]:
        """Get writing summary for a specific date.
        
        Args:
            date: Date to get summary for (defaults to today)
            
        Returns:
            Dictionary containing the day's writing summary or None
        """
        if date is None:
            target_date = datetime.now().date()
        elif isinstance(date, str):
            target_date = datetime.fromisoformat(date).date()
        else:
            target_date = date.date()
        
        history = self.get_writing_history(0)
        
        daily_entries = []
        for entry in history:
            entry_date = datetime.fromisoformat(entry['date'].replace('Z', '+00:00')).date()
            if entry_date == target_date:
                daily_entries.append(entry)
        
        if not daily_entries:
            return None
        
        # Combine multiple sessions on the same day
        total_words = sum(entry['word_count'] for entry in daily_entries)
        summaries = [entry['page_summary'] for entry in daily_entries]
        
        return {
            "date": target_date.isoformat(),
            "total_word_count": total_words,
            "sessions": len(daily_entries),
            "combined_summary": ' | '.join(summaries),
            "entries": daily_entries
        }
