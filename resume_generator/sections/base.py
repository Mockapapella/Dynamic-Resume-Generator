"""Base class for resume sections."""

from fpdf import FPDF
from fpdf import XPos
from fpdf import YPos


class BaseSection:
    """Base class for resume section handlers.

    This class provides common functionality for all resume sections, including
    methods for setting fonts and adding content to the PDF.
    """

    def __init__(self, pdf: FPDF, data: dict, styles: dict, config: dict):
        """Initialize the section handler.

        Args:
            pdf (FPDF): The PDF document object.
            data (dict): The section-specific data.
            styles (dict): Style definitions for this section.
            config (dict): Template configuration settings.
        """
        self.pdf = pdf
        self.data = data
        self.styles = styles
        self.cell_width = config["cell_width"]
        self.cell_height = config["cell_height"]

    def set_style(self, style_key: str) -> None:
        """Set the font according to the specified style.

        Args:
            style_key (str): Key to look up in the styles dictionary.
        """
        style = self.styles[style_key]
        font_style = style.get("style", "")
        self.pdf.set_font(style["font"], style=font_style, size=style["size"])

    def add_cell(self, text: str, style_key: str, height: float = None) -> None:
        """Add a cell with the specified text and style.

        Args:
            text (str): The text to add.
            style_key (str): Key to look up in the styles dictionary.
            height (float, optional): Cell height. Defaults to self.cell_height.
        """
        self.set_style(style_key)
        self.pdf.cell(
            self.cell_width,
            height or self.cell_height,
            text=text,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

    def add_multi_cell(self, text: str, style_key: str) -> None:
        """Add a multi-line cell with the specified text and style.

        Args:
            text (str): The text to add.
            style_key (str): Key to look up in the styles dictionary.
        """
        self.set_style(style_key)
        self.pdf.multi_cell(
            self.cell_width,
            self.cell_height,
            text=text,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

    def add_section(self) -> None:
        """Add the section to the PDF.

        This method must be implemented by subclasses.

        Raises:
            NotImplementedError: If the subclass doesn't implement this method.
        """
        raise NotImplementedError("Subclasses must implement add_section()")
