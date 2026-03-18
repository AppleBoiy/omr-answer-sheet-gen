"""
Batch generation examples.
"""

import csv
import os
from omr_generator import OMRGenerator, ExamConfig, StudentData
from omr_generator.constants import ChoicePresets


def example_batch_from_list():
    """Generate OMR sheets for multiple students from a list."""
    print("Example: Batch generation from list")
    
    generator = OMRGenerator()
    
    exam_config = ExamConfig(
        exam_title="สอบปลายภาคเรียนที่ 2",
        subject_name="วิทยาศาสตร์ (ป.4)",
        exam_date="20 มีนาคม 2569",
        exam_code="SCI-P4-2569-FINAL"
    )
    
    students = [
        StudentData("CMU-69-001", "เด็กชายรักเรียน ดีมาก", "ป.4/1", "1"),
        StudentData("CMU-69-002", "เด็กหญิงขยัน เรียนดี", "ป.4/1", "2"),
        StudentData("CMU-69-003", "เด็กชายฉลาด มากความรู้", "ป.4/1", "3"),
        StudentData("CMU-69-004", "เด็กหญิงสุภาพ น่ารัก", "ป.4/1", "4"),
        StudentData("CMU-69-005", "เด็กชายเก่ง ทุกวิชา", "ป.4/1", "5"),
    ]
    
    generated = generator.generate_batch(
        exam_config=exam_config,
        students=students,
        output_dir="output/batch",
        num_questions=20,
        choices=ChoicePresets.THAI_4
    )
    
    print(f"✓ Generated {len(generated)} OMR sheets")
    for filename in generated:
        print(f"  - {filename}")
    print()


def example_batch_from_csv():
    """Generate OMR sheets from CSV file."""
    print("Example: Batch generation from CSV")
    
    # Create sample CSV
    csv_file = "output/students.csv"
    os.makedirs("output", exist_ok=True)
    
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'room', 'number'])
        writer.writeheader()
        writer.writerows([
            {'id': 'CMU-69-011', 'name': 'เด็กชายสมชาย ใจดี', 'room': 'ป.4/2', 'number': '1'},
            {'id': 'CMU-69-012', 'name': 'เด็กหญิงสมหญิง สวยงาม', 'room': 'ป.4/2', 'number': '2'},
            {'id': 'CMU-69-013', 'name': 'เด็กชายสมศักดิ์ เรียนเก่ง', 'room': 'ป.4/2', 'number': '3'},
        ])
    
    print(f"✓ Created sample CSV: {csv_file}")
    
    generator = OMRGenerator()
    
    exam_config = ExamConfig(
        exam_title="สอบกลางภาค",
        subject_name="คณิตศาสตร์ (ป.4)",
        exam_date="21 มีนาคม 2569"
    )
    
    generated = generator.generate_batch_from_csv(
        exam_config=exam_config,
        csv_file=csv_file,
        output_dir="output/batch_csv",
        num_questions=20,
        choices=ChoicePresets.THAI_4
    )
    
    print(f"✓ Generated {len(generated)} OMR sheets from CSV")
    for filename in generated:
        print(f"  - {filename}")
    print()


if __name__ == "__main__":
    print("=== Batch Generation Examples ===\n")
    
    example_batch_from_list()
    example_batch_from_csv()
    
    print("=== All batch examples completed ===")
