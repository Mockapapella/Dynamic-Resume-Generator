from fpdf import FPDF, XPos, YPos
import json
from schemas import ApplicationInfo
from schemas import General
from schemas import Jobs
from schemas import Education
from schemas import LicensesAndCertifications
from schemas import VolunteerExperience
from schemas import HonorsAndAwards
from schemas import Languages
from schemas import Projects
from fpdf import FPDF
import warnings
warnings.simplefilter('default', DeprecationWarning)
# Load the JSON data from the file
with open('resume.json', 'r') as file:
    resume_data = json.load(file)

# Now resume_data is a dictionary containing the contents of the JSON file
application_info = ApplicationInfo.model_validate(
    resume_data["ApplicationInfo"])
general = General.model_validate(resume_data["General"])
jobs = [Jobs.model_validate(resume_data["Jobs"][job])
        for job in resume_data["Jobs"]]
schools = [Education.model_validate(resume_data["Education"][school])
           for school in resume_data["Education"]]
certifications = [LicensesAndCertifications.model_validate(resume_data["LicensesAndCertifications"][cert])
                  for cert in resume_data["LicensesAndCertifications"]]
volunteer_experiences = [VolunteerExperience.model_validate(resume_data["VolunteerExperience"][experience])
                         for experience in resume_data["VolunteerExperience"]]
projects = [Projects.model_validate(resume_data["Projects"][project])
            for project in resume_data["Projects"]]
awards = [HonorsAndAwards.model_validate(resume_data["HonorsAndAwards"][award])
          for award in resume_data["HonorsAndAwards"]]
languages = [Languages.model_validate(resume_data["Languages"][language])
             for language in resume_data["Languages"]]
cell_width = 190
cell_height = 4

# Set up the PDF document
pdf = FPDF(format="letter")
pdf.add_page()
# Assuming the font files are in 'fonts/' directory
pdf.add_font('DejaVuSans', '', 'fonts/DejaVuSans.ttf')
pdf.add_font('TwitterEmojis', '', 'fonts/TwitterEmojis.ttf')
pdf.set_fallback_fonts(['TwitterEmojis'])
pdf.set_font('DejaVuSans', size=8)


def add_general_information(pdf):
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 10, text=f"{general.name}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font(size=16)
    pdf.cell(cell_width, 8, text=f"{general.title}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font(size=8)
    pdf.cell(cell_width, cell_height, text=f"{general.location}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(cell_width, cell_height, text=f"{general.email}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(cell_width, cell_height, text=f"{general.cell_number}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(cell_width, cell_height, text=f"{general.portfolio}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(cell_width, cell_height, text=f"{general.linkedin}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(cell_width, cell_height, text=f"{general.github}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Handle the description with text wrapping
    pdf.set_font(size=14)
    pdf.cell(cell_width, 8, text="Description",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font(size=8)
    pdf.multi_cell(cell_width, cell_height,
                   text=f"{general.description}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    return pdf


def add_jobs(pdf):
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 8, text="Jobs",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for job in jobs:
        if job.include is True:
            pdf.set_font(size=12)
            pdf.cell(cell_width, 5, text=f"{job.title}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=10)
            pdf.cell(cell_width, cell_height, text=f"{job.company}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=8)
            pdf.cell(cell_width, cell_height, text=f"Employment Type: {job.employment_type}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(cell_width, cell_height, text=f"Duration: {job.duration[0]} - {job.duration[1]}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.multi_cell(cell_width, cell_height, text=f"Description: {job.description}",
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            if job.skills:
                pdf.cell(cell_width, cell_height, text=f"Skills: {', '.join([x for x in job.skills])}",
                         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(cell_width, 5, text="",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    return pdf


def add_education(pdf):
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 8, text="Education",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for school in schools:
        if school.include is True:
            pdf.set_font(size=12)
            pdf.cell(cell_width, 5, text=f"{school.school}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=10)
            pdf.cell(cell_width, cell_height, text=f"{school.field}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=8)
            pdf.cell(cell_width, cell_height, text=f"Duration: {school.duration[0]} - {school.duration[1]}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            if school.activities_and_societies:
                pdf.cell(cell_width, cell_height, text=f"Clubs: {', '.join([x for x in school.activities_and_societies])}",
                         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(cell_width, 5, text="",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    return pdf


def add_certification(pdf):
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 8, text="Certifications",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for cert in certifications:
        if cert.include is True:
            pdf.set_font(size=12)
            pdf.cell(cell_width, 5, text=f"{cert.name}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=10)
            pdf.cell(cell_width, cell_height, text=f"Issued By: {cert.issuer}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=8)
            pdf.cell(cell_width, cell_height, text=f"Issued On: {cert.issued_on}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(cell_width, cell_height, text=f"Credential ID: {cert.credential_id}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(cell_width, 5, text="",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    return pdf


def add_volunteering(pdf):
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 8, text="Volunteering",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for experience in volunteer_experiences:
        if experience.include is True:
            pdf.set_font(size=12)
            pdf.cell(cell_width, 5, text=f"{experience.organization}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=10)
            pdf.cell(cell_width, cell_height, text=f"{experience.role}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=8)
            pdf.cell(cell_width, cell_height, text=f"{experience.cause}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(cell_width, cell_height, text=f"Duration: {experience.duration[0]} - {experience.duration[1]}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.multi_cell(cell_width, cell_height, text=f"Description: {experience.description}",
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(cell_width, 5, text="",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    return pdf


def add_projects(pdf):
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 8, text="Projects",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for project in projects:
        if project.include is True:
            pdf.set_font(size=12)
            pdf.cell(cell_width, 5, text=f"{project.name}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=10)
            pdf.write_html(f'<a href="{project.link}">{project.link}</a>')
            pdf.set_font(size=8)
            pdf.cell(cell_width, cell_height, text=f"Duration: {project.duration[0]} - {project.duration[1]}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.multi_cell(cell_width, cell_height, text=f"Description: {project.description}",
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            if project.skills:
                pdf.cell(cell_width, cell_height, text=f"Skills: {', '.join([x for x in project.skills])}",
                         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(cell_width, 5, text="",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    return pdf


def add_awards(pdf):
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 8, text="Awards",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for award in awards:
        if award.include is True:
            pdf.set_font(size=12)
            pdf.cell(cell_width, 5, text=f"{award.title}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=10)
            pdf.cell(cell_width, cell_height, text=f"{award.issuer}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=8)
            pdf.cell(cell_width, cell_height, text=f"{award.issued_on}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.multi_cell(cell_width, cell_height, text=f"Description: {award.description}",
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.cell(cell_width, 5, text="",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    return pdf


def add_languages(pdf):
    pdf.set_font(size=14, style="U")
    pdf.cell(cell_width, 8, text="Languages",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    for language in languages:
        if language.include is True:
            pdf.set_font(size=12)
            pdf.cell(cell_width, 5, text=f"{language.language}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font(size=10)
            pdf.cell(cell_width, cell_height, text=f"{language.proficiency}",
                     new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    return pdf


pdf = add_general_information(pdf)
pdf = add_jobs(pdf)
pdf = add_education(pdf)
pdf = add_certification(pdf)
pdf = add_volunteering(pdf)
pdf = add_projects(pdf)
pdf = add_awards(pdf)
pdf = add_languages(pdf)


# Save the PDF to a file
pdf.output("general_info.pdf")
