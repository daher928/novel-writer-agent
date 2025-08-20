# Novel Writer Agent

An autonomous AI agent that writes one page of a novel daily, inspired by real-world factors like mood, world news, and authentic writer influences. This agent creates compelling fiction by analyzing current events, emotional patterns, and literary styles to produce consistent, engaging narrative content.

## Overview

The Novel Writer Agent is a creative AI system that functions as an autonomous book author, crafting original fiction with daily consistency. It draws inspiration from multiple real-world sources to create authentic, emotionally resonant storytelling that evolves with current events and human experiences.

## Key Features

- **📚 Daily Writing**: Automatically generates one page of novel content every day
- **🌍 World News Integration**: Incorporates current events and global happenings into narrative themes
- **😊 Mood Analysis**: Adapts writing style and tone based on emotional and atmospheric factors
- **✍️ Writer Inspiration**: Emulates authentic writer behaviors, routines, and creative processes
- **📖 Narrative Consistency**: Maintains character development and plot coherence across daily entries
- **🎨 Style Adaptation**: Evolves writing style based on genre, mood, and thematic requirements
- **💾 Auto-Save**: Automatically saves story drafts with versioning and backup functionality

## Auto-Save System

The Novel Writer Agent includes a robust auto-save system that ensures your creative work is never lost:

### Features
- **Automatic Versioning**: Every save creates a timestamped version for easy recovery
- **Smart Backup**: Creates backups with configurable retention policies
- **Word Count Tracking**: Monitors progress with built-in word counting
- **Metadata Storage**: Saves additional information like timestamps and version numbers
- **Recovery Options**: Load previous saves or access save history

### Usage

```python
from src.auto_save import AutoSave

# Initialize auto-save system
autosave = AutoSave(save_directory="saves", backup_directory="backups")

# Save story draft
story_data = {
    "content": "Your story content here...",
    "characters": ["Character 1", "Character 2"],
    "plot_points": ["Plot point 1", "Plot point 2"]
}

save_path = autosave.save_story_draft(story_data)
print(f"Story saved to: {save_path}")

# Create manual backup
backup_path = autosave.create_backup(story_data)
print(f"Backup created: {backup_path}")

# Load latest save
latest_story = autosave.load_latest_save()
if latest_story:
    print(f"Loaded story with {autosave._calculate_word_count(latest_story)} words")

# View save history
history = autosave.get_save_history()
for save in history:
    print(f"Version {save['version']}: {save['word_count']} words ({save['timestamp']})")
```

### Configuration

The auto-save system can be customized:

- `save_directory`: Directory for regular saves (default: "saves")
- `backup_directory`: Directory for backup files (default: "backups")
- `save_interval`: Time between auto-saves in seconds (default: 300)
- `max_versions`: Maximum number of versions to keep (default: 10)
- `max_backups`: Maximum number of backups to keep (default: 5)

## How It Works

The agent operates on a daily cycle:

1. **Morning Analysis**: Scans world news, weather, and cultural events
2. **Mood Assessment**: Analyzes current emotional and atmospheric conditions
3. **Creative Synthesis**: Combines real-world inputs with ongoing narrative threads
4. **Daily Writing**: Generates one page (~250-300 words) of novel content
5. **Story Continuity**: Updates character arcs and plot progression
6. **Archive & Reflect**: Saves the day's work and prepares for tomorrow's inspiration
7. **Auto-Save**: Automatically saves progress with versioning and backup

## Installation

### Prerequisites

- Python 3.9+
- OpenAI API key or other LLM provider
- News API access (for world events)
- Weather API access (for atmospheric inspiration)

### Setup

```bash
# Clone the repository
git clone https://github.com/daher928/novel-writer-agent.git
cd novel-writer-agent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and configuration
```
