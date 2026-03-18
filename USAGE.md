# คู่มือการใช้งาน OMR Generator

## การติดตั้ง

### 1. ติดตั้ง dependencies

```bash
pip install -r requirements.txt
```

### 2. ติดตั้งเป็น package (ถ้าต้องการ)

```bash
pip install -e .
```

## การใช้งานพื้นฐาน

### สร้าง OMR แบบง่าย

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

# สร้าง PDF
generator.generate(
    exam_config=exam_config,
    filename="omr_sheet.pdf",
    student=student,
    num_questions=20,
    choices=ChoicePresets.THAI_4
)
```

## ตัวอย่างการใช้งาน

### 1. กระดาษคำตอบว่าง (ไม่มีข้อมูลนักเรียน)

```python
generator.generate(
    exam_config=exam_config,
    filename="blank_sheet.pdf",
    num_questions=20,
    choices=ChoicePresets.THAI_4
)
```

### 2. ข้อสอบถูก-ผิด

```python
generator.generate(
    exam_config=exam_config,
    filename="true_false.pdf",
    num_questions=15,
    choices=ChoicePresets.TRUE_FALSE  # ["ถูก", "ผิด"]
)
```

### 3. ข้อสอบภาษาอังกฤษ

```python
exam_config = ExamConfig(
    exam_title="English Test",
    subject_name="English (Grade 4)"
)

generator.generate(
    exam_config=exam_config,
    filename="english_test.pdf",
    num_questions=20,
    choices=ChoicePresets.ENGLISH_4  # ["A", "B", "C", "D"]
)
```

### 4. มีส่วนเขียนตอบ

```python
generator.generate(
    exam_config=exam_config,
    filename="with_essay.pdf",
    student=student,
    num_questions=20,
    choices=ChoicePresets.THAI_4,
    include_essay=True,
    essay_lines=3  # จำนวนบรรทัด
)
```

### 5. แบ่งหมวดคะแนน

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

### 6. สร้างเฉลยคำตอบ

```python
# กำหนดเฉลย: 0=ก, 1=ข, 2=ค, 3=ง
answer_key = [
    0, 1, 2, 3, 0, 1, 2, 3, 0, 1,  # ข้อ 1-10
    2, 3, 0, 1, 2, 3, 0, 1, 2, 3   # ข้อ 11-20
]

generator.generate_answer_key(
    exam_config=exam_config,
    filename="answer_key.pdf",
    num_questions=20,
    choices=ChoicePresets.THAI_4,
    answer_key=answer_key
)
```

### 7. สร้างหลายคนพร้อมกัน (Batch)

```python
students = [
    StudentData("CMU-69-001", "เด็กชายรักเรียน ดีมาก", "ป.4/1", "1"),
    StudentData("CMU-69-002", "เด็กหญิงขยัน เรียนดี", "ป.4/1", "2"),
    StudentData("CMU-69-003", "เด็กชายฉลาด มากความรู้", "ป.4/1", "3"),
]

generated_files = generator.generate_batch(
    exam_config=exam_config,
    students=students,
    output_dir="batch_output",
    num_questions=20,
    choices=ChoicePresets.THAI_4
)

print(f"สร้างไฟล์ {len(generated_files)} ไฟล์")
```

### 8. สร้างจากไฟล์ CSV

สร้างไฟล์ `students.csv`:
```csv
id,name,room,number
CMU-69-001,เด็กชายรักเรียน ดีมาก,ป.4/1,1
CMU-69-002,เด็กหญิงขยัน เรียนดี,ป.4/1,2
CMU-69-003,เด็กชายฉลาด มากความรู้,ป.4/1,3
```

```python
generated_files = generator.generate_batch_from_csv(
    exam_config=exam_config,
    csv_file="students.csv",
    output_dir="batch_output",
    num_questions=20,
    choices=ChoicePresets.THAI_4
)
```

## ตัวเลือกคำตอบที่มีให้

```python
from omr_generator.constants import ChoicePresets

# ภาษาไทย
ChoicePresets.THAI_4          # ["ก", "ข", "ค", "ง"]
ChoicePresets.THAI_5          # ["ก", "ข", "ค", "ง", "จ"]

# ถูก-ผิด
ChoicePresets.TRUE_FALSE      # ["ถูก", "ผิด"]
ChoicePresets.TRUE_FALSE_SHORT # ["ถ", "ผ"]

# ภาษาอังกฤษ
ChoicePresets.ENGLISH_4       # ["A", "B", "C", "D"]
ChoicePresets.ENGLISH_5       # ["A", "B", "C", "D", "E"]

# ตัวเลข
ChoicePresets.NUMBERS_3       # ["1", "2", "3"]
ChoicePresets.NUMBERS_4       # ["1", "2", "3", "4"]
```

### กำหนดตัวเลือกเอง

```python
custom_choices = ["甲", "乙", "丙", "丁"]  # ภาษาจีน
custom_choices = ["α", "β", "γ", "δ"]     # กรีก
custom_choices = ["①", "②", "③", "④"]     # ตัวเลขวงกลม
```

## รันตัวอย่าง

```bash
# ตัวอย่างพื้นฐาน
PYTHONPATH=. python examples/basic_usage.py

# ตัวอย่าง Batch Generation
PYTHONPATH=. python examples/batch_generation.py
```

## โครงสร้างโปรเจค

```
.
├── omr_generator/          # Package หลัก
│   ├── __init__.py
│   ├── core.py            # OMRGenerator class
│   ├── models.py          # Data models
│   ├── constants.py       # Constants & presets
│   ├── fonts.py           # Font management
│   └── components.py      # PDF components
│
├── examples/              # ตัวอย่างการใช้งาน
│   ├── basic_usage.py
│   └── batch_generation.py
│
├── fonts/                 # ฟอนต์ไทย
│   └── THSarabunNew/
│
├── README.md             # เอกสารหลัก
├── USAGE.md              # คู่มือนี้
├── requirements.txt      # Dependencies
└── setup.py              # Setup script
```

## Tips & Tricks

### 1. ปรับจำนวนข้อสอบ
```python
num_questions=10  # 1-20 ข้อ
```

### 2. ปรับจำนวนบรรทัดเขียนตอบ
```python
essay_lines=5  # 2-10 บรรทัด
```

### 3. ใส่รหัสข้อสอบใน QR Code
```python
exam_config = ExamConfig(
    exam_title="สอบปลายภาค",
    subject_name="วิทยาศาสตร์",
    exam_code="SCI-P4-2569-FINAL",  # จะถูกใส่ใน QR
    exam_date="15 มีนาคม 2569"
)
```

### 4. สร้างกระดาษว่างหลายแผ่น
```python
for i in range(10):
    generator.generate(
        exam_config=exam_config,
        filename=f"blank_{i+1}.pdf",
        num_questions=20,
        choices=ChoicePresets.THAI_4
    )
```

## การแก้ปัญหา

### ฟอนต์ไม่แสดง
ตรวจสอบว่ามีโฟลเดอร์ `fonts/THSarabunNew/` และมีไฟล์ฟอนต์ครบ

### Import Error
ใช้ `PYTHONPATH=.` หน้าคำสั่ง python หรือติดตั้งเป็น package ด้วย `pip install -e .`

### PDF ไม่สร้าง
ตรวจสอบว่าโฟลเดอร์ output มีอยู่หรือไม่ หรือสร้างด้วย `os.makedirs("output", exist_ok=True)`

## License

MIT License
