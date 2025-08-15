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

## How It Works

The agent operates on a daily cycle:

1. **Morning Analysis**: Scans world news, weather, and cultural events
2. **Mood Assessment**: Analyzes current emotional and atmospheric conditions
3. **Creative Synthesis**: Combines real-world inputs with ongoing narrative threads
4. **Daily Writing**: Generates one page (~250-300 words) of novel content
5. **Story Continuity**: Updates character arcs and plot progression
6. **Archive & Reflect**: Saves the day's work and prepares for tomorrow's inspiration

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

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| OPENAI_API_KEY | OpenAI API key for text generation | Yes |
| NEWS_API_KEY | News API key for current events | Yes |
| WEATHER_API_KEY | Weather API key for atmospheric data | No |
| WRITING_TIME | Daily writing time (default: 09:00) | No |
| TARGET_WORDS | Target words per page (default: 300) | No |

### Novel Settings

```yaml
# config/novel.yaml
novel:
  title: "Your Novel Title"
  genre: "literary fiction"  # or mystery, romance, sci-fi, etc.
  target_length: 80000  # target word count
  voice: "third-person"  # or first-person
  
characters:
  protagonist:
    name: "Main Character"
    age: 30
    background: "Character background"
    
writing_style:
  complexity: "moderate"  # simple, moderate, complex
  tone: "contemplative"   # humorous, dark, light, contemplative
  pacing: "steady"        # fast, steady, slow
```

## Quick Start

```python
from novel_agent import NovelWriterAgent

# Initialize the agent
writer = NovelWriterAgent(
    novel_config="config/novel.yaml",
    api_keys={
        "openai": "your-openai-key",
        "news": "your-news-api-key"
    }
)

# Generate today's page
today_page = writer.write_daily_page()
print(today_page.content)

# Get writing statistics
stats = writer.get_progress_stats()
print(f"Total pages: {stats.total_pages}")
print(f"Total words: {stats.total_words}")
```

## Daily Writing Process

The agent follows a sophisticated creative process:

### 1. Environmental Scanning
- Analyzes current news headlines
- Checks weather and atmospheric conditions
- Reviews cultural events and trends
- Assesses general mood indicators

### 2. Creative Integration
- Maps real-world events to narrative themes
- Identifies emotional undertones
- Selects appropriate writing mood and style
- Plans character reactions and developments

### 3. Content Generation
- Writes one cohesive page of fiction
- Maintains continuity with previous pages
- Incorporates daily inspirations subtly
- Ensures character voice consistency

### 4. Quality Assurance
- Reviews for narrative coherence
- Checks character consistency
- Validates emotional authenticity
- Ensures appropriate pacing

## Features in Detail

### News Integration
The agent doesn't simply copy news events but transforms them into:
- Character motivations and conflicts
- Background atmospheric details
- Subtle thematic elements
- Emotional undertones and tensions

### Mood Analysis
Daily mood assessment considers:
- Weather patterns and seasonal changes
- Global news sentiment
- Cultural events and celebrations
- Historical significance of the date

### Writer Authenticity
Emulates real writer behaviors:
- Morning coffee ritual simulation
- Writer's block handling
- Creative breakthrough moments
- Editing and revision processes

## Monitoring & Analytics

### Writing Statistics
- Daily word count tracking
- Character development metrics
- Plot progression analysis
- Style consistency measurements

### Quality Metrics
- Narrative coherence scores
- Character voice consistency
- Emotional authenticity ratings
- Reader engagement predictions

## Customization

### Custom Writing Prompts
```python
# Add custom inspiration sources
writer.add_inspiration_source("daily_quotes")
writer.add_inspiration_source("historical_events")

# Customize writing style
writer.set_style_preference("minimalist")
writer.set_emotional_range("melancholic_to_hopeful")
```

### Genre-Specific Modules
- Mystery: Crime news integration, red herrings
- Romance: Relationship dynamics, emotional beats
- Sci-Fi: Technology trends, scientific discoveries
- Fantasy: Mythological themes, archetypal patterns

## Deployment

### Automated Daily Writing
```bash
# Set up daily cron job
0 9 * * * cd /path/to/novel-writer-agent && python daily_write.py
```

### Cloud Deployment
- Docker containerization included
- AWS Lambda functions for serverless operation
- Google Cloud Functions support
- Azure Functions compatibility

## Example Output

*Page 1 - Written on a rainy Tuesday during international tensions:*

> The rain drummed against Margaret's window with an urgency that matched her heartbeat. She hadn't slept well—few had, given the morning's news from across the ocean. The world felt smaller somehow, more fragile, as if the threads holding everything together had grown thin overnight.
> 
> She pulled her shawl tighter and moved to the kitchen, where the familiar ritual of coffee promised a anchor in the shifting day. The beans were from a small farm in Colombia, a detail that once seemed romantic but now carried weight—how many hands had touched them, how many lives intersected in this simple morning pleasure?
> 
> Outside, the city stirred with its usual determination, people hurrying to work despite the weather, despite the uncertainty that seemed to hang in the air like humidity. Margaret watched them from her third-floor window, each figure a story moving through the rain...

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/creative-enhancement`)
3. Commit your changes (`git commit -m 'Add new inspiration source'`)
4. Push to the branch (`git push origin feature/creative-enhancement`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **OpenAI** - For GPT models that enable creative writing
- **News API** - For real-world event integration
- **The writing community** - For inspiration on authentic creative processes
- **Daily writers everywhere** - Who prove that consistency creates magic

## Support

For questions, suggestions, or to share your novel's progress:
- [GitHub Issues](https://github.com/daher928/novel-writer-agent/issues)
- [Discussions](https://github.com/daher928/novel-writer-agent/discussions)

---

*"Every day brings new inspiration. Every page brings us closer to the story only we can tell."*

Built with ❤️ for writers, dreamers, and the stories that need to be told.
