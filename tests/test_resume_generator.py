import json
import os

import pytest
import yaml

from resume_generator.main import ensure_output_directory
from resume_generator.main import load_config
from resume_generator.main import load_resume_data
from resume_generator.main import setup_pdf


@pytest.fixture
def sample_resume_data():
    return {
        "ApplicationInfo": {"company": "Test Company", "job": "Test Position"},
        "General": {
            "name": "John Doe",
            "title": "Software Engineer",
            "location": "San Francisco, CA",
            "email": "john@example.com",
            "cell_number": "+1234567890",
            "portfolio": "https://portfolio.example.com",
            "linkedin": "https://linkedin.com/in/johndoe",
            "github": "https://github.com/johndoe",
            "description": "Experienced software engineer with a passion for clean code.",
        },
        "Jobs": {},
        "Education": {},
        "LicensesAndCertifications": {},
        "VolunteerExperience": {},
        "Projects": {},
        "HonorsAndAwards": {},
        "Languages": {},
    }


@pytest.fixture
def sample_config():
    return {
        "output_directory": "generated_applications",
        "file_name_template": "Resume - {name} - {company} - {job} - {date}.pdf",
        "template": "modern",
        "templates": {
            "modern": {
                "pdf_format": "letter",
                "cell_width": 190,
                "cell_height": 4,
                "fonts": {
                    "primary": "DejaVuSans",
                    "bold": "DejaVuSans-Bold",
                    "emoji": "TwitterEmojis",
                },
                "font_size": {
                    "name": 24,
                    "title": 16,
                    "section_header": 14,
                    "job_title": 12,
                    "normal": 8,
                },
            }
        },
    }


def test_load_config(tmp_path, sample_config, monkeypatch):
    """Test loading configuration from YAML file."""
    # Change working directory to temp path for testing
    monkeypatch.chdir(tmp_path)

    # Test should fail when config.yaml doesn't exist
    with pytest.raises(FileNotFoundError):
        load_config()

    # Write config file and test successful loading
    with open("config.yaml", "w") as f:
        yaml.dump(sample_config, f)

    # Test successful loading
    config = load_config()
    assert config == sample_config


def test_load_resume_data(tmp_path, sample_resume_data, monkeypatch):
    """Test loading and validating resume data."""
    # Change working directory to temp path for testing
    monkeypatch.chdir(tmp_path)

    # Test should fail when resume.json doesn't exist
    with pytest.raises(FileNotFoundError):
        load_resume_data()

    # Write resume file and test successful loading
    with open("resume.json", "w") as f:
        json.dump(sample_resume_data, f)

    # Test successful loading
    result = load_resume_data()
    assert len(result) == 9  # Check that all sections are loaded


def test_ensure_output_directory(tmp_path, sample_config, sample_resume_data):
    """Test output directory creation"""
    config = sample_config.copy()
    config["output_directory"] = str(tmp_path / "output")

    from resume_generator.schemas import ApplicationInfo

    application_info = ApplicationInfo.model_validate(sample_resume_data["ApplicationInfo"])

    output_dir = ensure_output_directory(config, application_info)
    assert os.path.exists(output_dir)
    assert os.path.isdir(output_dir)
    assert output_dir.endswith(f"{application_info.company}/{application_info.job}")


def test_setup_pdf(tmp_path, sample_config, monkeypatch):
    """Test PDF setup with configuration."""
    # Change working directory to temp path for testing
    monkeypatch.chdir(tmp_path)

    # Create fonts directory but don't add any font files
    os.makedirs("fonts", exist_ok=True)

    with pytest.raises(RuntimeError) as excinfo:
        # Should fail when font files don't exist
        setup_pdf(sample_config)
    assert "Font file not found" in str(excinfo.value)
