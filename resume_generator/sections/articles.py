"""Articles section handler."""

from typing import List

from resume_generator.schemas import Articles
from resume_generator.sections.base import BaseSection


class ArticlesSection(BaseSection):
    """Handler for the articles section of the resume."""

    def __init__(self, pdf, data: List[Articles], styles: dict, config: dict):
        """Initialize the articles section handler.

        Args:
            pdf: The PDF document object.
            data (List[Articles]): List of articles.
            styles (dict): Style definitions for this section.
            config (dict): Template configuration settings.
        """
        super().__init__(pdf, data, styles["articles"], config)

    def add_section(self) -> None:
        """Add the articles section to the PDF."""
        # Add section header
        self.add_cell("Articles", "section_header", height=8)

        # Add each article entry
        for article in self.data:
            if article.include:
                # Add article title
                self.add_cell(article.title, "title", height=5)

                # Add URL if available
                if article.url:
                    self.set_style("link")
                    self.pdf.write_html(f'<a href="{article.url}">{article.url}</a>')

                # Add publication date
                self.add_multi_cell(article.date, "details")

                # Add description if available
                if article.description:
                    self.add_multi_cell(article.description, "details")

                # Add spacing between articles
                self.add_cell("", "details", height=5)
