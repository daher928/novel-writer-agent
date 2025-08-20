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
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutoSave:
    """
    Handles automatic saving of story drafts with versioning and backup capabilities.
    """
    
    def __init__(self, save_directory: str = "saves", backup_directory: str = "backups"):
        """
        Initialize the AutoSave system.
        
        Args:
            save_directory: Directory for regular saves
            backup_directory: Directory for backup files
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
    
    def save_story_draft(self, story_data: Dict, filename: Optional[str] = None) -> str:
        """
        Save a story draft with automatic versioning.
        
        Args:
            story_data: Dictionary containing story content and metadata
            filename: Optional custom filename
            
        Returns:
            Path to the saved file
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
    
    def create_backup(self, story_data: Dict) -> str:
        """
        Create a backup of the current story state.
        
        Args:
            story_data: Dictionary containing story content and metadata
            
        Returns:
            Path to the backup file
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
    
    def load_latest_save(self) -> Optional[Dict]:
        """
        Load the most recent save file.
        
        Returns:
            Dictionary containing story data, or None if no saves exist
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
    
    def get_save_history(self) -> List[Dict]:
        """
        Get a list of all available save files with metadata.
        
        Returns:
            List of dictionaries containing save file information
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
    
    def _calculate_word_count(self, story_data: Dict) -> int:
        """
        Calculate total word count from story data.
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
    
    def _cleanup_old_versions(self):
        """
        Remove old save versions beyond the maximum limit.
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
                    logger.error(f"Failed to remove old save file {old_file}: {e}")
    
    def _cleanup_old_backups(self):
        """
        Remove old backup files beyond the maximum limit.
        """
        backup_files = list(self.backup_dir.glob("backup_*.json"))
        
        if len(backup_files) > self.max_backups:
            # Sort by modification time (oldest first)
            backup_files.sort(key=lambda x: x.stat().st_mtime)
            
            # Remove oldest backups
            for old_backup in backup_files[:-self.max_backups]:
                try:
                    old_backup.unlink()
                    logger.info(f"Removed old backup file: {old_backup}")
                except Exception as e:
                    logger.error(f"Failed to remove old backup file {old_backup}: {e}")
