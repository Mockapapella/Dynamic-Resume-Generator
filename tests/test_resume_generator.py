import pytest
import os
import json
from datetime import datetime
from main import (
    load_config,
    load_resume_data,
    setup_pdf,
    ensure_output_directory
)

@pytest.fixture
def sample_resume_data():
    return {
        "ApplicationInfo": {
            "company": "Test Company",
            "job": "Test Position"
        },
        "General": {
            "name": "John Doe",
            "title": "Software Engineer",
            "location": "San Francisco, CA",
            "email": "john@example.com",
            "cell_number": "+1234567890",
            "portfolio": "https://portfolio.example.com",
            "linkedin": "https://linkedin.com/in/johndoe",
            "github": "https://github.com/johndoe",
            "description": "Experienced software engineer with a passion for clean code."
        },
        "Jobs": {},
        "Education": {},
        "LicensesAndCertifications": {},
        "VolunteerExperience": {},
        "Projects": {},
        "HonorsAndAwards": {},
        "Languages": {}
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
                    "emoji": "TwitterEmojis"
                },
                "font_size": {
                    "name": 24,
                    "title": 16,
                    "section_header": 14,
                    "job_title": 12,
                    "normal": 8
                }
            }
        }
    }

def test_load_config(tmp_path, sample_config):
    """Test loading configuration from YAML file"""
    config_path = tmp_path / "config.yaml"
    with open(config_path, "w") as f:
        json.dump(sample_config, f)

    with pytest.raises(FileNotFoundError):
        load_config()  # Should fail when config.yaml doesn't exist in cwd

def test_load_resume_data(tmp_path, sample_resume_data):
    """Test loading and validating resume data"""
    resume_path = tmp_path / "resume.json"
    with open(resume_path, "w") as f:
        json.dump(sample_resume_data, f)

    with pytest.raises(FileNotFoundError):
        load_resume_data()  # Should fail when resume.json doesn't exist in cwd

def test_ensure_output_directory(tmp_path, sample_config, sample_resume_data):
    """Test output directory creation"""
    config = sample_config.copy()
    config["output_directory"] = str(tmp_path / "output")

    from schemas import ApplicationInfo
    application_info = ApplicationInfo.model_validate(sample_resume_data["ApplicationInfo"])

    output_dir = ensure_output_directory(config, application_info)
    assert os.path.exists(output_dir)
    assert os.path.isdir(output_dir)
    assert output_dir.endswith(f"{application_info.company}/{application_info.job}")

def test_setup_pdf(sample_config):
    """Test PDF setup with configuration"""
    with pytest.raises(FileNotFoundError):
        # Should fail when font files don't exist
        setup_pdf(sample_config)
