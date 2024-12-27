"""Resume section handlers."""

from resume_generator.sections.awards import AwardsSection
from resume_generator.sections.base import BaseSection
from resume_generator.sections.certifications import CertificationsSection
from resume_generator.sections.education import EducationSection
from resume_generator.sections.general import GeneralSection
from resume_generator.sections.jobs import JobsSection
from resume_generator.sections.languages import LanguagesSection
from resume_generator.sections.projects import ProjectsSection
from resume_generator.sections.volunteering import VolunteeringSection
from resume_generator.sections.articles import ArticlesSection

__all__ = [
    "AwardsSection",
    "BaseSection",
    "CertificationsSection",
    "EducationSection",
    "GeneralSection",
    "JobsSection",
    "LanguagesSection",
    "ProjectsSection",
    "VolunteeringSection",
    "ArticlesSection",
]
