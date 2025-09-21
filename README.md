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

## Example Daily Output

### Sample Generated Content

Here's an example of what the Novel Writer Agent produces on a typical day:

**Chapter 3: Echoes of Tomorrow**

*Generated on September 8, 2025*

*Inspired by: Global climate summit, autumn weather patterns*

Margaret stood at the edge of the research facility's observation deck, watching the automated weather sensors dance in the crisp September wind. The morning news had been filled with discussions from the climate summit in Geneva, and somehow those distant political voices seemed to whisper through the changing leaves outside her window.

"The data doesn't lie," she murmured to herself, reviewing the overnight readings on her tablet. The atmospheric composition readings showed subtle shifts that aligned disturbingly well with the predictions she'd been modeling for months. Each data point felt like a piece of a vast puzzle, one that humanity was still struggling to solve.

Dr. Chen appeared beside her, steam rising from his coffee cup in the cool morning air. "The algorithms picked up something interesting overnight," he said, his voice carrying that familiar mix of excitement and concern that had become their daily soundtrack.

Margaret turned to face him, noting how the early light caught the worry lines around his eyes. The weight of their research—understanding patterns that could reshape how humanity approached the future—seemed to age them all a little more each day. But there was something else in his expression today, a spark that suggested discovery.

"Show me," she said, following him back toward the lab where screens full of data waited to tell their story.

---

*Word Count: 287*

*Characters Developed: Margaret (protagonist), Dr. Chen (colleague)*

*Themes: Environmental consciousness, scientific discovery, human connection*

*Next Day's Focus: The discovery in the lab data*

### CLI Usage

Run the agent with typical arguments:

```bash
# Generate today's page with standard settings
python cli.py --generate-daily --mood-analysis --news-integration

# Run with specific genre and word count target
python cli.py --generate-daily --genre sci-fi --target-words 300 --mood-analysis

# Generate and auto-save with backup
python cli.py --generate-daily --auto-save --create-backup --save-dir "my_novel"

# Check progress and statistics
python cli.py --show-stats --recent-history 7

# Generate with custom inspiration sources
python cli.py --generate-daily --news-sources "technology,science" --weather-location "New York"
```

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Author**: Daher Daher ([@daher928](https://github.com/daher928))
- **Email**: daher.1995@gmail.com
- **Project Link**: https://github.com/daher928/novel-writer-agent
