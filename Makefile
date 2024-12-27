# Dynamic Resume Generator CLI

.PHONY: venv install run run-custom

# Default values for CLI arguments
INPUT := resume.json
CONFIG := config.yaml
TEMPLATE := modern
OUTPUT := ./generated_applications

# Create virtual environment
venv:
	uv venv

# Install package in development mode using uv
install: venv
	uv pip install -e .

# Run resume generator with default settings
run: install
	. .venv/bin/activate && uv run -m resume_generator.main

# Run resume generator with custom settings
# Usage: make run-custom INPUT=path/to/resume.json TEMPLATE=modern OUTPUT=./my-resumes CONFIG=path/to/config.yaml
run-custom: install
	. .venv/bin/activate && uv run -m resume_generator.main \
		--input $(INPUT) \
		--config $(CONFIG) \
		--template $(TEMPLATE) \
		--output-dir $(OUTPUT)
