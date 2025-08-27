"""
Auto-save functionality for Novel Writer Agent
This module provides automated saving of story drafts with versioning,
backup functionality, and recovery capabilities.
"""
import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutoSave:
    """
    Handles automatic saving of story drafts with versioning and backup capabilities.
    
    This class provides comprehensive auto-save functionality including:
    - Automatic versioning of story drafts
    - Backup creation and management
    - Save history tracking
    - Cleanup of old files
    - Word count calculation
    - Recovery capabilities
    
    Attributes:
        save_dir (Path): Directory for regular save files
        backup_dir (Path): Directory for backup files
        save_interval (int): Auto-save interval in seconds
        max_versions (int): Maximum number of save versions to keep
        max_backups (int): Maximum number of backup files to keep
    """
    
    def __init__(self, save_directory: str = "saves", backup_directory: str = "backups") -> None:
        """
        Initialize the AutoSave system.
        
        Sets up the save and backup directories, creates them if they don't exist,
        and configures default settings for auto-saving behavior.
        
        Args:
            save_directory (str, optional): Directory for regular saves. Defaults to "saves".
            backup_directory (str, optional): Directory for backup files. Defaults to "backups".
            
        Raises:
            OSError: If directories cannot be created due to permission issues.
        """
        self.save_dir = Path(save_directory)
        self.backup_dir = Path(backup_directory)
        self.save_interval = 300  # 5 minutes in seconds
        self.max_versions = 10
        self.max_backups = 5
        
        # Create directories if they don't exist
        self.save_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        
        logger.info(f"AutoSave initialized with save_dir: {self.save_dir}, backup_dir: {self.backup_dir}")
    
    def save_story_draft(self, story_data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Save a story draft with automatic versioning.
        
        Creates a timestamped save file with metadata including version number,
        word count, and save timestamp. Automatically manages old versions
        by cleaning up files beyond the maximum limit.
        
        Args:
            story_data (Dict[str, Any]): Dictionary containing story content and metadata.
                Expected to contain keys like 'content', 'pages', etc.
            filename (Optional[str], optional): Custom filename for the save file.
                If None, generates timestamp-based filename. Defaults to None.
                
        Returns:
            str: Full path to the saved file.
            
        Raises:
            IOError: If the file cannot be written due to permission or disk space issues.
            json.JSONEncodeError: If the story_data cannot be serialized to JSON.
            
        Example:
            >>> auto_save = AutoSave()
            >>> story = {'content': 'Once upon a time...', 'title': 'My Story'}
            >>> path = auto_save.save_story_draft(story)
            >>> print(f"Story saved to: {path}")
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"story_draft_{timestamp}.json"
        
        # Add save metadata
        story_data['save_metadata'] = {
            'timestamp': datetime.now().isoformat(),
            'version': self._get_next_version(filename),
            'word_count': self._calculate_word_count(story_data),
            'auto_saved': True
        }
        
        # Save to main directory
        save_path = self.save_dir / filename
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(story_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Story draft saved: {save_path}")
        
        # Clean up old versions
        self._cleanup_old_versions()
        
        return str(save_path)
    
    def create_backup(self, story_data: Dict[str, Any]) -> str:
        """
        Create a backup of the current story state.
        
        Creates a timestamped backup file in the backup directory with metadata
        including timestamp, word count, and backup type. Automatically manages
        old backups by cleaning up files beyond the maximum limit.
        
        Args:
            story_data (Dict[str, Any]): Dictionary containing story content and metadata
                to be backed up.
                
        Returns:
            str: Full path to the created backup file.
            
        Raises:
            IOError: If the backup file cannot be written due to permission or disk space issues.
            json.JSONEncodeError: If the story_data cannot be serialized to JSON.
            
        Example:
            >>> auto_save = AutoSave()
            >>> story = {'content': 'Important story content...', 'title': 'My Novel'}
            >>> backup_path = auto_save.create_backup(story)
            >>> print(f"Backup created at: {backup_path}")
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{timestamp}.json"
        
        # Add backup metadata
        story_data['backup_metadata'] = {
            'timestamp': datetime.now().isoformat(),
            'word_count': self._calculate_word_count(story_data),
            'backup_type': 'manual'
        }
        
        backup_path = self.backup_dir / backup_filename
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(story_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Backup created: {backup_path}")
        
        # Clean up old backups
        self._cleanup_old_backups()
        
        return str(backup_path)
    
    def load_latest_save(self) -> Optional[Dict[str, Any]]:
        """
        Load the most recent save file.
        
        Searches the save directory for story draft files and loads the most
        recently modified one. Returns None if no save files are found or if
        the latest file cannot be loaded.
        
        Returns:
            Optional[Dict[str, Any]]: Dictionary containing story data from the latest save,
                or None if no saves exist or loading fails.
                
        Raises:
            json.JSONDecodeError: If the save file contains invalid JSON (logged as error).
            IOError: If the file cannot be read (logged as error).
            
        Example:
            >>> auto_save = AutoSave()
            >>> latest_story = auto_save.load_latest_save()
            >>> if latest_story:
            ...     print(f"Loaded story: {latest_story.get('title', 'Untitled')}")
            ... else:
            ...     print("No saved stories found")
        """
        save_files = list(self.save_dir.glob("story_draft_*.json"))
        
        if not save_files:
            logger.warning("No save files found")
            return None
        
        # Sort by modification time (newest first)
        latest_save = max(save_files, key=lambda x: x.stat().st_mtime)
        
        try:
            with open(latest_save, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"Loaded latest save: {latest_save}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load save file {latest_save}: {e}")
            return None
    
    def get_save_history(self) -> List[Dict[str, Union[str, int, None]]]:
        """
        Get a list of all available save files with metadata.
        
        Scans the save directory for all story draft files and extracts metadata
        from each file including timestamp, version, word count, and file size.
        Returns a sorted list with the newest saves first.
        
        Returns:
            List[Dict[str, Union[str, int, None]]]: List of dictionaries containing save file information.
                Each dictionary contains:
                - filename (str): Name of the save file
                - path (str): Full path to the save file
                - timestamp (str): ISO timestamp of when the save was created
                - version (int): Version number of the save
                - word_count (int): Word count at time of save
                - size_bytes (int): File size in bytes
                
        Example:
            >>> auto_save = AutoSave()
            >>> history = auto_save.get_save_history()
            >>> for save in history:
            ...     print(f"{save['filename']}: {save['word_count']} words")
        """
        save_files = list(self.save_dir.glob("story_draft_*.json"))
        history = []
        
        for save_file in save_files:
            try:
                with open(save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                metadata = data.get('save_metadata', {})
                history.append({
                    'filename': save_file.name,
                    'path': str(save_file),
                    'timestamp': metadata.get('timestamp'),
                    'version': metadata.get('version'),
                    'word_count': metadata.get('word_count', 0),
                    'size_bytes': save_file.stat().st_size
                })
                
            except Exception as e:
                logger.warning(f"Failed to read save file {save_file}: {e}")
        
        # Sort by timestamp (newest first)
        history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return history
    
    def _get_next_version(self, base_filename: str) -> int:
        """
        Get the next version number for a save file.
        
        Scans existing save files to find the highest version number currently
        in use and returns the next sequential version number.
        
        Args:
            base_filename (str): Base filename for the save (currently unused but kept
                for potential future filename-specific versioning).
                
        Returns:
            int: Next available version number (starts from 1 if no versions exist).
            
        Note:
            This method scans all save files regardless of the base_filename parameter.
            Version numbers are global across all save files in the directory.
        """
        save_files = list(self.save_dir.glob("story_draft_*.json"))
        versions = []
        
        for save_file in save_files:
            try:
                with open(save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                metadata = data.get('save_metadata', {})
                if 'version' in metadata:
                    versions.append(metadata['version'])
            except Exception:
                continue
        
        return max(versions, default=0) + 1
    
    def _calculate_word_count(self, story_data: Dict[str, Any]) -> int:
        """
        Calculate total word count from story data.
        
        Analyzes the story data structure to count words across different content
        fields including 'content' and 'pages'. Handles various data structures
        including strings, lists, and nested dictionaries.
        
        Args:
            story_data (Dict[str, Any]): Dictionary containing story content to analyze.
                Expected to potentially contain 'content' and/or 'pages' keys.
                
        Returns:
            int: Total word count across all content in the story data.
            
        Note:
            Word counting is performed by splitting text on whitespace, so the count
            may not be exact for all text formatting scenarios but provides a good
            approximation for tracking writing progress.
        """
        word_count = 0
        
        # Count words in content fields
        if 'content' in story_data:
            if isinstance(story_data['content'], str):
                word_count += len(story_data['content'].split())
            elif isinstance(story_data['content'], list):
                for item in story_data['content']:
                    if isinstance(item, str):
                        word_count += len(item.split())
        
        # Count words in pages if present
        if 'pages' in story_data:
            for page in story_data['pages']:
                if isinstance(page, dict) and 'content' in page:
                    word_count += len(str(page['content']).split())
                elif isinstance(page, str):
                    word_count += len(page.split())
        
        return word_count
    
    def _cleanup_old_versions(self) -> None:
        """
        Remove old save versions beyond the maximum limit.
        
        Scans the save directory for story draft files and removes the oldest
        files when the total count exceeds max_versions. Files are identified
        by modification time, with the oldest files being removed first.
        
        Raises:
            OSError: If old files cannot be deleted due to permission issues
                (logged as error but does not stop execution).
                
        Note:
            This method is called automatically after each save operation to
            maintain the configured maximum number of save versions.
        """
        save_files = list(self.save_dir.glob("story_draft_*.json"))
        
        if len(save_files) > self.max_versions:
            # Sort by modification time (oldest first)
            save_files.sort(key=lambda x: x.stat().st_mtime)
            
            # Remove oldest files
            for old_file in save_files[:-self.max_versions]:
                try:
                    old_file.unlink()
                    logger.info(f"Removed old save file: {old_file}")
                except Exception as e:
                    logger.error(f"Failed to remove
