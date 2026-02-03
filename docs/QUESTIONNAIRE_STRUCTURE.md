# ILPA Questionnaire Structure Analysis

## Overview

The ILPA Due Diligence Questionnaire v1.2 is a comprehensive questionnaire used for private equity fund due diligence. Understanding its structure is essential for proper parsing and question extraction.

## Document Structure

### Main Sections

1. **Overview** - Introduction and purpose
2. **Frequently Asked Questions** - Common questions about the questionnaire
3. **Cover Sheet** - Basic information collection
4. **Basic Questions** - Yes/No questions with reference fields
5. **Detailed Questions** - Long-form questions organized by topic
6. **Appendices** - Templates and requested documents

### Detailed Questions Topics (14 Sections)

The Detailed Questions section is organized into 14 main topic areas:

1. **General Firm Information**
2. **General Fund Information**
3. **Investment Strategy**
4. **Investment Process**
5. **Team**
6. **Alignment of Interest**
7. **Market Environment**
8. **Fund Terms**
9. **Firm Governance/Risk/Compliance**
10. **ESG** (Environmental, Social, Governance)
11. **Track Record**
12. **Accounting/Valuation/Reporting**
13. **Legal/Administration**
14. **Diversity and Inclusion**

### Appendices

- **Appendix A** - Requested Documents (25+ document types)
- **Appendix B** - Templates: Team Members
- **Appendix C** - Templates: References
- **Appendix D** - Templates: Fund
- **Appendix E** - Templates: Portfolio Investments
  - E1: Deal Log
  - E2: Performance & Attribution
  - E3: Cash Flows
  - E4: Fee Schedule
  - E5: Debt Maturities
  - E6: Investment Details

## Parsing Strategy

### Section Identification

Sections can be identified by:
- Section numbers (1-14 for Detailed Questions)
- Section headings (e.g., "General Firm Information")
- Table of Contents references

### Question Identification

**Basic Questions:**
- Typically yes/no format
- Include "Reference" field for additional information
- May have sub-questions

**Detailed Questions:**
- Numbered questions (e.g., 1.1, 1.2, 2.1)
- May include sub-questions
- Can span multiple paragraphs
- May reference appendices or other sections

### Question Numbering Patterns

- Main questions: `SectionNumber.QuestionNumber` (e.g., 1.1, 1.2, 2.1)
- Sub-questions: May use letters (a, b, c) or additional numbers
- Cross-references: Questions may reference other questions or appendices

### Special Considerations

1. **N/A Questions**: Some questions may not apply to all funds
   - Basic Questions: Use "N/A" in Reference field
   - Detailed Questions: Provide brief explanation for skipped questions

2. **Sensitive Information**: GPs may provide answers:
   - In person
   - In redacted format
   - At later stage in diligence
   - Should include explanation for rationale

3. **Multi-Fund GPs**: Questions about "Firm" should focus on business units materially related to the Fund

4. **Templates**: Appendices contain structured templates that may need special handling:
   - Spreadsheet format preferred
   - Multiple currencies
   - Time-series data
   - Complex nested structures

## Parsing Implementation Notes

### Extraction Priorities

1. **Primary Questions**: Extract all numbered questions from Detailed Questions section
2. **Basic Questions**: Extract yes/no questions with reference fields
3. **Section Headers**: Identify and preserve section structure
4. **Question Order**: Maintain original ordering within sections
5. **Cross-References**: Preserve references to other questions/appendices

### Metadata to Capture

- Question number (e.g., "1.1", "2.3")
- Section name and number
- Question text (full text including sub-questions)
- Question type (basic yes/no vs detailed)
- Related appendices or templates
- Cross-references to other questions

### Challenges

1. **Multi-page Questions**: Questions may span multiple pages
2. **Nested Structure**: Sub-questions and sub-sections
3. **Table Format**: Some questions include tables
4. **Appendix References**: Questions reference appendices that contain structured data
5. **Formatting Variations**: Different formatting for Basic vs Detailed questions

## Example Parsed Structure

```
Questionnaire: ILPA Due Diligence Questionnaire v1.2
├── Section: Cover Sheet
│   └── Questions: [Cover sheet fields]
├── Section: Basic Questions
│   └── Questions: [Yes/No questions with references]
├── Section 1: General Firm Information
│   ├── Question 1.1: [Question text]
│   ├── Question 1.2: [Question text]
│   └── ...
├── Section 2: General Fund Information
│   └── ...
├── ...
└── Appendices
    ├── Appendix A: Requested Documents
    ├── Appendix B: Team Members Template
    ├── Appendix C: References Template
    ├── Appendix D: Fund Template
    └── Appendix E: Portfolio Investments Templates
```

## Integration with Answer Generation

When generating answers:
- Questions from Detailed Questions section require full-text answers with citations
- Basic Questions may be answered with yes/no plus reference citations
- Appendix-related questions may reference structured data from appendices
- Cross-referenced questions should maintain context from referenced questions
