"""
Data models for OMR generation.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class StudentData:
    """Student information."""
    id: str = ""
    name: str = ""
    room: str = ""
    number: str = ""


@dataclass
class QuestionSection:
    """Represents a section of questions with scoring."""
    name: str
    start_question: int
    end_question: int
    max_score: int


@dataclass
class ExamConfig:
    """Configuration for exam generation."""
    exam_title: str
    subject_name: str
    exam_date: str = ""
    exam_code: str = ""
    academic_year: str = "2569"
    sections: List[QuestionSection] = field(default_factory=list)
