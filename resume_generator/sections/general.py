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
        contact_fields = [
            self.data.location,
            self.data.email,
            self.data.cell_number,
            self.data.portfolio,
            self.data.linkedin,
            self.data.github
        ]

        # Filter out None values and convert to strings
        contact_info = [str(field) for field in contact_fields if field is not None]

        for info in contact_info:
            self.add_cell(info, "contact")

        # Add description header and content
        self.add_cell("Description", "description_header", height=8)
        self.add_multi_cell(self.data.description, "description")
