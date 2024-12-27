"""Awards section handler."""

from typing import List

from resume_generator.schemas import HonorsAndAwards
from resume_generator.sections.base import BaseSection


class AwardsSection(BaseSection):
    """Handler for the awards section of the resume."""

    def __init__(self, pdf, data: List[HonorsAndAwards], styles: dict, config: dict):
        """Initialize the awards section handler.

        Args:
            pdf: The PDF document object.
            data (List[HonorsAndAwards]): List of award entries.
            styles (dict): Style definitions for this section.
            config (dict): Template configuration settings.
        """
        super().__init__(pdf, data, styles["awards"], config)

    def add_section(self) -> None:
        """Add the awards section to the PDF."""
        # Add section header
        self.add_cell("Awards", "section_header", height=8)

        # Add each award entry
        for award in self.data:
            if award.include:
                # Add award title
                self.add_cell(award.title, "title", height=5)

                # Add issuer
                self.add_cell(award.issuer, "issuer")

                # Add issue date
                self.add_cell(f"Issued On: {award.issued_on}", "details")

                # Add description
                self.add_multi_cell(f"Description: {award.description}", "details")

                # Add spacing between awards
                self.add_cell("", "details", height=5)
