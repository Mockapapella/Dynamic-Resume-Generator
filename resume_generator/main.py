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
from fpdf import XPos
from fpdf import YPos

from resume_generator.schemas import ApplicationInfo
from resume_generator.schemas import Education
from resume_generator.schemas import General
from resume_generator.schemas import HonorsAndAwards
from resume_generator.schemas import Jobs
from resume_generator.schemas import Languages
from resume_generator.schemas import LicensesAndCertifications
from resume_generator.schemas import Projects
from resume_generator.schemas import VolunteerExperience

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
        application_info = ApplicationInfo.model_validate(resume_data["ApplicationInfo"])
        general = General.model_validate(resume_data["General"])
        jobs = [Jobs.model_validate(job_data) for job_data in resume_data["Jobs"].values()]
        schools = [
            Education.model_validate(edu_data) for edu_data in resume_data["Education"].values()
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
            Projects.model_validate(proj_data) for proj_data in resume_data["Projects"].values()
        ]
        awards = [
            HonorsAndAwards.model_validate(award_data)
            for award_data in resume_data["HonorsAndAwards"].values()
        ]
        languages = [
            Languages.model_validate(lang_data) for lang_data in resume_data["Languages"].values()
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
            template_config["fonts"]["primary"], size=template_config["font_size"]["normal"]
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


def add_general_information(pdf, config, general):
    """Add general personal information section to the PDF.

    Args:
        pdf (FPDF): PDF document object.
        config (dict): Template configuration dictionary.
        general (General): General personal information.

    Returns:
        FPDF: Updated PDF document object.
    """
    cell_width = config["cell_width"]
    cell_height = config["cell_height"]
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 10, text=f"{general.name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font(size=16)
    pdf.cell(cell_width, 8, text=f"{general.title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font(size=8)
    pdf.cell(
        cell_width, cell_height, text=f"{general.location}", new_x=XPos.LMARGIN, new_y=YPos.NEXT
    )
    pdf.cell(cell_width, cell_height, text=f"{general.email}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(
        cell_width, cell_height, text=f"{general.cell_number}", new_x=XPos.LMARGIN, new_y=YPos.NEXT
    )
    pdf.cell(
        cell_width, cell_height, text=f"{general.portfolio}", new_x=XPos.LMARGIN, new_y=YPos.NEXT
    )
    pdf.cell(
        cell_width, cell_height, text=f"{general.linkedin}", new_x=XPos.LMARGIN, new_y=YPos.NEXT
    )
    pdf.cell(cell_width, cell_height, text=f"{general.github}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Handle the description with text wrapping
    pdf.set_font(size=14)
    pdf.cell(cell_width, 8, text="Description", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font(size=8)
    pdf.multi_cell(
        cell_width, cell_height, text=f"{general.description}", new_x=XPos.LMARGIN, new_y=YPos.NEXT
    )

    return pdf


def add_jobs(pdf, config, jobs):
    """Add work experience section to the PDF.

    Args:
        pdf (FPDF): PDF document object.
        config (dict): Template configuration dictionary.
        jobs (list): List of Jobs objects.

    Returns:
        FPDF: Updated PDF document object.
    """
    cell_width = config["cell_width"]
    cell_height = config["cell_height"]
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 8, text="Jobs", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for job in jobs:
        if job.include is True:
            pdf.set_font(size=12)
            pdf.cell(cell_width, 5, text=f"{job.title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=10)
            pdf.cell(
                cell_width, cell_height, text=f"{job.company}", new_x=XPos.LMARGIN, new_y=YPos.NEXT
            )
            pdf.set_font(size=8)
            pdf.cell(
                cell_width,
                cell_height,
                text=f"Employment Type: {job.employment_type}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            pdf.cell(
                cell_width,
                cell_height,
                text=f"Duration: {job.duration[0]} - {job.duration[1]}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            pdf.multi_cell(
                cell_width,
                cell_height,
                text=f"Description: {job.description}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            if job.skills:
                pdf.cell(
                    cell_width,
                    cell_height,
                    text=f"Skills: {', '.join([x for x in job.skills])}",
                    new_x=XPos.LMARGIN,
                    new_y=YPos.NEXT,
                )
            pdf.cell(cell_width, 5, text="", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    return pdf


def add_education(pdf, config, schools):
    """Add education section to the PDF.

    Args:
        pdf (FPDF): PDF document object.
        config (dict): Template configuration dictionary.
        schools (list): List of Education objects.

    Returns:
        FPDF: Updated PDF document object.
    """
    cell_width = config["cell_width"]
    cell_height = config["cell_height"]
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 8, text="Education", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for school in schools:
        if school.include is True:
            pdf.set_font(size=12)
            pdf.cell(cell_width, 5, text=f"{school.school}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=10)
            pdf.cell(
                cell_width, cell_height, text=f"{school.field}", new_x=XPos.LMARGIN, new_y=YPos.NEXT
            )
            pdf.set_font(size=8)
            pdf.cell(
                cell_width,
                cell_height,
                text=f"Duration: {school.duration[0]} - {school.duration[1]}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            if school.activities_and_societies:
                pdf.cell(
                    cell_width,
                    cell_height,
                    text=f"Clubs: {', '.join([x for x in school.activities_and_societies])}",
                    new_x=XPos.LMARGIN,
                    new_y=YPos.NEXT,
                )
            pdf.cell(cell_width, 5, text="", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    return pdf


def add_certification(pdf, config, certifications):
    """Add certifications section to the PDF.

    Args:
        pdf (FPDF): PDF document object.
        config (dict): Template configuration dictionary.
        certifications (list): List of LicensesAndCertifications objects.

    Returns:
        FPDF: Updated PDF document object.
    """
    cell_width = config["cell_width"]
    cell_height = config["cell_height"]
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 8, text="Certifications", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for cert in certifications:
        if cert.include is True:
            pdf.set_font(size=12)
            pdf.cell(cell_width, 5, text=f"{cert.name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=10)
            pdf.cell(
                cell_width,
                cell_height,
                text=f"Issued By: {cert.issuer}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            pdf.set_font(size=8)
            pdf.cell(
                cell_width,
                cell_height,
                text=f"Issued On: {cert.issued_on}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            pdf.cell(
                cell_width,
                cell_height,
                text=f"Credential ID: {cert.credential_id}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            pdf.cell(cell_width, 5, text="", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    return pdf


def add_volunteering(pdf, config, volunteer_experiences):
    """Add volunteering section to the PDF.

    Args:
        pdf (FPDF): PDF document object.
        config (dict): Template configuration dictionary.
        volunteer_experiences (list): List of VolunteerExperience objects.

    Returns:
        FPDF: Updated PDF document object.
    """
    cell_width = config["cell_width"]
    cell_height = config["cell_height"]
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 8, text="Volunteering", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for experience in volunteer_experiences:
        if experience.include is True:
            pdf.set_font(size=12)
            pdf.cell(
                cell_width,
                5,
                text=f"{experience.organization}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            pdf.set_font(size=10)
            pdf.cell(
                cell_width,
                cell_height,
                text=f"{experience.role}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            pdf.set_font(size=8)
            pdf.cell(
                cell_width,
                cell_height,
                text=f"{experience.cause}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            pdf.cell(
                cell_width,
                cell_height,
                text=f"Duration: {experience.duration[0]} - {experience.duration[1]}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            pdf.multi_cell(
                cell_width,
                cell_height,
                text=f"Description: {experience.description}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            pdf.cell(cell_width, 5, text="", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    return pdf


def add_projects(pdf, config, projects):
    """Add projects section to the PDF.

    Args:
        pdf (FPDF): PDF document object.
        config (dict): Template configuration dictionary.
        projects (list): List of Projects objects.

    Returns:
        FPDF: Updated PDF document object.
    """
    cell_width = config["cell_width"]
    cell_height = config["cell_height"]
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 8, text="Projects", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for project in projects:
        if project.include is True:
            pdf.set_font(size=12)
            pdf.cell(cell_width, 5, text=f"{project.name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=10)
            pdf.write_html(f'<a href="{project.link}">{project.link}</a>')
            pdf.set_font(size=8)
            pdf.cell(
                cell_width,
                cell_height,
                text=f"Duration: {project.duration[0]} - {project.duration[1]}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            pdf.multi_cell(
                cell_width,
                cell_height,
                text=f"Description: {project.description}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            if project.skills:
                pdf.cell(
                    cell_width,
                    cell_height,
                    text=f"Skills: {', '.join([x for x in project.skills])}",
                    new_x=XPos.LMARGIN,
                    new_y=YPos.NEXT,
                )
            pdf.cell(cell_width, 5, text="", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    return pdf


def add_awards(pdf, config, awards):
    """Add awards section to the PDF.

    Args:
        pdf (FPDF): PDF document object.
        config (dict): Template configuration dictionary.
        awards (list): List of HonorsAndAwards objects.

    Returns:
        FPDF: Updated PDF document object.
    """
    cell_width = config["cell_width"]
    cell_height = config["cell_height"]
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 8, text="Awards", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for award in awards:
        if award.include is True:
            pdf.set_font(size=12)
            pdf.cell(cell_width, 5, text=f"{award.title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=10)
            pdf.cell(
                cell_width, cell_height, text=f"{award.issuer}", new_x=XPos.LMARGIN, new_y=YPos.NEXT
            )
            pdf.set_font(size=8)
            pdf.cell(
                cell_width,
                cell_height,
                text=f"{award.issued_on}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            pdf.multi_cell(
                cell_width,
                cell_height,
                text=f"Description: {award.description}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
            pdf.cell(cell_width, 5, text="", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    return pdf


def add_languages(pdf, config, languages):
    """Add languages section to the PDF.

    Args:
        pdf (FPDF): PDF document object.
        config (dict): Template configuration dictionary.
        languages (list): List of Languages objects.

    Returns:
        FPDF: Updated PDF document object.
    """
    cell_width = config["cell_width"]
    cell_height = config["cell_height"]
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 8, text="Languages", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for language in languages:
        if language.include is True:
            pdf.set_font(size=12)
            pdf.cell(
                cell_width, 5, text=f"{language.language}", new_x=XPos.LMARGIN, new_y=YPos.NEXT
            )
            pdf.set_font(size=10)
            pdf.cell(
                cell_width,
                cell_height,
                text=f"{language.proficiency}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
    return pdf


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
        ) = resume_data

        # Setup PDF with configuration
        pdf, template_config = setup_pdf(config)

        # Create output directory
        output_dir = ensure_output_directory(config, application_info)

        # Generate resume sections
        pdf = add_general_information(pdf, template_config, general)
        pdf = add_jobs(pdf, template_config, jobs)
        pdf = add_education(pdf, template_config, schools)
        pdf = add_certification(pdf, template_config, certifications)
        pdf = add_volunteering(pdf, template_config, volunteer_experiences)
        pdf = add_projects(pdf, template_config, projects)
        pdf = add_awards(pdf, template_config, awards)
        pdf = add_languages(pdf, template_config, languages)

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
