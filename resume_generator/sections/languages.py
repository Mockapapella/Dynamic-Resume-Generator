"""Languages section handler."""

from typing import List

from resume_generator.schemas import Languages
from resume_generator.sections.base import BaseSection


class LanguagesSection(BaseSection):
    """Handler for the languages section of the resume."""

    def __init__(self, pdf, data: List[Languages], styles: dict, config: dict):
        """Initialize the languages section handler.

        Args:
            pdf: The PDF document object.
            data (List[Languages]): List of language entries.
            styles (dict): Style definitions for this section.
            config (dict): Template configuration settings.
        """
        super().__init__(pdf, data, styles["languages"], config)

    def add_section(self) -> None:
        """Add the languages section to the PDF."""
        # Add section header
        self.add_cell("Languages", "section_header", height=8)

        # Add each language entry
        for language in self.data:
            if language.include:
                # Add language name
                self.add_cell(language.language, "language", height=5)

                # Add proficiency level
                self.add_multi_cell(language.proficiency, "proficiency")

                # Add spacing between languages
                self.add_cell("", "proficiency", height=2)
