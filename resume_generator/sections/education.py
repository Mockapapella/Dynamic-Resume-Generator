"""Education section handler."""

from typing import List

from resume_generator.schemas import Education
from resume_generator.sections.base import BaseSection


class EducationSection(BaseSection):
    """Handler for the education section of the resume."""

    def __init__(self, pdf, data: List[Education], styles: dict, config: dict):
        """Initialize the education section handler.

        Args:
            pdf: The PDF document object.
            data (List[Education]): List of education entries.
            styles (dict): Style definitions for this section.
            config (dict): Template configuration settings.
        """
        super().__init__(pdf, data, styles["education"], config)

    def add_section(self) -> None:
        """Add the education section to the PDF."""
        # Add section header
        self.add_cell("Education", "section_header", height=8)

        # Add each education entry
        for school in self.data:
            if school.include:
                # Add school name
                self.add_cell(school.school, "school", height=5)

                # Add field of study
                self.add_cell(school.field, "field")

                # Add duration
                self.add_cell(
                    f"Duration: {school.duration[0]} - {school.duration[1]}",
                    "details"
                )

                # Add degree if available
                if school.degree:
                    self.add_cell(f"Degree: {school.degree}", "details")

                # Add GPA if available
                if school.gpa:
                    self.add_cell(f"GPA: {school.gpa}", "details")

                # Add activities and societies if available
                if school.activities_and_societies:
                    self.add_cell(
                        f"Clubs: {', '.join(school.activities_and_societies)}",
                        "details"
                    )

                # Add description if available
                if school.description:
                    self.add_multi_cell(
                        f"Description: {school.description}",
                        "details"
                    )

                # Add spacing between schools
                self.add_cell("", "details", height=5)
