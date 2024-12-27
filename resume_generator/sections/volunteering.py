"""Volunteering section handler."""

from typing import List

from resume_generator.schemas import VolunteerExperience
from resume_generator.sections.base import BaseSection


class VolunteeringSection(BaseSection):
    """Handler for the volunteering section of the resume."""

    def __init__(self, pdf, data: List[VolunteerExperience], styles: dict, config: dict):
        """Initialize the volunteering section handler.

        Args:
            pdf: The PDF document object.
            data (List[VolunteerExperience]): List of volunteer experience entries.
            styles (dict): Style definitions for this section.
            config (dict): Template configuration settings.
        """
        super().__init__(pdf, data, styles["volunteering"], config)

    def add_section(self) -> None:
        """Add the volunteering section to the PDF."""
        # Add section header
        self.add_cell("Volunteering", "section_header", height=8)

        # Add each volunteer experience entry
        for experience in self.data:
            if experience.include:
                # Add organization name
                self.add_cell(experience.organization, "organization", height=5)

                # Add role
                self.add_cell(experience.role, "role")

                # Add cause and duration
                self.add_cell(experience.cause, "details")
                self.add_cell(
                    f"Duration: {experience.duration[0]} - {experience.duration[1]}",
                    "details"
                )

                # Add description if available
                if experience.description:
                    self.add_multi_cell(
                        f"Description: {experience.description}",
                        "details"
                    )

                # Add spacing between experiences
                self.add_cell("", "details", height=5)
