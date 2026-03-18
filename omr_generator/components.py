"""
PDF components for OMR sheets.
"""

import io
import json
from typing import Dict, List, Tuple, Optional

import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from datetime import datetime

from .constants import LayoutConstants
from .models import ExamConfig, QuestionSection


class BaseComponent:
    """Base class for all PDF components."""
    
    def __init__(self, x: float, y: float, width: float, height: float, section_id: int = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.section_id = section_id

    def _get_corners(self) -> List[Tuple[float, float, int, int]]:
        """Get corner coordinates with direction indicators."""
        return [
            (self.x, self.y, 1, 1),
            (self.x + self.width, self.y, -1, 1),
            (self.x, self.y + self.height, 1, -1),
            (self.x + self.width, self.y + self.height, -1, -1)
        ]

    def draw_unique_markers(self, c: canvas.Canvas) -> None:
        """Draw section markers for identification."""
        if self.section_id == 0:
            return
            
        marker_size = LayoutConstants.TRIM_MARKER_SIZE
        dot_radius = 0.6 * mm
        
        c.setStrokeColor(colors.black)
        c.setLineWidth(1.2)
        
        for cx, cy, dx, dy in self._get_corners():
            c.line(cx - (dx*0.5*mm), cy - (dy*0.5*mm), cx + (dx*marker_size), cy - (dy*0.5*mm))
            c.line(cx - (dx*0.5*mm), cy - (dy*0.5*mm), cx - (dx*0.5*mm), cy + (dy*marker_size))
            
            c.setFillColor(colors.black)
            for i in range(self.section_id):
                dot_x = cx + (dx * (marker_size + 2.5*mm + (i*2*mm)))
                dot_y = cy - (dy * 0.5*mm)
                c.circle(dot_x, dot_y, dot_radius, fill=1, stroke=0)
    
    def render(self, c: canvas.Canvas) -> None:
        """Render the component. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement render()")


class HeaderComponent(BaseComponent):
    """Header component displaying exam title and subject information."""
    
    def __init__(self, x: float, y: float, width: float, height: float, 
                 exam_title: str, subject_info: str):
        super().__init__(x, y, width, height, section_id=0)
        self.exam_title = exam_title
        self.subject_info = subject_info

    def render(self, c: canvas.Canvas) -> None:
        center_x = self.x + self.width / 2
        
        c.setFillColor(colors.black)
        c.setFont(LayoutConstants.FONT_BOLD, 26)
        c.drawCentredString(center_x, self.y + self.height - 10*mm, self.exam_title)
        
        c.setFont(LayoutConstants.FONT_NORMAL, 20)
        c.drawCentredString(center_x, self.y + 2*mm, self.subject_info)


class StudentIDComponent(BaseComponent):
    """Student ID section with QR code."""
    
    def __init__(self, x: float, y: float, width: float, height: float,
                 student: Dict[str, str], exam_config: ExamConfig):
        super().__init__(x, y, width, height, section_id=1)
        self.student = student or {}
        self.exam_config = exam_config
        self.has_data = bool(student and student.get('id'))

    def _generate_qr_code(self) -> ImageReader:
        """Generate QR code with exam and student data."""
        qr_data = {
            "student_id": self.student.get('id', ''),
            "student_name": self.student.get('name', ''),
            "room": self.student.get('room', ''),
            "number": self.student.get('number', ''),
            "exam_code": self.exam_config.exam_code,
            "exam_date": self.exam_config.exam_date,
            "subject": self.exam_config.subject_name,
            "timestamp": datetime.now().isoformat()
        }
        
        qr = qrcode.QRCode(version=2, box_size=10, border=0)
        qr.add_data(json.dumps(qr_data, ensure_ascii=False))
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        buf = io.BytesIO()
        qr_img.save(buf, format='PNG')
        buf.seek(0)
        return ImageReader(buf)

    def render(self, c: canvas.Canvas) -> None:
        self.draw_unique_markers(c)
        
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.5)
        c.rect(self.x, self.y, self.width, self.height)
        
        qr_size = self.height - 6*mm
        
        # QR Code
        if self.has_data:
            qr_image = self._generate_qr_code()
            c.drawImage(qr_image, self.x + 3*mm, self.y + 3*mm, width=qr_size, height=qr_size)
        else:
            c.setStrokeColor(colors.lightgrey)
            c.setLineWidth(0.3)
            c.rect(self.x + 3*mm, self.y + 3*mm, qr_size, qr_size)
        
        # Student Info
        info_x = self.x + qr_size + 8*mm
        line_width = self.width - qr_size - 50*mm
        
        c.setFont(LayoutConstants.FONT_BOLD, 22)
        c.drawString(info_x, self.y + self.height - 10*mm, "ชื่อ: ")
        
        if self.has_data and self.student.get('name'):
            c.drawString(info_x + 12*mm, self.y + self.height - 10*mm, self.student['name'])
        else:
            c.setStrokeColor(colors.black)
            c.setLineWidth(0.5)
            c.line(info_x + 12*mm, self.y + self.height - 11*mm, 
                   info_x + line_width, self.y + self.height - 11*mm)
        
        c.setFont(LayoutConstants.FONT_NORMAL, 19)
        c.drawString(info_x, self.y + 5*mm, "ชั้น: ")
        
        if self.has_data and self.student.get('room'):
            c.drawString(info_x + 12*mm, self.y + 5*mm, self.student['room'])
        else:
            c.setStrokeColor(colors.black)
            c.setLineWidth(0.5)
            c.line(info_x + 12*mm, self.y + 4*mm, 
                   info_x + line_width, self.y + 4*mm)
        
        # Number Box
        box_width = 30 * mm
        box_x = self.x + self.width - box_width - 5*mm
        
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.5)
        c.rect(box_x, self.y + 2*mm, box_width, self.height - 4*mm)
        
        c.setFont(LayoutConstants.FONT_BOLD, 16)
        c.drawCentredString(box_x + box_width/2, self.y + self.height - 6*mm, "เลขที่")
        
        if self.has_data and self.student.get('number'):
            c.setFont(LayoutConstants.FONT_BOLD, 69)
            c.drawCentredString(box_x + box_width/2, self.y + 3*mm, str(self.student['number']))


class AnswerSheetComponent(BaseComponent):
    """Answer section with multiple choice bubbles."""
    
    COLUMNS = 2
    
    def __init__(self, x: float, y: float, width: float, height: float,
                 num_questions: int, choices: List[str], 
                 sections: List[QuestionSection] = None,
                 answer_key: List[int] = None):
        super().__init__(x, y, width, height, section_id=2)
        self.num_questions = num_questions
        self.choices = choices
        self.sections = sections or []
        self.answer_key = answer_key
        self.questions_per_column = (num_questions + 1) // 2
        self.question_height = self._calculate_question_height()
        self.bubble_spacing = self._calculate_bubble_spacing()

    def _calculate_question_height(self) -> float:
        available_height = self.height - 20*mm
        max_rows = max(self.questions_per_column, 1)
        return min(available_height / max_rows, 14.5 * mm)
    
    def _calculate_bubble_spacing(self) -> float:
        if len(self.choices) == 2:
            max_label_len = max(len(choice) for choice in self.choices)
            if max_label_len > 2:
                return 20 * mm
            return 15 * mm
        elif len(self.choices) == 3:
            return 15 * mm
        elif len(self.choices) == 4:
            return 13 * mm
        else:
            return 11 * mm

    def _get_section_for_question(self, question_num: int) -> Optional[QuestionSection]:
        for section in self.sections:
            if section.start_question <= question_num <= section.end_question:
                return section
        return None

    def _draw_question_row(self, c: canvas.Canvas, col_x: float, 
                          question_num: int, row_y: float) -> None:
        c.setFont(LayoutConstants.FONT_BOLD, 24)
        c.setFillColor(colors.black)
        c.drawCentredString(col_x + 10*mm, row_y - 1.5*mm, f"{question_num}.")
        
        max_label_len = max(len(choice) for choice in self.choices)
        font_size = 18 if max_label_len > 2 else 24
        
        for i, choice in enumerate(self.choices):
            bubble_x = col_x + 28*mm + (i * self.bubble_spacing)
            
            is_correct = (self.answer_key and 
                         question_num <= len(self.answer_key) and 
                         self.answer_key[question_num - 1] == i)
            
            c.setStrokeColor(colors.black)
            if is_correct:
                c.setFillColor(colors.black)
                c.circle(bubble_x, row_y, LayoutConstants.BUBBLE_DIAMETER/2, fill=1, stroke=1)
            else:
                c.circle(bubble_x, row_y, LayoutConstants.BUBBLE_DIAMETER/2, fill=0, stroke=1)
            
            c.setFont(LayoutConstants.FONT_NORMAL, font_size)
            c.setFillColor(colors.gray if not is_correct else colors.white)
            c.drawCentredString(bubble_x, row_y - 1.8*mm, choice)

    def render(self, c: canvas.Canvas) -> None:
        self.draw_unique_markers(c)
        
        c.setLineWidth(0.5)
        c.rect(self.x, self.y, self.width, self.height)
        
        col_width = self.width / self.COLUMNS
        start_y = self.y + self.height - 15 * mm
        
        # Draw choice headers
        for col_idx in range(self.COLUMNS):
            col_x = self.x + (col_idx * col_width)
            c.setFillColor(colors.black)
            max_label_len = max(len(choice) for choice in self.choices)
            font_size = 20 if max_label_len > 2 else 24
            c.setFont(LayoutConstants.FONT_BOLD, font_size)
            
            for i, choice in enumerate(self.choices):
                c.drawCentredString(col_x + 28*mm + (i * self.bubble_spacing), 
                                  start_y + 3*mm, choice)
        
        # Draw questions
        for col_idx in range(self.COLUMNS):
            col_x = self.x + (col_idx * col_width)
            questions_in_col = self.questions_per_column if col_idx == 0 else self.num_questions - self.questions_per_column
            
            for q_idx in range(questions_in_col):
                question_num = (col_idx * self.questions_per_column) + q_idx + 1
                if question_num > self.num_questions:
                    break
                
                row_y = start_y - (q_idx * self.question_height) - (self.question_height / 2)
                self._draw_question_row(c, col_x, question_num, row_y)


class EssayComponent(BaseComponent):
    """Section for essay/written answers."""
    
    def __init__(self, x: float, y: float, width: float, height: float, 
                 num_lines: int = 3, title: str = "ส่วนเขียนตอบ"):
        super().__init__(x, y, width, height, section_id=0)
        self.num_lines = num_lines
        self.title = title

    def render(self, c: canvas.Canvas) -> None:
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.5)
        c.rect(self.x, self.y, self.width, self.height)
        
        c.setFont(LayoutConstants.FONT_BOLD, 20)
        c.setFillColor(colors.black)
        c.drawString(self.x + 5*mm, self.y + self.height - 8*mm, self.title)
        
        line_spacing = (self.height - 15*mm) / self.num_lines
        start_y = self.y + self.height - 15*mm
        
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.5)
        
        for i in range(self.num_lines):
            line_y = start_y - (i * line_spacing)
            c.line(self.x + 5*mm, line_y, self.x + self.width - 5*mm, line_y)


class FooterComponent(BaseComponent):
    """Footer with instructions and score box."""
    
    def render(self, c: canvas.Canvas) -> None:
        c.setLineWidth(0.5)
        c.setStrokeColor(colors.black)
        
        c.setFont(LayoutConstants.FONT_BOLD, 18)
        c.drawString(self.x + 5*mm, self.y + self.height - 8*mm, "วิธีการระบายที่ถูกต้อง:")
        
        c.setFont(LayoutConstants.FONT_NORMAL, 17)
        c.drawString(self.x + 45*mm, self.y + self.height - 8*mm, "ถูกต้อง")
        c.setFillColor(colors.black)
        c.circle(self.x + 60*mm, self.y + self.height - 6.5*mm, 3*mm, fill=1, stroke=1)
        
        c.setFillColor(colors.black)
        c.drawString(self.x + 75*mm, self.y + self.height - 8*mm, "ผิด")
        
        c.circle(self.x + 85*mm, self.y + self.height - 6.5*mm, 3*mm, fill=0, stroke=1)
        c.setLineWidth(0.8)
        c.line(self.x + 83*mm, self.y + self.height - 8.5*mm, self.x + 87*mm, self.y + self.height - 4.5*mm)
        c.line(self.x + 83*mm, self.y + self.height - 4.5*mm, self.x + 87*mm, self.y + self.height - 8.5*mm)
        
        c.circle(self.x + 95*mm, self.y + self.height - 6.5*mm, 3*mm, fill=0, stroke=1)
        c.line(self.x + 93.5*mm, self.y + self.height - 7*mm, self.x + 95*mm, self.y + self.height - 9*mm)
        c.line(self.x + 95*mm, self.y + self.height - 9*mm, self.x + 97.5*mm, self.y + self.height - 4*mm)

        c.setFont(LayoutConstants.FONT_NORMAL, 16)
        c.drawString(self.x + 5*mm, self.y + 2*mm, 
                    "* ใช้ดินสอ 2B เท่านั้น และหากต้องการแก้ไขให้ใช้ยางลบลบให้สะอาดที่สุด")
        
        box_width, box_height = 40*mm, 15*mm
        box_x = self.x + self.width - box_width
        box_y = self.y + 2*mm
        
        c.setLineWidth(0.5)
        c.rect(box_x, box_y, box_width, box_height)
        
        c.setFont(LayoutConstants.FONT_BOLD, 14)
        c.drawCentredString(box_x + box_width/2, box_y + box_height - 4*mm, "คะแนน / Score")
