"""Projects section handler."""

from typing import List

from resume_generator.schemas import Projects
from resume_generator.sections.base import BaseSection


class ProjectsSection(BaseSection):
    """Handler for the projects section of the resume."""

    def __init__(self, pdf, data: List[Projects], styles: dict, config: dict):
        """Initialize the projects section handler.

        Args:
            pdf: The PDF document object.
            data (List[Projects]): List of project entries.
            styles (dict): Style definitions for this section.
            config (dict): Template configuration settings.
        """
        super().__init__(pdf, data, styles["projects"], config)

    def add_section(self) -> None:
        """Add the projects section to the PDF."""
        # Add section header
        self.add_cell("Projects", "section_header", height=8)

        # Add each project entry
        for project in self.data:
            if project.include:
                # Add project name
                self.add_cell(project.name, "name", height=5)

                # Add project link if available
                if project.link:
                    self.set_style("link")
                    self.pdf.write_html(f'<a href="{project.link}">{project.link}</a>')

                # Add duration
                self.add_multi_cell(f"{project.duration[0]} - {project.duration[1]}", "details")

                # Add description
                self.add_multi_cell(project.description, "details")
                # Add separator line
                self.add_cell("―" * 30, "details", height=2)

                # Add skills if available
                if project.skills:
                    self.format_labeled_text("Skills:", ', '.join(project.skills), "details")

                # Add spacing between projects
                self.add_cell("", "details", height=5)
