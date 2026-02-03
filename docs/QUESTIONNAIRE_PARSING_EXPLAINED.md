# Questionnaire Parsing Explained

## Simple Overview

Questionnaire parsing is like converting a PDF form into a structured database of questions that the system can answer.

## Step-by-Step Process

### Step 1: Read the PDF File

**Input**: `ILPA_Due_Diligence_Questionnaire_v1.2.pdf`

**What happens**:
- System reads the PDF file
- Extracts all text content
- Preserves structure (headings, page numbers, formatting)

**Example extracted text**:
```
Section 1: General Firm Information

1.1 What is the legal name of your firm?
Please provide the legal name as registered with relevant authorities.

1.2 When was your firm established?
Provide the date of establishment.

1.3 What is your firm's primary business address?
Include street address, city, state, and country.
```

### Step 2: Identify Sections

**How it works**:
- Look for section headers (e.g., "Section 1:", "Section 2:")
- Look for major headings (e.g., "General Firm Information")
- Use table of contents if available

**Result**:
```
Sections Found:
- Cover Sheet
- Basic Questions
- Section 1: General Firm Information
- Section 2: General Fund Information
- Section 3: Investment Strategy
... (14 sections total)
- Appendices A-E
```

### Step 3: Extract Questions

**For each section, find questions**:

**Pattern Recognition**:
- Questions usually start with numbers: "1.1", "1.2", "2.1"
- May have sub-questions: "1.1a", "1.1b"
- Question text follows the number

**Example Extraction**:
```
Section 1: General Firm Information

Question Found:
  Number: "1.1"
  Text: "What is the legal name of your firm?"
  Full Text: "What is the legal name of your firm? Please provide the legal name as registered with relevant authorities."
  Order: 1 (first question in section 1)

Question Found:
  Number: "1.2"
  Text: "When was your firm established?"
  Full Text: "When was your firm established? Provide the date of establishment."
  Order: 2 (second question in section 1)
```

### Step 4: Structure the Data

**Create structured objects**:

```python
Questionnaire {
  id: "q_12345"
  name: "ILPA Due Diligence Questionnaire v1.2"
  sections: [
    Section {
      id: "sec_1"
      name: "General Firm Information"
      order: 1
      questions: [
        Question {
          id: "q_1_1"
          section_id: "sec_1"
          question_number: "1.1"
          question_text: "What is the legal name of your firm? Please provide the legal name as registered with relevant authorities."
          order: 1
        },
        Question {
          id: "q_1_2"
          section_id: "sec_1"
          question_number: "1.2"
          question_text: "When was your firm established? Provide the date of establishment."
          order: 2
        }
      ]
    }
  ]
}
```

### Step 5: Store in Database

**Save to database tables**:

```
questionnaires table:
  - questionnaire_id: "q_12345"
  - name: "ILPA Due Diligence Questionnaire v1.2"
  - created_at: "2026-02-04"

sections table:
  - section_id: "sec_1"
  - questionnaire_id: "q_12345"
  - section_name: "General Firm Information"
  - order: 1

questions table:
  - question_id: "q_1_1"
  - section_id: "sec_1"
  - question_number: "1.1"
  - question_text: "What is the legal name of your firm?..."
  - order: 1
```

## Real Example: ILPA Questionnaire

### What the PDF Contains

```
ILPA Due Diligence Questionnaire v1.2

Table of Contents:
- Section 1: General Firm Information
- Section 2: General Fund Information
- Section 3: Investment Strategy
...

Section 1: General Firm Information

1.1 What is the legal name of your firm?
[Text continues...]

1.2 When was your firm established?
[Text continues...]
```

### What Gets Extracted

**14 Main Sections**:
1. General Firm Information
2. General Fund Information
3. Investment Strategy
4. Investment Process
5. Team
6. Alignment of Interest
7. Market Environment
8. Fund Terms
9. Firm Governance/Risk/Compliance
10. ESG
11. Track Record
12. Accounting/Valuation/Reporting
13. Legal/Administration
14. Diversity and Inclusion

**Plus**:
- Cover Sheet questions
- Basic Questions (yes/no format)
- Appendices (templates)

## Technical Implementation

### Parsing Algorithm (Pseudocode)

```python
def parse_questionnaire(pdf_file):
    # Step 1: Extract text
    text = extract_text_from_pdf(pdf_file)

    # Step 2: Find sections
    sections = []
    for heading in find_section_headings(text):
        section = {
            'name': heading,
            'order': len(sections) + 1,
            'questions': []
        }
        sections.append(section)

    # Step 3: Extract questions from each section
    for section in sections:
        section_text = get_section_text(text, section['name'])
        questions = extract_questions(section_text)
        section['questions'] = questions

    # Step 4: Create questionnaire object
    questionnaire = {
        'name': get_questionnaire_name(text),
        'sections': sections,
        'total_questions': count_all_questions(sections)
    }

    return questionnaire

def extract_questions(section_text):
    questions = []
    # Pattern: "1.1 Question text here..."
    pattern = r'(\d+\.\d+[a-z]?)\s+(.+?)(?=\d+\.\d+|\Z)'
    matches = re.findall(pattern, section_text, re.DOTALL)

    for i, (number, text) in enumerate(matches):
        question = {
            'question_number': number,
            'question_text': text.strip(),
            'order': i + 1
        }
        questions.append(question)

    return questions
```

### Challenges

1. **Multi-page Questions**: A question might span multiple pages
   - Solution: Track page breaks and continue reading

2. **Sub-questions**: Questions like "1.1a", "1.1b"
   - Solution: Use regex pattern that captures letters after numbers

3. **Tables**: Some questions include tables
   - Solution: Extract table structure separately

4. **Cross-references**: Questions reference other questions
   - Solution: Extract references and store as metadata

5. **Formatting Variations**: Different PDFs have different formats
   - Solution: Use multiple parsing strategies and fallbacks

## Why This Matters

Once parsed, the system can:
- ✅ Generate answers for each question automatically
- ✅ Track which questions have been answered
- ✅ Organize answers by section
- ✅ Reference questions by ID (not just text)

## Visual Flow

```
PDF File
    ↓
[PDF Parser]
    ↓
Raw Text with Structure
    ↓
[Section Detector]
    ↓
Identified Sections
    ↓
[Question Extractor]
    ↓
Structured Questions
    ↓
[Database Storage]
    ↓
Ready for Answer Generation
```

## Summary

**Questionnaire Parsing = Converting PDF → Structured Questions Database**

- Input: PDF file
- Process: Extract text → Find sections → Extract questions → Structure data
- Output: Database of questions organized by sections
- Purpose: Enable automated answer generation for each question
