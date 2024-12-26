from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, EmailStr, field_validator
from typing import Dict, Optional, List, Union
import re

# Constants
PROFICIENCY_LEVELS = [
    "Native or Bilingual",
    "Full Professional",
    "Professional Working",
    "Limited Working",
    "Elementary"
]

EMPLOYMENT_TYPES = [
    "Full-time",
    "Part-time",
    "Self-employed",
    "Freelance",
    "Contract",
    "Internship",
    "Apprenticeship",
    "Seasonal"
]

class ApplicationInfo(BaseModel):
    company: str = Field(..., min_length=1)
    job: str = Field(..., min_length=1)

class General(BaseModel):
    name: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    email: EmailStr
    cell_number: Optional[str] = None
    portfolio: HttpUrl
    linkedin: HttpUrl
    github: HttpUrl
    description: str = Field(..., min_length=10)

    @field_validator('cell_number')
    def validate_phone(cls, v):
        if v is None:
            return v
        pattern = re.compile(r'^\+?1?\d{9,15}$')
        if not pattern.match(v):
            raise ValueError('Invalid phone number format')
        return v

class Reference(BaseModel):
    name: str
    position: str
    number: Optional[str] = None
    web: Optional[HttpUrl] = None

    @field_validator('number')
    def validate_phone(cls, v):
        if v is None:
            return v
        pattern = re.compile(r'^\+?1?\d{9,15}$')
        if not pattern.match(v):
            raise ValueError('Invalid phone number format')
        return v

class DateRange(BaseModel):
    start: str
    end: str = "Present"

    @field_validator('start', 'end')
    def validate_date(cls, v):
        if v.lower() == "present":
            return v
        try:
            datetime.strptime(v, '%Y-%m')
            return v
        except ValueError:
            raise ValueError('Invalid date format. Use YYYY-MM or "Present"')

class Jobs(BaseModel):
    include: bool = True
    title: str = Field(..., min_length=1)
    company: str = Field(..., min_length=1)
    employment_type: str = Field(..., min_length=1)
    duration: List[str] = Field(..., max_length=2)
    references: Optional[List[Reference]] = None
    description: Optional[str] = None
    skills: Optional[List[str]] = None

    @field_validator('employment_type')
    def validate_employment_type(cls, v):
        if v not in EMPLOYMENT_TYPES:
            raise ValueError(f'Invalid employment type. Must be one of: {", ".join(EMPLOYMENT_TYPES)}')
        return v

    @field_validator('duration')
    def validate_duration(cls, v):
        if len(v) != 2:
            raise ValueError('Duration must have exactly 2 elements [start, end]')
        for date in v:
            if date.lower() != "present":
                try:
                    datetime.strptime(date, '%Y-%m')
                except ValueError:
                    raise ValueError('Invalid date format. Use YYYY-MM or "Present"')
        return v

class Education(BaseModel):
    include: bool = True
    school: str = Field(..., min_length=1)
    degree: Optional[str] = None
    field: str = Field(..., min_length=1)
    duration: List[str] = Field(..., max_length=2)
    gpa: Optional[str] = None
    activities_and_societies: Optional[List[str]] = None
    description: Optional[str] = None

    @field_validator('duration')
    def validate_duration(cls, v):
        if len(v) != 2:
            raise ValueError('Duration must have exactly 2 elements [start, end]')
        for date in v:
            if date.lower() != "present":
                try:
                    datetime.strptime(date, '%Y-%m')
                except ValueError:
                    raise ValueError('Invalid date format. Use YYYY-MM or "Present"')
        return v

    @field_validator('gpa')
    def validate_gpa(cls, v):
        if v is None:
            return v
        try:
            gpa = float(v)
            if not 0 <= gpa <= 4.0:
                raise ValueError('GPA must be between 0.0 and 4.0')
        except ValueError:
            raise ValueError('Invalid GPA format')
        return v

class LicensesAndCertifications(BaseModel):
    include: bool = True
    name: str = Field(..., min_length=1)
    issuer: str = Field(..., min_length=1)
    issued_on: str
    credential_id: str = Field(..., min_length=1)

    @field_validator('issued_on')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m')
            return v
        except ValueError:
            raise ValueError('Invalid date format. Use YYYY-MM')

class VolunteerExperience(BaseModel):
    include: bool = True
    organization: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)
    cause: str = Field(..., min_length=1)
    duration: List[str] = Field(..., max_length=2)
    description: Optional[str] = None

    @field_validator('duration')
    def validate_duration(cls, v):
        if len(v) != 2:
            raise ValueError('Duration must have exactly 2 elements [start, end]')
        for date in v:
            if date.lower() != "present":
                try:
                    datetime.strptime(date, '%Y-%m')
                except ValueError:
                    raise ValueError('Invalid date format. Use YYYY-MM or "Present"')
        return v

class Projects(BaseModel):
    include: bool = True
    name: str = Field(..., min_length=1)
    duration: List[str] = Field(..., max_length=2)
    link: Optional[HttpUrl] = None
    description: str = Field(..., min_length=10)
    skills: List[str] = Field(default_factory=list)

    @field_validator('duration')
    def validate_duration(cls, v):
        if len(v) != 2:
            raise ValueError('Duration must have exactly 2 elements [start, end]')
        for date in v:
            if date.lower() != "present":
                try:
                    datetime.strptime(date, '%Y-%m')
                except ValueError:
                    raise ValueError('Invalid date format. Use YYYY-MM or "Present"')
        return v

class HonorsAndAwards(BaseModel):
    include: bool = True
    title: str = Field(..., min_length=1)
    issuer: str = Field(..., min_length=1)
    issued_on: str
    description: str = Field(..., min_length=10)

    @field_validator('issued_on')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m')
            return v
        except ValueError:
            raise ValueError('Invalid date format. Use YYYY-MM')

class Languages(BaseModel):
    include: bool = True
    language: str = Field(..., min_length=1)
    proficiency: str = Field(..., min_length=1)

    @field_validator('proficiency')
    def validate_proficiency(cls, v):
        if v not in PROFICIENCY_LEVELS:
            raise ValueError(f'Invalid proficiency level. Must be one of: {", ".join(PROFICIENCY_LEVELS)}')
        return v
