# OMR Generator - Thai OMR Answer Sheet Generator

ระบบสร้างกระดาษคำตอบ OMR (Optical Mark Recognition) แบบครบวงจร รองรับภาษาไทยและภาษาอังกฤษ

## Disclaimer

> [!IMPORTANT]
>
>  จริงๆแล้วโปรเจ็คนี้ผมสร้างเพื่อให้ครูท่านนึง มีโปรแกรมสำหรับรวจการบ้านเด็กโดยที่ไม่ต้องมานั่งตรวจทีละข้อ แต่ก็อยากเผยแพร่ให้คนอื่นได้ใช้บ้าง code จริงๆแล้วนั้นเละเทะมากจนผมไม่กล้าแชร์ (ฮา) จึงอาศัยบุญบารมีหลวงปู AI ช่วยเขียนให้ใหม่ดังนั้น มันอาจจะมีบางส่วนที่โค้ดทำงานแปลกๆเนื่อจากไม่ได้ตรวจดีพอ แต่หวังว่าจะเอาไปเป็นแนวทางให้แก่ทุกคนได้นะครับ

## Installation

```bash
pip install reportlab qrcode pillow
```

## Quick Start

```python
from omr_generator import OMRGenerator, ExamConfig, StudentData
from omr_generator.constants import ChoicePresets

# สร้าง generator
generator = OMRGenerator()

# ตั้งค่าข้อสอบ
exam_config = ExamConfig(
    exam_title="สอบปลายภาคเรียนที่ 2",
    subject_name="วิทยาศาสตร์ (ป.4)",
    exam_date="15 มีนาคม 2569"
)

# ข้อมูลนักเรียน
student = StudentData(
    id="CMU-69-001",
    name="เด็กชายรักเรียน ดีมาก",
    room="ป.4/1",
    number="1"
)

# สร้าง OMR
generator.generate(
    exam_config=exam_config,
    filename="omr_sheet.pdf",
    student=student,
    num_questions=20,
    choices=ChoicePresets.THAI_4
)
```

## Usage Examples

### 1. Basic OMR Sheet

```python
from omr_generator import OMRGenerator, ExamConfig, StudentData
from omr_generator.constants import ChoicePresets

generator = OMRGenerator()

exam_config = ExamConfig(
    exam_title="สอบปลายภาค",
    subject_name="คณิตศาสตร์ (ป.4)"
)

student = StudentData("CMU-69-001", "เด็กชายรักเรียน ดีมาก", "ป.4/1", "1")

generator.generate(
    exam_config=exam_config,
    filename="output.pdf",
    student=student,
    num_questions=20,
    choices=ChoicePresets.THAI_4
)
```

### 2. Blank Sheet (No Student Data)

```python
generator.generate(
    exam_config=exam_config,
    filename="blank.pdf",
    num_questions=20,
    choices=ChoicePresets.THAI_4
)
```

### 3. True/False Test

```python
generator.generate(
    exam_config=exam_config,
    filename="true_false.pdf",
    num_questions=15,
    choices=ChoicePresets.TRUE_FALSE  # ["ถูก", "ผิด"]
)
```

### 4. With Essay Section

```python
generator.generate(
    exam_config=exam_config,
    filename="with_essay.pdf",
    student=student,
    num_questions=20,
    choices=ChoicePresets.THAI_4,
    include_essay=True,
    essay_lines=3
)
```

### 5. With Scoring Sections

```python
from omr_generator import QuestionSection

sections = [
    QuestionSection("ส่วนที่ 1: ไวยากรณ์", 1, 10, 10),
    QuestionSection("ส่วนที่ 2: การอ่าน", 11, 20, 10)
]

exam_config = ExamConfig(
    exam_title="สอบปลายภาค",
    subject_name="ภาษาไทย (ป.4)",
    sections=sections
)

generator.generate(
    exam_config=exam_config,
    filename="with_sections.pdf",
    student=student,
    num_questions=20,
    choices=ChoicePresets.THAI_4
)
```

### 6. Generate Answer Key

```python
# Answer key: 0=ก, 1=ข, 2=ค, 3=ง
answer_key = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1,
              2, 3, 0, 1, 2, 3, 0, 1, 2, 3]

generator.generate_answer_key(
    exam_config=exam_config,
    filename="answer_key.pdf",
    num_questions=20,
    choices=ChoicePresets.THAI_4,
    answer_key=answer_key
)
```

### 7. Batch Generation from List

```python
students = [
    StudentData("CMU-69-001", "เด็กชายรักเรียน ดีมาก", "ป.4/1", "1"),
    StudentData("CMU-69-002", "เด็กหญิงขยัน เรียนดี", "ป.4/1", "2"),
    StudentData("CMU-69-003", "เด็กชายฉลาด มากความรู้", "ป.4/1", "3"),
]

generated = generator.generate_batch(
    exam_config=exam_config,
    students=students,
    output_dir="batch_output",
    num_questions=20,
    choices=ChoicePresets.THAI_4
)

print(f"Generated {len(generated)} files")
```

### 8. Batch Generation from CSV

CSV format:
```csv
id,name,room,number
CMU-69-001,เด็กชายรักเรียน ดีมาก,ป.4/1,1
CMU-69-002,เด็กหญิงขยัน เรียนดี,ป.4/1,2
```

```python
generated = generator.generate_batch_from_csv(
    exam_config=exam_config,
    csv_file="students.csv",
    output_dir="batch_output",
    num_questions=20,
    choices=ChoicePresets.THAI_4
)
```

## Choice Presets

```python
from omr_generator.constants import ChoicePresets

ChoicePresets.THAI_4          # ["ก", "ข", "ค", "ง"]
ChoicePresets.THAI_5          # ["ก", "ข", "ค", "ง", "จ"]
ChoicePresets.TRUE_FALSE      # ["ถูก", "ผิด"]
ChoicePresets.TRUE_FALSE_SHORT # ["ถ", "ผ"]
ChoicePresets.ENGLISH_4       # ["A", "B", "C", "D"]
ChoicePresets.ENGLISH_5       # ["A", "B", "C", "D", "E"]
ChoicePresets.NUMBERS_3       # ["1", "2", "3"]
ChoicePresets.NUMBERS_4       # ["1", "2", "3", "4"]
```

Or use custom choices:
```python
choices = ["α", "β", "γ", "δ"]
```

## API Reference

### OMRGenerator

Main class for generating OMR sheets.

#### Methods

- `generate()` - Generate a single OMR sheet
- `generate_batch()` - Generate multiple sheets from list
- `generate_batch_from_csv()` - Generate from CSV file
- `generate_answer_key()` - Generate answer key sheet

### ExamConfig

Exam configuration dataclass.

```python
ExamConfig(
    exam_title: str,           # ชื่อข้อสอบ
    subject_name: str,         # ชื่อวิชา
    exam_date: str = "",       # วันที่สอบ
    exam_code: str = "",       # รหัสข้อสอบ
    academic_year: str = "2569", # ปีการศึกษา
    sections: List[QuestionSection] = None  # หมวดคะแนน
)
```

### StudentData

Student information dataclass.

```python
StudentData(
    id: str = "",      # รหัสนักเรียน
    name: str = "",    # ชื่อ-นามสกุล
    room: str = "",    # ห้องเรียน
    number: str = ""   # เลขที่
)
```

### QuestionSection

Question section for scoring.

```python
QuestionSection(
    name: str,              # ชื่อหมวด
    start_question: int,    # ข้อเริ่มต้น
    end_question: int,      # ข้อสุดท้าย
    max_score: int          # คะแนนเต็ม
)
```

## Project Structure

```
omr_generator/
├── __init__.py          # Package initialization
├── core.py              # Main OMRGenerator class
├── models.py            # Data models
├── constants.py         # Constants and presets
├── fonts.py             # Font management
└── components.py        # PDF components

examples/
├── basic_usage.py       # Basic examples
└── batch_generation.py  # Batch generation examples

fonts/
└── THSarabunNew/        # Thai fonts
```

## Requirements

- Python 3.7+
- reportlab
- qrcode
- pillow

## License

MIT License - see [LICENSE](LICENSE) file for details

Created for Thai educational institutions.


