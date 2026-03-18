"""
Basic usage examples for OMR Generator.
"""

from omr_generator import OMRGenerator, ExamConfig, StudentData, QuestionSection
from omr_generator.constants import ChoicePresets


def example_1_simple_sheet():
    """Generate a simple OMR sheet."""
    print("Example 1: Simple OMR sheet")
    
    generator = OMRGenerator()
    
    exam_config = ExamConfig(
        exam_title="สอบปลายภาคเรียนที่ 2",
        subject_name="วิทยาศาสตร์ (ป.4)",
        exam_date="15 มีนาคม 2569"
    )
    
    student = StudentData(
        id="CMU-69-001",
        name="เด็กชายรักเรียน ดีมาก",
        room="ป.4/1",
        number="1"
    )
    
    generator.generate(
        exam_config=exam_config,
        filename="output/simple_sheet.pdf",
        student=student,
        num_questions=20,
        choices=ChoicePresets.THAI_4
    )
    
    print("✓ Generated: output/simple_sheet.pdf\n")


def example_2_blank_sheet():
    """Generate a blank OMR sheet."""
    print("Example 2: Blank OMR sheet")
    
    generator = OMRGenerator()
    
    exam_config = ExamConfig(
        exam_title="สอบปลายภาคเรียนที่ 2",
        subject_name="คณิตศาสตร์ (ป.4)"
    )
    
    generator.generate(
        exam_config=exam_config,
        filename="output/blank_sheet.pdf",
        num_questions=20,
        choices=ChoicePresets.THAI_4
    )
    
    print("✓ Generated: output/blank_sheet.pdf\n")


def example_3_true_false():
    """Generate True/False OMR sheet."""
    print("Example 3: True/False sheet")
    
    generator = OMRGenerator()
    
    exam_config = ExamConfig(
        exam_title="แบบทดสอบถูก-ผิด",
        subject_name="สังคมศึกษา (ป.4)",
        exam_date="16 มีนาคม 2569"
    )
    
    generator.generate(
        exam_config=exam_config,
        filename="output/true_false.pdf",
        num_questions=15,
        choices=ChoicePresets.TRUE_FALSE
    )
    
    print("✓ Generated: output/true_false.pdf\n")


def example_4_with_sections():
    """Generate OMR with scoring sections."""
    print("Example 4: OMR with sections")
    
    generator = OMRGenerator()
    
    sections = [
        QuestionSection("ส่วนที่ 1: ไวยากรณ์", 1, 10, 10),
        QuestionSection("ส่วนที่ 2: การอ่าน", 11, 20, 10)
    ]
    
    exam_config = ExamConfig(
        exam_title="สอบปลายภาค",
        subject_name="ภาษาไทย (ป.4)",
        exam_date="17 มีนาคม 2569",
        exam_code="TH-P4-2569-02",
        sections=sections
    )
    
    student = StudentData(
        id="CMU-69-002",
        name="เด็กหญิงขยัน เรียนดี",
        room="ป.4/1",
        number="2"
    )
    
    generator.generate(
        exam_config=exam_config,
        filename="output/with_sections.pdf",
        student=student,
        num_questions=20,
        choices=ChoicePresets.THAI_4
    )
    
    print("✓ Generated: output/with_sections.pdf\n")


def example_5_with_essay():
    """Generate OMR with essay section."""
    print("Example 5: OMR with essay section")
    
    generator = OMRGenerator()
    
    exam_config = ExamConfig(
        exam_title="สอบปลายภาค",
        subject_name="ภาษาไทย (ป.4)",
        exam_date="18 มีนาคม 2569"
    )
    
    student = StudentData(
        id="CMU-69-003",
        name="เด็กชายฉลาด มากความรู้",
        room="ป.4/1",
        number="3"
    )
    
    generator.generate(
        exam_config=exam_config,
        filename="output/with_essay.pdf",
        student=student,
        num_questions=20,
        choices=ChoicePresets.THAI_4,
        include_essay=True,
        essay_lines=3
    )
    
    print("✓ Generated: output/with_essay.pdf\n")


def example_6_answer_key():
    """Generate answer key."""
    print("Example 6: Answer key")
    
    generator = OMRGenerator()
    
    exam_config = ExamConfig(
        exam_title="เฉลยข้อสอบ",
        subject_name="วิทยาศาสตร์ (ป.4)",
        exam_code="SCI-P4-2569-KEY"
    )
    
    # Answer key: 0=ก, 1=ข, 2=ค, 3=ง
    answer_key = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1,
                  2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
    
    generator.generate_answer_key(
        exam_config=exam_config,
        filename="output/answer_key.pdf",
        num_questions=20,
        choices=ChoicePresets.THAI_4,
        answer_key=answer_key
    )
    
    print("✓ Generated: output/answer_key.pdf\n")


def example_7_english_choices():
    """Generate OMR with English choices."""
    print("Example 7: English choices")
    
    generator = OMRGenerator()
    
    exam_config = ExamConfig(
        exam_title="English Test",
        subject_name="English (Grade 4)",
        exam_date="March 19, 2026"
    )
    
    generator.generate(
        exam_config=exam_config,
        filename="output/english_test.pdf",
        num_questions=15,
        choices=ChoicePresets.ENGLISH_4
    )
    
    print("✓ Generated: output/english_test.pdf\n")


if __name__ == "__main__":
    import os
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    print("=== OMR Generator Examples ===\n")
    
    example_1_simple_sheet()
    example_2_blank_sheet()
    example_3_true_false()
    example_4_with_sections()
    example_5_with_essay()
    example_6_answer_key()
    example_7_english_choices()
    
    print("=== All examples completed ===")
