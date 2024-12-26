# Dynamic Resume Generator

A powerful tool that generates professionally formatted PDF resumes from a JSON template, with support for multiple design templates and extensive customization options.

## Features

- **Multiple Design Templates**: Choose between different resume styles (modern, minimal)
- **Customizable Layouts**: Configure fonts, colors, spacing, and more via YAML
- **Smart Data Validation**: Ensures your resume data follows best practices
- **ATS-Friendly**: Generated PDFs are optimized for Applicant Tracking Systems
- **Section Control**: Enable/disable sections using `include` flags
- **Organized Output**: Resumes are automatically organized by company and job
- **CLI Interface**: Flexible command-line options for easy integration

## Installation & Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management and Python version control.

### Prerequisites

1. Install uv if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### Project Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Dynamic-Resume-Generator
   ```

2. Initialize uv project:
   ```bash
   uv init
   ```

3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

4. Set up Python 3.13:
   ```bash
   # Check available Python versions
   uv python list

   # Install Python 3.13 if not available
   uv python install 3.13

   # Pin project to Python 3.13
   uv python pin 3.13
   ```

5. Create your resume:
   - Copy `demo.json` to `resume.json`
   - Fill in your information following the demo format
   - Use `"include": true/false` to control what appears in the generated PDF

### Development Setup

If you're contributing to development:

1. Compile requirements from pyproject.toml:
   ```bash
   uv pip compile --python 3.13 pyproject.toml -o requirements.txt
   ```

2. Install development dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

## Usage

Basic usage:
```bash
uv run main.py
```

Advanced options:
```bash
uv run main.py --input resume.json --template modern --output-dir ./my-resumes
```

Available arguments:
- `--input`, `-i`: Path to input JSON file (default: resume.json)
- `--config`, `-c`: Path to config file (default: config.yaml)
- `--template`, `-t`: Template to use (e.g., modern, minimal)
- `--output-dir`, `-o`: Output directory for generated resumes

## Resume Structure

The `resume.json` file contains sections for:

### Application Info
- Company name
- Job title

### General Information
- Name
- Professional title
- Location
- Contact details (email, phone)
- Online presence (portfolio, LinkedIn, GitHub)
- Professional summary

### Experience Sections
- **Jobs**: Work experience with company, title, dates, and descriptions
- **Education**: Academic background with institutions and degrees
- **Certifications**: Professional certifications and licenses
- **Projects**: Notable projects with descriptions and technologies
- **Volunteer Experience**: Community involvement and contributions
- **Awards**: Honors and recognition
- **Languages**: Language proficiency levels

Each section and item supports an `include` flag for easy customization.

## Data Validation

The generator enforces several validation rules to ensure professional quality:

- **Dates**: Must use YYYY-MM format (e.g., "2023-12")
- **URLs**: Must be valid HTTP/HTTPS URLs
- **Email**: Must be a valid email address
- **Phone**: Optional, but must follow international format if provided
- **Language Proficiency**: Must use standard levels (Native, Professional, etc.)
- **Employment Types**: Must use standard types (Full-time, Part-time, etc.)

## Templates

### Modern Template
- Professional design with colored section headers
- Emphasis on work experience and skills
- Ideal for technical and corporate positions

### Minimal Template
- Clean, straightforward layout
- Monochromatic color scheme
- Perfect for academic or traditional industries

## Configuration

The `config.yaml` file allows customization of:

- Output directory structure
- File naming patterns
- PDF format and dimensions
- Font selections and sizes
- Color schemes
- Section spacing
- Error messages

## Example Output Structure

Generated resumes are organized as:
```
generated_applications/
  company_name/
    job_title/
      Resume - Name - Company - Job - Date.pdf
```

## Example Resume

![resume example](./media/resume_example.png)

## Testing

The project uses pytest for testing. To run the tests:

```bash
# Install test dependencies
uv pip install -r requirements.txt

# Run tests
pytest
```

Test coverage includes:
- Configuration loading and validation
- Resume data parsing and validation
- PDF generation and output handling
- Directory structure management

## Security

This project follows security best practices:

- **Input Validation**: All user input is validated through Pydantic models
- **File Operations**: Secure file handling with proper error handling and permissions
- **Dependencies**: Regular security audits of dependencies using `safety`:
  ```bash
  pip install safety
  safety check -r requirements.txt
  ```
- **Configuration**: No sensitive data in configuration files
- **Error Handling**: Secure error messages that don't expose system details

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

Areas for contribution:
- Templates
- Validation rules
- Documentation
- Bug fixes
- Test coverage improvements

## Note

The script expects all top-level sections in `resume.json` to be present, even if empty. See `demo.json` for the expected structure.
