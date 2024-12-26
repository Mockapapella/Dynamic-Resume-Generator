import json
from schemas import (
    ApplicationInfo, General, Jobs, Education,
    LicensesAndCertifications, VolunteerExperience,
    Projects, HonorsAndAwards, Languages
)

def test_demo_json_validation():
    """Test that demo.json matches our schema definitions"""
    with open('demo.json', 'r') as f:
        data = json.load(f)

    # Validate each section
    ApplicationInfo.model_validate(data["ApplicationInfo"])
    General.model_validate(data["General"])

    # Validate lists of items
    for job in data["Jobs"].values():
        Jobs.model_validate(job)

    for edu in data["Education"].values():
        Education.model_validate(edu)

    for cert in data["LicensesAndCertifications"].values():
        LicensesAndCertifications.model_validate(cert)

    for exp in data["VolunteerExperience"].values():
        VolunteerExperience.model_validate(exp)

    for proj in data["Projects"].values():
        Projects.model_validate(proj)

    for award in data["HonorsAndAwards"].values():
        HonorsAndAwards.model_validate(award)

    for lang in data["Languages"].values():
        Languages.model_validate(lang)
