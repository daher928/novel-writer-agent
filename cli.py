#!/usr/bin/env python3
"""
CLI Utility for Novel Writer Agent

Provides command-line interface for showing progress and recent save history.
Uses argparse to expose --progress, --history, and --help commands.
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add src directory to Python path for importing AutoSave
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from auto_save import AutoSave
except ImportError as e:
    print(f"Error: Could not import AutoSave class: {e}")
    print("Make sure the src/auto_save.py file exists and is properly configured.")
    sys.exit(1)


def format_timestamp(timestamp_str: Optional[str]) -> str:
    """Format ISO timestamp string to readable format."""
    if not timestamp_str:
        return "Unknown"
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, AttributeError):
        return timestamp_str


def show_progress():
    """Show current novel statistics and progress."""
    print("📊 Novel Writing Progress")
    print("=" * 50)
    
    try:
        autosave = AutoSave()
        
        # Load latest save to get current stats
        latest_story = autosave.load_latest_save()
        
        if latest_story:
            metadata = latest_story.get('save_metadata', {})
            word_count = metadata.get('word_count', 0)
            version = metadata.get('version', 'Unknown')
            timestamp = metadata.get('timestamp')
            
            print(f"📝 Current Word Count: {word_count:,} words")
            print(f"📄 Current Version: {version}")
            print(f"⏰ Last Save: {format_timestamp(timestamp)}")
            
            # Estimate pages (assuming ~250 words per page)
            estimated_pages = word_count / 250
            print(f"📚 Estimated Pages: {estimated_pages:.1f} pages")
            
            # Show story title if available
            title = latest_story.get('title', latest_story.get('story_title'))
            if title:
                print(f"📖 Story Title: {title}")
            
            # Show character count if available
            if 'characters' in latest_story:
                char_count = len(latest_story['characters'])
                print(f"👥 Characters: {char_count}")
            
        else:
            print("⚠️  No story saves found.")
            print("   Start writing to see progress statistics.")
            
    except Exception as e:
        print(f"❌ Error loading progress data: {e}")


def show_history():
    """List the last 3 save versions with details."""
    print("📚 Recent Save History")
    print("=" * 50)
    
    try:
        autosave = AutoSave()
        history = autosave.get_save_history()
        
        if not history:
            print("⚠️  No save history found.")
            print("   Create some saves to see history.")
            return
        
        # Show last 3 saves
        recent_saves = history[:3]
        
        for i, save in enumerate(recent_saves, 1):
            print(f"\n🔸 Save #{i}")
            print(f"   📁 File: {save['filename']}")
            print(f"   📊 Version: {save.get('version', 'Unknown')}")
            print(f"   📝 Words: {save.get('word_count', 0):,}")
            print(f"   ⏰ Saved: {format_timestamp(save.get('timestamp'))}")
            
            # File size in KB
            size_bytes = save.get('size_bytes', 0)
            size_kb = size_bytes / 1024 if size_bytes > 0 else 0
            print(f"   💾 Size: {size_kb:.1f} KB")
        
        if len(history) > 3:
            print(f"\n📝 ... and {len(history) - 3} more saves in history")
            
    except Exception as e:
        print(f"❌ Error loading save history: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Novel Writer Agent CLI Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --progress    Show current writing progress and stats
  python cli.py --history     List the last 3 save versions
  python cli.py --help        Show this help message

For more information about the Novel Writer Agent, see the README.md file.
        """
    )
    
    # Add mutually exclusive group for main commands
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument(
        "--progress",
        action="store_true",
        help="Show current novel statistics including word count, version, and last save time"
    )
    
    group.add_argument(
        "--history",
        action="store_true",
        help="List the last 3 save versions with details (filename, word count, timestamp)"
    )
    
    try:
        args = parser.parse_args()
        
        # Execute the requested command
        if args.progress:
            show_progress()
        elif args.history:
            show_history()
            
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
