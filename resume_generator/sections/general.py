"""General information section handler."""

from resume_generator.schemas import General
from resume_generator.sections.base import BaseSection


class GeneralSection(BaseSection):
    """Handler for the general information section of the resume."""

    def __init__(self, pdf, data: General, styles: dict, config: dict):
        """Initialize the general section handler.

        Args:
            pdf: The PDF document object.
            data (General): The general information data.
            styles (dict): Style definitions for this section.
            config (dict): Template configuration settings.
        """
        super().__init__(pdf, data, styles["general"], config)

    def add_section(self) -> None:
        """Add the general information section to the PDF."""
        # Add name
        self.add_cell(self.data.name, "name", height=10)

        # Add title
        self.add_cell(self.data.title, "title", height=8)

        # Add contact information
        if self.data.location:
            self.add_cell(self.data.location, "contact")
        if self.data.email:
            self.add_cell(self.data.email, "contact")
        if self.data.cell_number:
            self.add_cell(str(self.data.cell_number), "contact")

        # Add URLs as clickable links with proper spacing
        if self.data.portfolio:
            self.set_style("link")
            self.pdf.write_html(f'<a href="{self.data.portfolio}">{self.data.portfolio}</a>')
            self.add_cell("", "contact", height=1)  # Add spacing after link
        if self.data.linkedin:
            self.set_style("link")
            self.pdf.write_html(f'<a href="{self.data.linkedin}">{self.data.linkedin}</a>')
            self.add_cell("", "contact", height=1)  # Add spacing after link
        if self.data.github:
            self.set_style("link")
            self.pdf.write_html(f'<a href="{self.data.github}">{self.data.github}</a>')

        # Add description header and content
        self.add_cell("Description", "description_header", height=8)
        self.add_multi_cell(self.data.description, "description")
