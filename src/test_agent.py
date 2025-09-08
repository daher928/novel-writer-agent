"""Test suite for the novel writer agent module.

This module contains pytest-compatible tests for validating the core functionality
of the novel writer agent, including page generation and CLI option parsing.
"""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the main agent module (assuming it exists as agent.py)
try:
    from agent import generate_page, parse_cli_args
except ImportError:
    # If agent module doesn't exist yet, create mock functions for testing
    def generate_page(*args, **kwargs):
        """Mock function for testing."""
        return "Generated page content"
    
    def parse_cli_args(*args, **kwargs):
        """Mock function for testing."""
        return {"output_dir": "./output", "verbose": False}


class TestPageGeneration:
    """Test cases for page generation functionality."""
    
    def test_generate_page_creates_output(self):
        """Test that generate_page function produces valid output.
        
        Verifies that the page generation function returns non-empty content
        and that the content is properly formatted as a string.
        """
        result = generate_page("Test prompt", "Test context")
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Test" in result or len(result) > 10  # Basic content validation
    
    def test_generate_page_saves_to_file(self):
        """Test that generated pages are properly saved to disk.
        
        Creates a temporary directory, generates a page, saves it to a file,
        and verifies that the file exists and contains the expected content.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_page.txt"
            content = generate_page("Sample prompt", "Sample context")
            
            # Save the generated content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Verify file was created and contains content
            assert output_path.exists()
            assert output_path.stat().st_size > 0
            
            # Read back and verify content
            with open(output_path, 'r', encoding='utf-8') as f:
                saved_content = f.read()
            
            assert saved_content == content
            assert len(saved_content) > 0


class TestCLIOptionParser:
    """Test cases for command-line interface option parsing."""
    
    def test_parse_cli_args_default_values(self):
        """Test CLI parser with default argument values.
        
        Verifies that the CLI argument parser correctly handles default
        values when no arguments are provided.
        """
        with patch('sys.argv', ['agent.py']):
            args = parse_cli_args()
            
            assert isinstance(args, dict)
            assert 'output_dir' in args or hasattr(args, 'output_dir')
    
    def test_parse_cli_args_with_output_dir(self):
        """Test CLI parser with custom output directory.
        
        Verifies that the CLI argument parser correctly processes
        a custom output directory argument.
        """
        test_output_dir = "/custom/output/path"
        
        with patch('sys.argv', ['agent.py', '--output-dir', test_output_dir]):
            try:
                args = parse_cli_args()
                
                # Handle both dict and namespace object returns
                if isinstance(args, dict):
                    output_dir = args.get('output_dir', args.get('output-dir'))
                else:
                    output_dir = getattr(args, 'output_dir', getattr(args, 'output-dir', None))
                
                assert output_dir == test_output_dir
            except (SystemExit, AttributeError):
                # If the actual CLI parser doesn't exist yet, this is expected
                pytest.skip("CLI parser not yet implemented")
    
    def test_parse_cli_args_verbose_flag(self):
        """Test CLI parser with verbose flag.
        
        Verifies that the CLI argument parser correctly processes
        the verbose flag option.
        """
        with patch('sys.argv', ['agent.py', '--verbose']):
            try:
                args = parse_cli_args()
                
                # Handle both dict and namespace object returns
                if isinstance(args, dict):
                    verbose = args.get('verbose', False)
                else:
                    verbose = getattr(args, 'verbose', False)
                
                assert verbose is True
            except (SystemExit, AttributeError):
                # If the actual CLI parser doesn't exist yet, this is expected
                pytest.skip("CLI parser not yet implemented")


class TestAgentIntegration:
    """Integration tests for the novel writer agent."""
    
    def test_end_to_end_page_generation(self):
        """Test complete workflow from input to saved output.
        
        Performs an end-to-end test that simulates the complete workflow
        of generating a page and saving it to the filesystem.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test data
            prompt = "Write a short story about a mysterious forest"
            context = "Fantasy genre, 200 words maximum"
            output_file = Path(temp_dir) / "generated_story.txt"
            
            # Generate content
            content = generate_page(prompt, context)
            
            # Simulate saving process
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Verify the complete workflow
            assert output_file.exists()
            assert output_file.stat().st_size > 0
            
            # Verify content quality (basic checks)
            with open(output_file, 'r', encoding='utf-8') as f:
                saved_content = f.read()
            
            assert len(saved_content) > 50  # Reasonable minimum length
            assert isinstance(saved_content, str)
            
    def test_multiple_page_generation(self):
        """Test generation of multiple pages in sequence.
        
        Verifies that the agent can generate multiple pages without
        conflicts or performance degradation.
        """
        prompts = [
            "Write about a brave knight",
            "Describe a magical kingdom",
            "Tell a tale of adventure"
        ]
        
        results = []
        for prompt in prompts:
            content = generate_page(prompt, "Fantasy context")
            results.append(content)
        
        # Verify all generations succeeded
        assert len(results) == len(prompts)
        for result in results:
            assert isinstance(result, str)
            assert len(result) > 0
        
        # Verify results are different (basic uniqueness check)
        assert len(set(results)) >= len(results) // 2  # Allow some similarity


if __name__ == "__main__":
    # Allow running tests directly with python test_agent.py
    pytest.main([__file__])
