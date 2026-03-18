"""
Core OMR generator functionality.
"""

import io
import os
import csv
from typing import Dict, List, Optional

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from .fonts import FontManager
from .constants import LayoutConstants, ChoicePresets
from .models import ExamConfig, StudentData
from .components import (
    HeaderComponent, StudentIDComponent, AnswerSheetComponent,
    EssayComponent, FooterComponent
)


class OMRGenerator:
    """Main OMR sheet generator."""
    
    HEADER_HEIGHT = 22 * mm
    
    def __init__(self):
        """Initialize the OMR generator."""
        FontManager.register_fonts()
        self.page_width, self.page_height = A4
        self.margin = 18 * mm

    def _draw_fiducial_markers(self, c: canvas.Canvas) -> None:
        """Draw corner alignment markers."""
        size = LayoutConstants.FIDUCIAL_SIZE
        positions = [
            (5*mm, 5*mm),
            (self.page_width - 15*mm, 5*mm),
            (5*mm, self.page_height - 15*mm),
            (self.page_width - 15*mm, self.page_height - 15*mm)
        ]
        
        for x, y in positions:
            c.rect(x, y, size, size, fill=1)

    def generate(self, 
                exam_config: ExamConfig,
                filename: str,
                student: Optional[StudentData] = None,
                num_questions: int = 20,
                choices: Optional[List[str]] = None,
                answer_key: Optional[List[int]] = None,
                include_essay: bool = False,
                essay_lines: int = 3) -> None:
        """
        Generate a single OMR sheet.
        
        Args:
            exam_config: Exam configuration
            filename: Output PDF filename
            student: Student data (optional, creates blank sheet if None)
            num_questions: Number of questions
            choices: Choice labels (defaults to Thai 4 choices)
            answer_key: List of correct answer indices for answer key
            include_essay: Include essay section
            essay_lines: Number of lines in essay section
        """
        choices = choices or ChoicePresets.THAI_4
        student_dict = self._student_to_dict(student)
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        self._draw_fiducial_markers(c)
        
        content_width = self.page_width - 2 * self.margin
        
        # Header
        header_y = self.page_height - self.margin - self.HEADER_HEIGHT
        subject_info = f"รายวิชา: {exam_config.subject_name} | ปีการศึกษา {exam_config.academic_year}"
        if exam_config.exam_date:
            subject_info += f" | วันที่สอบ: {exam_config.exam_date}"
        
        HeaderComponent(self.margin, header_y, content_width, self.HEADER_HEIGHT,
                       exam_config.exam_title, subject_info).render(c)
        
        # Student ID
        id_y = header_y - LayoutConstants.ID_SECTION_HEIGHT - 6*mm
        StudentIDComponent(self.margin, id_y, content_width,
                          LayoutConstants.ID_SECTION_HEIGHT, 
                          student_dict, exam_config).render(c)
        
        # Footer
        footer_y = self.margin + 2*mm
        FooterComponent(self.margin, footer_y, content_width,
                       LayoutConstants.FOOTER_HEIGHT).render(c)
        
        # Answer Section
        if include_essay:
            answer_height = 120 * mm
            essay_height = 40 * mm
            answer_y = footer_y + LayoutConstants.FOOTER_HEIGHT + 4*mm
            
            AnswerSheetComponent(self.margin, answer_y, content_width, answer_height,
                               num_questions, choices, exam_config.sections, 
                               answer_key).render(c)
            
            essay_y = answer_y + answer_height + 4*mm
            EssayComponent(self.margin, essay_y, content_width, essay_height,
                          essay_lines).render(c)
        else:
            answer_y = footer_y + LayoutConstants.FOOTER_HEIGHT + 4*mm
            AnswerSheetComponent(self.margin, answer_y, content_width,
                               LayoutConstants.ANSWER_SECTION_HEIGHT,
                               num_questions, choices, exam_config.sections,
                               answer_key).render(c)
        
        c.save()
        
        with open(filename, "wb") as f:
            f.write(buffer.getvalue())

    def generate_batch(self,
                      exam_config: ExamConfig,
                      students: List[StudentData],
                      output_dir: str,
                      num_questions: int = 20,
                      choices: Optional[List[str]] = None,
                      include_essay: bool = False) -> List[str]:
        """
        Generate OMR sheets for multiple students.
        
        Args:
            exam_config: Exam configuration
            students: List of student data
            output_dir: Output directory for PDFs
            num_questions: Number of questions
            choices: Choice labels
            include_essay: Include essay section
            
        Returns:
            List of generated filenames
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        generated_files = []
        choices = choices or ChoicePresets.THAI_4
        
        for student in students:
            safe_room = student.room.replace('/', '-').replace(' ', '_')
            safe_name = student.name.replace(' ', '_')
            filename = os.path.join(output_dir, 
                                   f"omr_{safe_room}_no{student.number}_{safe_name}.pdf")
            
            self.generate(exam_config, filename, student, num_questions, 
                        choices, include_essay=include_essay)
            generated_files.append(filename)
        
        return generated_files

    def generate_batch_from_csv(self,
                               exam_config: ExamConfig,
                               csv_file: str,
                               output_dir: str,
                               num_questions: int = 20,
                               choices: Optional[List[str]] = None,
                               include_essay: bool = False) -> List[str]:
        """
        Generate OMR sheets from CSV file.
        
        CSV format: id, name, room, number
        
        Args:
            exam_config: Exam configuration
            csv_file: Path to CSV file
            output_dir: Output directory
            num_questions: Number of questions
            choices: Choice labels
            include_essay: Include essay section
            
        Returns:
            List of generated filenames
        """
        students = []
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append(StudentData(
                    id=row.get('id', ''),
                    name=row.get('name', ''),
                    room=row.get('room', ''),
                    number=row.get('number', '')
                ))
        
        return self.generate_batch(exam_config, students, output_dir, 
                                  num_questions, choices, include_essay)

    def generate_answer_key(self,
                           exam_config: ExamConfig,
                           filename: str,
                           num_questions: int,
                           choices: List[str],
                           answer_key: List[int]) -> None:
        """
        Generate answer key sheet with correct answers filled.
        
        Args:
            exam_config: Exam configuration
            filename: Output filename
            num_questions: Number of questions
            choices: Choice labels
            answer_key: List of correct answer indices (0-based)
        """
        answer_key_student = StudentData(
            id='ANSWER_KEY',
            name='เฉลยคำตอบ',
            room='ANSWER KEY',
            number='0'
        )
        
        self.generate(exam_config, filename, answer_key_student, 
                     num_questions, choices, answer_key)

    @staticmethod
    def _student_to_dict(student: Optional[StudentData]) -> Dict[str, str]:
        """Convert StudentData to dict."""
        if student is None:
            return {}
        return {
            'id': student.id,
            'name': student.name,
            'room': student.room,
            'number': student.number
        }
