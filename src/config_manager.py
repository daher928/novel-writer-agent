"""
Comprehensive Configuration Manager for Novel Writer Agent

This module provides robust configuration management with:
- Environment variable support
- YAML configuration file loading
- Configuration validation
- Default fallbacks
- Type safety with Pydantic models
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, validator, SecretStr
import logging

logger = logging.getLogger(__name__)

class APIConfig(BaseModel):
    """API configuration settings."""
    openai_api_key: Optional[SecretStr] = Field(None, description="OpenAI API key")
    news_api_key: Optional[SecretStr] = Field(None, description="News API key")
    weather_api_key: Optional[SecretStr] = Field(None, description="Weather API key")
    
    class Config:
        # Allow environment variable loading
        env_prefix = 'NOVEL_WRITER_'

class NovelConfig(BaseModel):
    """Novel-specific configuration settings."""
    title: str = Field("Untitled Novel", description="Title of the novel")
    genre: str = Field("Romance/Fantasy", description="Genre of the novel")
    target_length: int = Field(80000, description="Target word count for the novel")
    voice: str = Field("third-person", description="Narrative voice")
    protagonist_name: str = Field("Alex", description="Main character name")
    
    writing_style: Dict[str, str] = Field(
        default_factory=lambda: {
            "complexity": "moderate",
            "tone": "contemplative", 
            "pacing": "steady"
        },
        description="Writing style parameters"
    )
    
    @validator('target_length')
    def validate_target_length(cls, v):
        if v <= 0:
            raise ValueError('Target length must be positive')
        return v
    
    @validator('voice')
    def validate_voice(cls, v):
        valid_voices = ['first-person', 'second-person', 'third-person']
        if v not in valid_voices:
            raise ValueError(f'Voice must be one of: {", ".join(valid_voices)}')
        return v

class WritingConfig(BaseModel):
    """Writing process configuration."""
    daily_word_target: int = Field(300, description="Target words per day")
    auto_save_interval: int = Field(300, description="Auto-save interval in seconds")
    max_save_versions: int = Field(10, description="Maximum save versions to keep")
    max_backups: int = Field(5, description="Maximum backup files to keep")
    
    # Directory settings
    save_directory: str = Field("saves", description="Directory for save files")
    backup_directory: str = Field("backups", description="Directory for backup files")
    output_directory: str = Field("output", description="Directory for final output files")
    
    @validator('daily_word_target', 'auto_save_interval', 'max_save_versions', 'max_backups')
    def validate_positive_integers(cls, v):
        if v <= 0:
            raise ValueError('Value must be positive')
        return v

class AnalysisConfig(BaseModel):
    """News and mood analysis configuration."""
    enable_news_analysis: bool = Field(True, description="Enable news analysis for inspiration")
    enable_mood_analysis: bool = Field(True, description="Enable mood/weather analysis")
    enable_sentiment_analysis: bool = Field(True, description="Enable sentiment analysis")
    
    # News sources and filtering
    news_sources: List[str] = Field(
        default_factory=lambda: ["general", "technology", "arts"],
        description="News categories to analyze"
    )
    news_language: str = Field("en", description="Language for news analysis")
    news_country: str = Field("us", description="Country for news analysis")
    
    # Analysis frequency
    analysis_frequency_hours: int = Field(24, description="How often to refresh analysis (hours)")
    
    @validator('analysis_frequency_hours')
    def validate_analysis_frequency(cls, v):
        if v <= 0 or v > 168:  # Max 1 week
            raise ValueError('Analysis frequency must be between 1 and 168 hours')
        return v

class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = Field("INFO", description="Logging level")
    format: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    file_enabled: bool = Field(True, description="Enable file logging")
    file_path: str = Field("logs/novel_writer.log", description="Log file path")
    console_enabled: bool = Field(True, description="Enable console logging")
    
    @validator('level')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Log level must be one of: {", ".join(valid_levels)}')
        return v.upper()

class AppConfig(BaseModel):
    """Main application configuration."""
    api: APIConfig = Field(default_factory=APIConfig)
    novel: NovelConfig = Field(default_factory=NovelConfig)
    writing: WritingConfig = Field(default_factory=WritingConfig)
    analysis: AnalysisConfig = Field(default_factory=AnalysisConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
    # Environment
    environment: str = Field("development", description="Environment: development, production, testing")
    debug: bool = Field(False, description="Enable debug mode")
    
    @validator('environment')
    def validate_environment(cls, v):
        valid_envs = ['development', 'production', 'testing']
        if v not in valid_envs:
            raise ValueError(f'Environment must be one of: {", ".join(valid_envs)}')
        return v

class ConfigManager:
    """
    Comprehensive configuration manager that handles loading from multiple sources.
    
    Priority order (highest to lowest):
    1. Environment variables
    2. YAML configuration file
    3. Default values
    """
    
    def __init__(self, config_file: Optional[Union[str, Path]] = None, 
                 env_prefix: str = "NOVEL_WRITER_"):
        """
        Initialize the configuration manager.
        
        Args:
            config_file: Path to YAML configuration file
            env_prefix: Prefix for environment variables
        """
        self.config_file = Path(config_file) if config_file else None
        self.env_prefix = env_prefix
        self._config: Optional[AppConfig] = None
        
    def load_config(self) -> AppConfig:
        """
        Load configuration from all sources with proper precedence.
        
        Returns:
            AppConfig: Loaded and validated configuration
            
        Raises:
            ValidationError: If configuration validation fails
            FileNotFoundError: If specified config file doesn't exist
        """
        if self._config is not None:
            return self._config
            
        # Start with defaults
        config_data = {}
        
        # Load from YAML file if provided
        if self.config_file and self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    yaml_data = yaml.safe_load(f)
                    if yaml_data:
                        config_data.update(yaml_data)
                logger.info(f"Loaded configuration from {self.config_file}")
            except Exception as e:
                logger.error(f"Failed to load config file {self.config_file}: {e}")
                raise
        
        # Override with environment variables
        self._load_from_env(config_data)
        
        # Create and validate configuration
        try:
            self._config = AppConfig(**config_data)
            logger.info("Configuration loaded and validated successfully")
            return self._config
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            raise
    
    def _load_from_env(self, config_data: Dict[str, Any]) -> None:
        """
        Load configuration from environment variables.
        
        Args:
            config_data: Configuration dictionary to update
        """
        # API keys
        if os.getenv(f"{self.env_prefix}OPENAI_API_KEY"):
            config_data.setdefault("api", {})["openai_api_key"] = os.getenv(f"{self.env_prefix}OPENAI_API_KEY")
        
        if os.getenv(f"{self.env_prefix}NEWS_API_KEY"):
            config_data.setdefault("api", {})["news_api_key"] = os.getenv(f"{self.env_prefix}NEWS_API_KEY")
            
        if os.getenv(f"{self.env_prefix}WEATHER_API_KEY"):
            config_data.setdefault("api", {})["weather_api_key"] = os.getenv(f"{self.env_prefix}WEATHER_API_KEY")
        
        # Novel settings
        if os.getenv(f"{self.env_prefix}NOVEL_TITLE"):
            config_data.setdefault("novel", {})["title"] = os.getenv(f"{self.env_prefix}NOVEL_TITLE")
            
        if os.getenv(f"{self.env_prefix}NOVEL_GENRE"):
            config_data.setdefault("novel", {})["genre"] = os.getenv(f"{self.env_prefix}NOVEL_GENRE")
        
        # Environment
        if os.getenv(f"{self.env_prefix}ENVIRONMENT"):
            config_data["environment"] = os.getenv(f"{self.env_prefix}ENVIRONMENT")
            
        if os.getenv(f"{self.env_prefix}DEBUG"):
            config_data["debug"] = os.getenv(f"{self.env_prefix}DEBUG").lower() in ('true', '1', 'yes')
    
    def get_config(self) -> AppConfig:
        """
        Get the current configuration, loading it if necessary.
        
        Returns:
            AppConfig: Current configuration
        """
        if self._config is None:
            return self.load_config()
        return self._config
    
    def reload_config(self) -> AppConfig:
        """
        Force reload of configuration from all sources.
        
        Returns:
            AppConfig: Reloaded configuration
        """
        self._config = None
        return self.load_config()
    
    def save_config_template(self, output_path: Union[str, Path]) -> None:
        """
        Save a configuration template file with all available options.
        
        Args:
            output_path: Path where to save the template
        """
        template_config = AppConfig()
        config_dict = template_config.dict()
        
        # Remove sensitive data from template
        if 'api' in config_dict:
            for key in config_dict['api']:
                if 'key' in key:
                    config_dict['api'][key] = "your_api_key_here"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_dict, f, default_flow_style=False, 
                     allow_unicode=True, indent=2)
        
        logger.info(f"Configuration template saved to {output_path}")
    
    def validate_api_keys(self) -> Dict[str, bool]:
        """
        Check which API keys are configured and valid.
        
        Returns:
            Dict mapping API names to their availability status
        """
        config = self.get_config()
        
        validation_results = {
            'openai': bool(config.api.openai_api_key),
            'news': bool(config.api.news_api_key),
            'weather': bool(config.api.weather_api_key)
        }
        
        return validation_results

# Global configuration instance
_config_manager: Optional[ConfigManager] = None

def get_config_manager(config_file: Optional[Union[str, Path]] = None) -> ConfigManager:
    """
    Get the global configuration manager instance.
    
    Args:
        config_file: Path to configuration file (only used on first call)
        
    Returns:
        ConfigManager: Global configuration manager
    """
    global _config_manager
    
    if _config_manager is None:
        _config_manager = ConfigManager(config_file)
    
    return _config_manager

def get_config(config_file: Optional[Union[str, Path]] = None) -> AppConfig:
    """
    Convenience function to get the current configuration.
    
    Args:
        config_file: Path to configuration file (only used on first call)
        
    Returns:
        AppConfig: Current application configuration
    """
    return get_config_manager(config_file).get_config()
