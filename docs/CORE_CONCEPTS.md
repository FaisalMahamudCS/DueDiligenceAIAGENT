# Core Concepts Explained

## 1. Questionnaire Parsing

### What It Is
Converting a PDF questionnaire into a structured database of questions.

### Simple Analogy
Like converting a paper form into a spreadsheet where each row is a question.

### How It Works

```
PDF File (ILPA_Questionnaire.pdf)
    ↓
[Read PDF] Extract all text
    ↓
[Find Sections] "Section 1: General Firm Information"
    ↓
[Extract Questions] "1.1 What is your firm's name?"
    ↓
[Structure Data] Create Question objects with IDs
    ↓
[Store in Database] Save to questions table
    ↓
Ready for Answer Generation
```

### Example

**Input (PDF)**:
```
Section 1: General Firm Information

1.1 What is the legal name of your firm?
Please provide the legal name as registered.

1.2 When was your firm established?
Provide the date of establishment.
```

**Output (Database)**:
```
Question 1:
  ID: q_1_1
  Section: General Firm Information
  Number: 1.1
  Text: "What is the legal name of your firm? Please provide the legal name as registered."

Question 2:
  ID: q_1_2
  Section: General Firm Information
  Number: 1.2
  Text: "When was your firm established? Provide the date of establishment."
```

### Why It Matters
- System can automatically answer each question
- Track which questions are answered
- Organize by sections
- Reference questions by ID

---

## 2. AI/LLM Layer

### What It Is
The AI service that generates answers to questions using company documents.

### Simple Analogy
Like a smart assistant that reads documents and answers questions about them.

### How It Works

```
Question: "What is your firm's name?"
    ↓
[Search Documents] Find relevant parts in company documents
    ↓
[Retrieve Context] Get text chunks from documents
    ↓
[Send to LLM] "Here's the question and relevant document text"
    ↓
[LLM Generates Answer] "MiniMax Corporation" (with citations)
    ↓
[Return Answer] Answer with confidence score and citations
```

### The AI Layer Components

**1. LLM Service** (`src/services/llm_service.py`):
- Connects to AI models (OpenAI GPT-4, Anthropic Claude, etc.)
- Generates answers from questions + document context
- Creates embeddings for semantic search
- Calculates semantic similarity

**2. Answer Generation Process**:
```
Step 1: Find relevant documents
  → Use semantic search (embeddings)
  → Get top 5 most relevant chunks

Step 2: Get citations
  → Extract page numbers
  → Get bounding boxes (exact location on page)

Step 3: Ask LLM
  → Send question + document chunks to LLM
  → LLM reads context and generates answer
  → LLM includes citations in answer

Step 4: Process response
  → Extract answer text
  → Determine if answerable
  → Calculate confidence score
```

### Example Flow

**Input**:
- Question: "What is your firm's name?"
- Documents: Prospectus.pdf, Financial Report.pdf

**Process**:
1. Search documents → Find "MiniMax Corporation" in Prospectus.pdf, page 5
2. Retrieve context → Get text chunk with bounding box coordinates
3. Send to LLM → "Question: What is your firm's name? Context: [Prospectus text]"
4. LLM responds → "MiniMax Corporation [Citation: Prospectus.pdf, page 5]"

**Output**:
```json
{
  "answer_text": "MiniMax Corporation",
  "is_answerable": true,
  "confidence": 0.95,
  "citations": [
    {
      "document_name": "Prospectus.pdf",
      "page_number": 5,
      "chunk_text": "MiniMax Corporation was established...",
      "bounding_box": { "x0": 100, "y0": 200, "x1": 300, "y1": 250 }
    }
  ]
}
```

### Why It Matters
- Automatically generates answers (no manual searching)
- Finds information across multiple documents
- Provides citations (shows where answer came from)
- Calculates confidence (how sure the AI is)

---

## How They Work Together

### Complete Flow

```
1. Upload Questionnaire PDF
   → Parse into questions
   → Store in database

2. Upload Company Documents
   → Index documents
   → Create embeddings
   → Store in vector database

3. Generate Answer
   → Get question from database
   → Search documents (semantic search)
   → Retrieve relevant chunks
   → Send to LLM with context
   → LLM generates answer
   → Return answer with citations

4. Human Review
   → Review AI answer
   → Approve, reject, or edit
   → Store both AI and human answers

5. Evaluate
   → Compare AI vs human answers
   → Calculate similarity scores
   → Generate evaluation report
```

### Architecture

```
┌─────────────────┐
│  Questionnaire  │
│     Parser      │ → Extracts questions from PDF
└─────────────────┘

┌─────────────────┐
│  Document       │
│   Indexer       │ → Indexes company documents
└─────────────────┘

┌─────────────────┐
│  Answer Service │ → Orchestrates answer generation
└─────────────────┘
         │
         ├─→ Indexing Pipeline (finds relevant docs)
         │
         └─→ LLM Service (generates answer)
                │
                └─→ External AI API (OpenAI, Anthropic, etc.)
```

---

## Key Takeaways

1. **Questionnaire Parsing**: PDF → Structured Questions
   - Extracts questions from PDF
   - Organizes by sections
   - Stores in database

2. **AI/LLM Layer**: Questions + Documents → Answers
   - Searches documents semantically
   - Uses AI to generate answers
   - Provides citations and confidence

3. **Together**: Automated questionnaire completion
   - Parse questionnaire once
   - Generate answers automatically
   - Human reviews and improves
   - System learns from feedback

---

## Files to Review

- **Questionnaire Parsing**: `docs/QUESTIONNAIRE_PARSING_EXPLAINED.md`
- **AI/LLM Service**: `backend/src/services/llm_service.py`
- **Answer Generation**: `backend/src/services/answer_service.py`
- **Architecture**: `docs/ARCHITECTURE_DESIGN.md`
