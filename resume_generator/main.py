"""Resume generator that creates customized PDF resumes from JSON data.

This module provides functionality to generate professional resumes in PDF format
using data from a JSON file and configuration from a YAML file. It supports
various sections including personal information, work experience, education,
certifications, volunteering, projects, awards, and languages.
"""

import json
import os
import warnings
from datetime import datetime

import yaml
from fpdf import FPDF

from resume_generator.schemas import ApplicationInfo
from resume_generator.schemas import Articles
from resume_generator.schemas import Education
from resume_generator.schemas import General
from resume_generator.schemas import HonorsAndAwards
from resume_generator.schemas import Jobs
from resume_generator.schemas import Languages
from resume_generator.schemas import LicensesAndCertifications
from resume_generator.schemas import Projects
from resume_generator.schemas import VolunteerExperience
from resume_generator.sections import ArticlesSection
from resume_generator.sections import AwardsSection
from resume_generator.sections import CertificationsSection
from resume_generator.sections import EducationSection
from resume_generator.sections import GeneralSection
from resume_generator.sections import JobsSection
from resume_generator.sections import LanguagesSection
from resume_generator.sections import ProjectsSection
from resume_generator.sections import VolunteeringSection
from resume_generator.styles import modern_styles

warnings.simplefilter("default", DeprecationWarning)


def load_config():
    """Load configuration from config.yaml file.

    Returns:
        dict: Configuration settings loaded from YAML file.

    Raises:
        FileNotFoundError: If config.yaml is not found.
        ValueError: If config.yaml contains invalid YAML.
    """
    try:
        with open("config.yaml", "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError("config.yaml not found")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in config.yaml: {str(e)}")


def load_resume_data():
    """Load and validate resume data from JSON file.

    Returns:
        tuple: Validated resume data sections (application_info, general, jobs, etc.).

    Raises:
        FileNotFoundError: If resume.json is not found.
        ValueError: If resume.json contains invalid JSON or data validation fails.
    """
    try:
        with open("resume.json", "r") as file:
            resume_data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("resume.json not found")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in resume.json: {str(e)}")

    try:
        # Validate and parse resume sections
        application_info = ApplicationInfo.model_validate(
            resume_data["ApplicationInfo"]
        )
        general = General.model_validate(resume_data["General"])
        jobs = [
            Jobs.model_validate(job_data) for job_data in resume_data["Jobs"].values()
        ]
        schools = [
            Education.model_validate(edu_data)
            for edu_data in resume_data["Education"].values()
        ]
        certifications = [
            LicensesAndCertifications.model_validate(cert_data)
            for cert_data in resume_data["LicensesAndCertifications"].values()
        ]
        volunteer_experiences = [
            VolunteerExperience.model_validate(exp_data)
            for exp_data in resume_data["VolunteerExperience"].values()
        ]
        projects = [
            Projects.model_validate(proj_data)
            for proj_data in resume_data["Projects"].values()
        ]
        awards = [
            HonorsAndAwards.model_validate(award_data)
            for award_data in resume_data["HonorsAndAwards"].values()
        ]
        languages = [
            Languages.model_validate(lang_data)
            for lang_data in resume_data["Languages"].values()
        ]
        articles = [
            Articles.model_validate(article_data)
            for article_data in resume_data["Articles"].values()
        ]

        return (
            application_info,
            general,
            jobs,
            schools,
            certifications,
            volunteer_experiences,
            projects,
            awards,
            languages,
            articles,
        )
    except KeyError as e:
        raise ValueError(f"Missing required section in resume.json: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error validating resume data: {str(e)}")


def setup_pdf(config):
    """Initialize PDF with configuration settings.

    Args:
        config (dict): Configuration dictionary containing PDF settings.

    Returns:
        tuple: (FPDF object, template configuration dictionary).

    Raises:
        FileNotFoundError: If required font files are not found.
        ValueError: If required configuration is missing.
        RuntimeError: If PDF setup fails.
    """
    try:
        template_config = config["templates"][config["template"]]
        pdf = FPDF(format=template_config["pdf_format"])
        pdf.add_page()

        # Add fonts
        for font_name, font_file in template_config["fonts"].items():
            font_path = f"fonts/{font_file}.ttf"
            if not os.path.exists(font_path):
                raise FileNotFoundError(f"Font file not found: {font_path}")
            pdf.add_font(font_file, "", font_path)

        pdf.set_fallback_fonts(["TwitterEmojis"])
        pdf.set_font(
            template_config["fonts"]["primary"],
            size=template_config["font_size"]["normal"],
        )

        return pdf, template_config
    except KeyError as e:
        raise ValueError(f"Missing required configuration: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error setting up PDF: {str(e)}")


def ensure_output_directory(config, application_info):
    """Create output directory structure if it doesn't exist.

    Args:
        config (dict): Configuration dictionary containing output settings.
        application_info (ApplicationInfo): Application-specific information.

    Returns:
        str: Path to the created output directory.

    Raises:
        RuntimeError: If directory creation fails.
    """
    try:
        output_dir = os.path.join(
            config["output_directory"], application_info.company, application_info.job
        )
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    except Exception as e:
        raise RuntimeError(f"Error creating output directory: {str(e)}")


def main():
    """Generate a customized PDF resume from JSON data and YAML configuration.

    This function orchestrates the entire resume generation process by:
    1. Loading configuration and resume data
    2. Setting up the PDF with proper formatting
    3. Creating the output directory structure
    4. Adding each resume section to the PDF
    5. Saving the final PDF file

    Raises:
        Various exceptions with descriptive error messages if any step fails.
    """
    try:
        # Load configuration and resume data
        config = load_config()
        resume_data = load_resume_data()
        (
            application_info,
            general,
            jobs,
            schools,
            certifications,
            volunteer_experiences,
            projects,
            awards,
            languages,
            articles,
        ) = resume_data

        # Setup PDF with configuration
        pdf, template_config = setup_pdf(config)

        # Create output directory
        output_dir = ensure_output_directory(config, application_info)

        # Get styles based on template
        styles = modern_styles  # For now, we only have modern style

        # Generate resume sections using section handlers
        sections = [
            GeneralSection(pdf, general, styles, template_config),
            ProjectsSection(pdf, projects, styles, template_config),
            ArticlesSection(pdf, articles, styles, template_config),
            JobsSection(pdf, jobs, styles, template_config),
            # EducationSection(pdf, schools, styles, template_config),
            # CertificationsSection(pdf, certifications, styles, template_config),
            # VolunteeringSection(pdf, volunteer_experiences, styles, template_config),
            # AwardsSection(pdf, awards, styles, template_config),
            # LanguagesSection(pdf, languages, styles, template_config),
        ]

        # Add each section to the PDF
        for section in sections:
            section.add_section()

        # Generate output filename
        output_file = config["file_name_template"].format(
            name=general.name,
            company=application_info.company,
            job=application_info.job,
            date=datetime.now().strftime("%Y-%m-%d"),
        )
        output_path = os.path.join(output_dir, output_file)

        # Save the PDF
        pdf.output(output_path)
        print(f"Resume generated successfully: {output_path}")

    except Exception as e:
        print(f"Error generating resume: {str(e)}")
        raise


if __name__ == "__main__":
    main()
