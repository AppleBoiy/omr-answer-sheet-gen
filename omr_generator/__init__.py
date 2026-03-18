"""
OMR Generator - Thai OMR Answer Sheet Generator
A comprehensive system for generating OMR (Optical Mark Recognition) answer sheets.
"""

from .core import OMRGenerator
from .models import ExamConfig, QuestionSection, StudentData
from .constants import LayoutConstants, ChoicePresets

__version__ = "1.0.0"
__all__ = [
    "OMRGenerator",
    "ExamConfig", 
    "QuestionSection",
    "StudentData",
    "LayoutConstants",
    "ChoicePresets"
]
