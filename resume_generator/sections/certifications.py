"""Certifications section handler."""

from typing import List

from resume_generator.schemas import LicensesAndCertifications
from resume_generator.sections.base import BaseSection


class CertificationsSection(BaseSection):
    """Handler for the certifications section of the resume."""

    def __init__(
        self, pdf, data: List[LicensesAndCertifications], styles: dict, config: dict
    ):
        """Initialize the certifications section handler.

        Args:
            pdf: The PDF document object.
            data (List[LicensesAndCertifications]): List of certification entries.
            styles (dict): Style definitions for this section.
            config (dict): Template configuration settings.
        """
        super().__init__(pdf, data, styles["certifications"], config)

    def add_section(self) -> None:
        """Add the certifications section to the PDF."""
        # Add section header
        self.add_cell("Certifications", "section_header", height=8)

        # Add each certification entry
        for cert in self.data:
            if cert.include:
                # Add certification name
                self.add_cell(cert.name, "name", height=5)

                # Add issuer
                self.add_multi_cell(cert.issuer, "issuer")

                # Add issue date and credential ID
                self.add_multi_cell(cert.issued_on, "details")
                self.add_multi_cell(cert.credential_id, "details")

                # Add spacing between certifications
                self.add_cell("", "details", height=5)
