from pydantic import BaseModel
from pydantic import Field
from typing import Optional
from typing import List


class ApplicationInfo(BaseModel):
    company: str
    job: str


class General(BaseModel):
    name: str
    title: str
    location: str
    email: str
    cell_number: str
    portfolio: str
    linkedin: str
    github: str
    description: str


class Jobs(BaseModel):
    include: bool
    title: str
    company: str
    employment_type: str
    duration: List[str] = Field(max_length=2)
    reference: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[List[str]] = None


class Education(BaseModel):
    include: bool
    school: str
    degree: Optional[str] = None
    field: str
    duration: List[str] = Field(max_length=2)
    gpa: Optional[str] = None
    activities_and_societies: Optional[List[str]]
    description: Optional[str] = None


class LicensesAndCertifications(BaseModel):
    include: bool
    name: str
    issuer: str
    issued_on: str
    credential_id: str


class VolunteerExperience(BaseModel):
    include: bool
    organization: str
    role: str
    cause: str
    duration: List[str] = Field(max_length=2)
    description: Optional[str] = None


class Projects(BaseModel):
    include: bool
    name: str
    duration: List[str] = Field(max_length=2)
    link: Optional[str]
    description: str
    skills: List[str]


class HonorsAndAwards(BaseModel):
    include: bool
    title: str
    issuer: str
    issued_on: str
    description: str


class Languages(BaseModel):
    include: bool
    language: str
    proficiency: str
