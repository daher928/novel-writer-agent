"""Daily Writer Module

This module contains utilities and classes for daily novel writing operations,
including scheduling, content management, and integration with external services.
"""

import asyncio
import logging
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path

from .agent import NovelWriterAgent


class DailyWriter:
    """Daily writing scheduler and manager for the Novel Writer Agent.
    
    This class handles the daily execution of writing tasks, manages scheduling,
    and provides utilities for consistent daily novel generation.
    """
    
    def __init__(self, agent: NovelWriterAgent, output_dir: str = "./output"):
        """Initialize the Daily Writer.
        
        Args:
            agent: The NovelWriterAgent instance to use for writing
            output_dir: Directory to save daily writing output
        """
        self.agent = agent
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Set up logging
        self.logger = self._setup_logging()
        
        # Writing schedule configuration
        self.writing_time = "09:00"  # Default 9 AM
        self.is_scheduled = False
        
        # Callbacks for events
        self.on_write_complete: Optional[Callable] = None
        self.on_write_error: Optional[Callable] = None
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for daily writing operations.
        
        Returns:
            logging.Logger: Configured logger instance
        """
        logger = logging.getLogger('daily_writer')
        logger.setLevel(logging.INFO)
        
        # Create file handler
        log_file = self.output_dir / 'daily_writer.log'
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        if not logger.handlers:
            logger.addHandler(handler)
        
        return logger
    
    def schedule_daily_writing(self, time_str: str = "09:00") -> None:
        """Schedule daily writing at a specific time.
        
        Args:
            time_str: Time in HH:MM format (24-hour) to schedule writing
        """
        self.writing_time = time_str
        
        # Clear existing schedule
        schedule.clear()
        
        # Schedule daily writing
        schedule.every().day.at(time_str).do(self._execute_daily_writing)
        
        self.is_scheduled = True
        self.logger.info(f"Daily writing scheduled for {time_str}")
    
    def _execute_daily_writing(self) -> Dict[str, Any]:
        """Execute the daily writing task.
        
        Returns:
            Dict containing writing results and metadata
        """
        try:
            self.logger.info("Starting daily writing session")
            
            # Generate today's page
            result = self.agent.write_daily_page()
            
            # Save the output
            self._save_daily_output(result)
            
            # Update progress
            self.agent.save_progress()
            
            self.logger.info(
                f"Daily writing completed successfully. "
                f"Words written: {result['word_count']}"
            )
            
            # Call completion callback if set
            if self.on_write_complete:
                self.on_write_complete(result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Daily writing failed: {str(e)}")
            
            # Call error callback if set
            if self.on_write_error:
                self.on_write_error(e)
            
            raise
    
    def _save_daily_output(self, result: Dict[str, Any]) -> None:
        """Save daily writing output to files.
        
        Args:
            result: Writing result from the agent
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Save the content
        content_file = self.output_dir / f"{date_str}_page.txt"
        with open(content_file, 'w', encoding='utf-8') as f:
            f.write(result['content'])
        
        # Save metadata
        import json
        metadata_file = self.output_dir / f"{date_str}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        
        self.logger.info(f"Daily output saved to {content_file}")
    
    def run_scheduled_writer(self) -> None:
        """Run the scheduled writer in a loop.
        
        This method starts the scheduling system and runs indefinitely,
        executing writing tasks at the scheduled times.
        """
        if not self.is_scheduled:
            self.schedule_daily_writing()
        
        self.logger.info("Starting scheduled writer loop")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("Scheduled writer stopped by user")
        except Exception as e:
            self.logger.error(f"Scheduled writer error: {str(e)}")
            raise
    
    def write_now(self) -> Dict[str, Any]:
        """Execute writing immediately, regardless of schedule.
        
        Returns:
            Dict containing writing results and metadata
        """
        self.logger.info("Manual writing session triggered")
        return self._execute_daily_writing()
    
    def get_writing_history(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get writing history for the past N days.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of writing sessions with metadata
        """
        history = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            
            metadata_file = self.output_dir / f"{date_str}_metadata.json"
            
            if metadata_file.exists():
                import json
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    history.append(data)
        
        return history
    
    def get_writing_stats(self) -> Dict[str, Any]:
        """Get comprehensive writing statistics.
        
        Returns:
            Dict containing various writing metrics and statistics
        """
        history = self.get_writing_history(30)  # Last 30 days
        
        if not history:
            return {
                "total_days": 0,
                "total_words": 0,
                "average_words_per_day": 0,
                "streak_days": 0,
                "last_writing_date": None
            }
        
        total_words = sum(session['word_count'] for session in history)
        total_days = len(history)
        average_words = total_words // total_days if total_days > 0 else 0
        
        # Calculate current streak
        streak_days = self._calculate_writing_streak()
        
        return {
            "total_days": total_days,
            "total_words": total_words,
            "average_words_per_day": average_words,
            "streak_days": streak_days,
            "last_writing_date": history[0]['date'] if history else None,
            "progress_stats": self.agent.get_progress_stats()
        }
    
    def _calculate_writing_streak(self) -> int:
        """Calculate current consecutive writing streak.
        
        Returns:
            int: Number of consecutive days with writing
        """
        streak = 0
        current_date = datetime.now()
        
        while True:
            date_str = current_date.strftime("%Y-%m-%d")
            metadata_file = self.output_dir / f"{date_str}_metadata.json"
            
            if metadata_file.exists():
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        return streak
    
    async def async_write_daily_page(self) -> Dict[str, Any]:
        """Asynchronous version of daily writing for integration with async systems.
        
        Returns:
            Dict containing writing results and metadata
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._execute_daily_writing)
    
    def backup_progress(self, backup_dir: str = "./backups") -> None:
        """Create a backup of all writing progress and data.
        
        Args:
            backup_dir: Directory to store backups
        """
        backup_path = Path(backup_dir)
        backup_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_path / f"novel_backup_{timestamp}.zip"
        
        import zipfile
        
        with zipfile.ZipFile(backup_file, 'w') as zipf:
            # Backup output directory
            for file_path in self.output_dir.rglob('*'):
                if file_path.is_file():
                    zipf.write(file_path, file_path.relative_to(self.output_dir.parent))
            
            # Backup progress file if it exists
            progress_file = Path("novel_progress.json")
            if progress_file.exists():
                zipf.write(progress_file, progress_file.name)
        
        self.logger.info(f"Backup created: {backup_file}")
    
    def set_callbacks(self, 
                     on_complete: Optional[Callable] = None,
                     on_error: Optional[Callable] = None) -> None:
        """Set callback functions for writing events.
        
        Args:
            on_complete: Function to call when writing completes successfully
            on_error: Function to call when writing encounters an error
        """
        self.on_write_complete = on_complete
        self.on_write_error = on_error


# Utility functions for standalone usage
def quick_daily_write(config_file: Optional[str] = None) -> Dict[str, Any]:
    """Quick function to perform a daily write with minimal setup.
    
    Args:
        config_file: Optional path to configuration file
        
    Returns:
        Dict containing writing results
    """
    agent = NovelWriterAgent(config_file=config_file)
    writer = DailyWriter(agent)
    return writer.write_now()


def setup_daily_schedule(writing_time: str = "09:00", 
                        config_file: Optional[str] = None) -> DailyWriter:
    """Set up and return a configured daily writer with scheduling.
    
    Args:
        writing_time: Time to schedule daily writing (HH:MM format)
        config_file: Optional path to configuration file
        
    Returns:
        DailyWriter: Configured writer instance
    """
    agent = NovelWriterAgent(config_file=config_file)
    writer = DailyWriter(agent)
    writer.schedule_daily_writing(writing_time)
    return writer
