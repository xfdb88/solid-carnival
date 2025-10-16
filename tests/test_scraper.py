"""Tests for Instagram scraper functionality."""

import pytest
import csv
from pathlib import Path
from instagram_scraper.config import Config
from instagram_scraper.cli import read_usernames, write_results


@pytest.fixture
def temp_input_file(tmp_path):
    """Create a temporary input CSV file."""
    file_path = tmp_path / "input.csv"
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['username'])
        writer.writerow(['testuser1'])
        writer.writerow(['testuser2'])
    return file_path


@pytest.fixture
def temp_output_file(tmp_path):
    """Create a temporary output CSV file path."""
    return tmp_path / "output.csv"


@pytest.fixture
def sample_results():
    """Sample scraper results."""
    return [
        {
            "username": "testuser1",
            "display_name": "Test User 1",
            "bio": "Test bio",
            "email": "",
            "phone": "",
            "links": "",
            "gender": "",
            "age": "",
            "region": "",
            "warning_code": "",
            "error": ""
        },
        {
            "username": "testuser2",
            "display_name": "Test User 2",
            "bio": "",
            "email": "",
            "phone": "",
            "links": "",
            "gender": "",
            "age": "",
            "region": "",
            "warning_code": "",
            "error": "Profile not found"
        }
    ]


def test_read_usernames(temp_input_file):
    """Test reading usernames from CSV."""
    usernames = read_usernames(temp_input_file)
    assert len(usernames) == 2
    assert usernames[0] == 'testuser1'
    assert usernames[1] == 'testuser2'


def test_read_usernames_file_not_found():
    """Test reading from non-existent file."""
    with pytest.raises(SystemExit):
        read_usernames(Path("/nonexistent/file.csv"))


def test_write_results(temp_output_file, sample_results):
    """Test writing results to CSV."""
    write_results(temp_output_file, sample_results)
    
    assert temp_output_file.exists()
    
    with open(temp_output_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == 2
    assert rows[0]['username'] == 'testuser1'
    assert rows[0]['display_name'] == 'Test User 1'
    assert rows[1]['username'] == 'testuser2'
    assert rows[1]['error'] == 'Profile not found'


def test_write_results_empty_list(temp_output_file):
    """Test writing empty results."""
    write_results(temp_output_file, [])
    assert not temp_output_file.exists() or temp_output_file.stat().st_size == 0


def test_config_validation():
    """Test config validation."""
    original_username = Config.INSTAGRAM_USERNAME
    original_password = Config.INSTAGRAM_PASSWORD
    
    Config.INSTAGRAM_USERNAME = ""
    Config.INSTAGRAM_PASSWORD = ""
    
    with pytest.raises(ValueError, match="Instagram credentials must be set"):
        Config.validate()
    
    Config.INSTAGRAM_USERNAME = original_username
    Config.INSTAGRAM_PASSWORD = original_password
