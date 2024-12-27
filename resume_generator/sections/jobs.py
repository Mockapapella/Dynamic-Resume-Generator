"""Jobs section handler."""

from typing import List

from resume_generator.schemas import Jobs
from resume_generator.sections.base import BaseSection


class JobsSection(BaseSection):
    """Handler for the jobs/work experience section of the resume."""

    def __init__(self, pdf, data: List[Jobs], styles: dict, config: dict):
        """Initialize the jobs section handler.

        Args:
            pdf: The PDF document object.
            data (List[Jobs]): List of job experiences.
            styles (dict): Style definitions for this section.
            config (dict): Template configuration settings.
        """
        super().__init__(pdf, data, styles["jobs"], config)

    def add_section(self) -> None:
        """Add the jobs section to the PDF."""
        # Add section header
        self.add_cell("Jobs", "section_header", height=8)

        # Add each job entry
        for job in self.data:
            if job.include:
                # Add job title
                self.add_cell(job.title, "title", height=5)

                # Add company name
                self.add_cell(job.company, "company")

                # Add employment type and duration
                self.add_cell(f"Employment Type: {job.employment_type}", "details")
                self.add_cell(
                    f"Duration: {job.duration[0]} - {job.duration[1]}",
                    "details"
                )

                # Add description if available
                if job.description:
                    self.add_multi_cell(
                        f"Description: {job.description}",
                        "details"
                    )

                # Add skills if available
                if job.skills:
                    self.add_cell(
                        f"Skills: {', '.join(job.skills)}",
                        "details"
                    )

                # Add spacing between jobs
                self.add_cell("", "details", height=5)
