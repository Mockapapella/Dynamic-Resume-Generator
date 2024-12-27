"""Modern style template for resume generation."""

STYLES = {
    "general": {
        "name": {"font": "DejaVuSans-Bold", "size": 14},  # Largest text for name
        "title": {"font": "DejaVuSans-Bold", "size": 10},
        "contact": {"font": "DejaVuSans", "size": 8},
        "description_header": {"font": "DejaVuSans-Bold", "size": 10},
        "description": {"font": "DejaVuSans", "size": 8},
        "link": {"font": "DejaVuSans", "size": 8, "color": (0, 102, 204)},  # Matching other section links
    },
    "jobs": {
        "section_header": {"font": "DejaVuSans-Bold", "size": 12, "color": (0, 51, 102)},  # Dark blue for headers
        "title": {"font": "DejaVuSans-Bold", "size": 9},
        "company": {"font": "DejaVuSans", "size": 8},
        "details": {"font": "DejaVuSans", "size": 8},
    },
    "education": {
        "section_header": {"font": "DejaVuSans-Bold", "size": 12, "color": (0, 51, 102)},
        "school": {"font": "DejaVuSans-Bold", "size": 9},
        "field": {"font": "DejaVuSans", "size": 8},
        "details": {"font": "DejaVuSans", "size": 8},
    },
    "certifications": {
        "section_header": {"font": "DejaVuSans-Bold", "size": 12, "color": (0, 51, 102)},
        "name": {"font": "DejaVuSans-Bold", "size": 9},
        "issuer": {"font": "DejaVuSans", "size": 8},
        "details": {"font": "DejaVuSans", "size": 8},
    },
    "volunteering": {
        "section_header": {"font": "DejaVuSans-Bold", "size": 12, "color": (0, 51, 102)},
        "organization": {"font": "DejaVuSans-Bold", "size": 9},
        "role": {"font": "DejaVuSans", "size": 8},
        "details": {"font": "DejaVuSans", "size": 8},
    },
    "projects": {
        "section_header": {"font": "DejaVuSans-Bold", "size": 12, "color": (0, 51, 102)},
        "name": {"font": "DejaVuSans-Bold", "size": 9},
        "link": {"font": "DejaVuSans", "size": 8, "color": (0, 102, 204)},  # Lighter blue for links
        "details": {"font": "DejaVuSans", "size": 8},
    },
    "awards": {
        "section_header": {"font": "DejaVuSans-Bold", "size": 12, "color": (0, 51, 102)},
        "title": {"font": "DejaVuSans-Bold", "size": 9},
        "issuer": {"font": "DejaVuSans", "size": 8},
        "details": {"font": "DejaVuSans", "size": 8},
    },
    "languages": {
        "section_header": {"font": "DejaVuSans-Bold", "size": 12, "color": (0, 51, 102)},
        "language": {"font": "DejaVuSans-Bold", "size": 9},
        "proficiency": {"font": "DejaVuSans", "size": 8},
    },
    "articles": {
        "section_header": {"font": "DejaVuSans-Bold", "size": 12, "color": (0, 51, 102)},
        "title": {"font": "DejaVuSans-Bold", "size": 9},
        "publication": {"font": "DejaVuSans", "size": 8},
        "details": {"font": "DejaVuSans", "size": 8},
        "link": {"font": "DejaVuSans", "size": 8, "color": (0, 102, 204)},
    },
}
