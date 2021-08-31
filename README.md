# What is this?

Dynamic Resume Generator is a tool that I built out of frustration from applying for jobs. Some things that I've done that are super relevant to the job I am applying for right now will be completely irrelevant to the next job. Rather than manually recreating a new resume for every single job posting (and having to deal with the subsequent clutter), I put all of my experience, awards, projects etc. into a single JSON file and run a script to generate a topical resume. Generated resumes are located in:

```
generated_applications > company name > job name
```

It isn't very fault tolerant and expects all top level arguments within `demo.json` or `resume.json` to be present, so keep that in mind if you are looking to remove anything from the JSON files. It's only a single file script, so if you want to modify any of it to suite your needs it should be fairly simple.

# Requirements

It uses `python-docx` to create the files. To use this tool you must have Microsoft Office installed. All instances of Microsoft Word close when this application runs, so make sure you have saved any unsaved documents. As a result, this script only runs on Windows.

# Example

![resume example](./media/resume_example.png)

# Setup

This script uses Python 3.9.6. Make sure you have Microsoft Office Installed. Once cloned, enter:

```
python -m venv venv
source venv/Scripts/activate
```

Install requirements:

```
pip install -r requirements.txt
```

Run script:

```
python main.py
```

By default it generates a demo resume. To create your own, copy `demo.json` and rename it to `resume.json`. All you need to do from here is copy the format outline in the demo and you should be good to go!
