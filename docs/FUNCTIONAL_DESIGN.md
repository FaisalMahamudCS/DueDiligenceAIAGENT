# Functional Design

## 1. Product & Data Model Alignment

### End-to-End Data Flow

**Questionnaire Project Lifecycle:**
1. User uploads questionnaire file (PDF)
2. System parses questionnaire into sections and questions
3. User creates project with questionnaire reference
4. User selects document scope (ALL_DOCS or SPECIFIC documents)
5. System validates document availability
6. Project status: CREATING → READY

**Document Ingestion Lifecycle:**
1. User uploads document (PDF, DOCX, XLSX, PPTX)
2. System parses document and extracts text with bounding boxes
3. System chunks document with metadata (page, position)
4. System generates embeddings for chunks
5. System stores in vector store and object storage
6. System marks ALL_DOCS projects as OUTDATED

**Answer Generation Lifecycle:**
1. User requests answer for question
2. System retrieves relevant document chunks (Layer 1: semantic/section retrieval)
3. System gets citation chunks with bounding boxes (Layer 2)
4. LLM generates answer using retrieved context
5. System determines answerability and calculates confidence
6. System stores answer with citations
7. User reviews and updates answer status

**Evaluation Lifecycle:**
1. User provides manual answers (ground truth)
2. User requests evaluation
3. System compares AI answers vs manual answers
4. System calculates similarity metrics
5. System generates evaluation report

### API to Database Mapping

| API Endpoint | Database Operations | Storage Operations |
|-------------|-------------------|-------------------|
| POST /create-project-async | INSERT projects, questionnaires, sections, questions | - |
| POST /index-document-async | INSERT documents, UPDATE projects (if ALL_DOCS) | ObjectStorage.upload, VectorStore.store |
| POST /generate-single-answer | INSERT answers, citations | VectorStore.search |
| POST /update-answer | UPDATE answers | - |
| GET /get-project-info | SELECT projects, questionnaires | - |
| POST /evaluate-project | INSERT evaluation_results | - |

### Enumerations

**Project Status**: creating, ready, processing, completed, outdated, error
**Answer Review Status**: pending, confirmed, rejected, manual_updated, missing_data
**Request Status**: pending, processing, completed, failed
**Document Scope**: ALL_DOCS, SPECIFIC

## 2. Document Ingestion & Indexing

### Document Format Support

**PDF Parsing:**
- Extract text content using PyPDF2 or pdfplumber
- Extract bounding boxes for each text element
- Preserve page numbers and coordinates
- Extract metadata (title, author, creation date)

**DOCX Parsing:**
- Extract text using python-docx
- Preserve document structure (headings, paragraphs, tables)
- Extract metadata

**XLSX Parsing:**
- Extract cell values using openpyxl
- Preserve table structure and sheet names
- Extract metadata

**PPTX Parsing:**
- Extract text from slides using python-pptx
- Preserve slide structure
- Extract metadata

### Multi-Layer Indexing

**Layer 1: Answer Retrieval**
- Purpose: Find relevant document sections for answering questions
- Method: Semantic similarity search using embeddings
- Input: Question text
- Output: Top-K relevant chunks with relevance scores
- Storage: Vector store with document_id, chunk_id, embedding

**Layer 2: Citation Chunks with Bounding Boxes**
- Purpose: Provide precise citations with visual references
- Method: Retrieve chunks identified in Layer 1 with full metadata
- Input: Chunk IDs from Layer 1
- Output: Citation objects with:
  - Document ID and name
  - Chunk text
  - Page number
  - Bounding box coordinates (x0, y0, x1, y1)
  - Relevance score
- Storage: Database citations table with bounding_box JSON field

### ALL_DOCS Project Outdated Logic

**Trigger**: When a new document is successfully indexed

**Process:**
1. Query all projects where `document_scope = 'ALL_DOCS'`
2. Update project status to `OUTDATED`
3. Set `updated_at` timestamp
4. Optionally notify user or trigger regeneration

**Rationale**: ALL_DOCS projects should include all available documents. When new documents are added, existing answers may become incomplete or inaccurate.

## 3. Questionnaire Parsing & Project Lifecycle

### Questionnaire Parsing

**Input**: PDF file containing questionnaire (e.g., ILPA Due Diligence Questionnaire v1.2)

**Process:**
1. Extract text from PDF with structure preservation
2. Identify sections (typically by headings or numbered sections)
   - For ILPA format: Cover Sheet, Basic Questions, Detailed Questions (14 sections), Appendices
3. Identify questions within each section
   - Basic Questions: Yes/No format with reference fields
   - Detailed Questions: Numbered format (e.g., "1.1", "1.2", "2.1")
4. Extract question numbers and text
   - Handle sub-questions and multi-paragraph questions
   - Preserve cross-references to other questions/appendices
5. Maintain ordering (section order, question order within sections)
6. Assign unique IDs to sections and questions
7. Capture metadata (question type, cross-references, appendix links)

**Output Structure:**
```
Questionnaire: ILPA Due Diligence Questionnaire v1.2
  ├── Cover Sheet
  ├── Basic Questions (yes/no with references)
  ├── Section 1: General Firm Information
  │   ├── Question 1.1
  │   ├── Question 1.2
  │   └── ...
  ├── Section 2: General Fund Information
  │   └── ...
  ├── ... (14 sections total)
  └── Appendices (A-E with templates)
```

**ILPA-Specific Considerations:**
- Basic Questions use "N/A" in Reference field for non-applicable questions
- Detailed Questions may include explanations for skipped questions
- Questions may reference appendices (structured templates)
- Some questions may be answered in person or redacted format

**Storage**:
- Questionnaire record in `questionnaires` table
- Section records in `sections` table
- Question records in `questions` table

### Project Creation (Async)

**Request**: POST /create-project-async
- Project name
- Questionnaire file path/URL
- Document scope (ALL_DOCS or SPECIFIC)
- Document IDs (if SPECIFIC)

**Process:**
1. Validate request
2. Enqueue async task
3. Return request_id
4. Background worker:
   - Parse questionnaire file
   - Validate document scope and document IDs
   - Create project record
   - Link questionnaire to project
   - Update status to READY

**Response**: RequestStatus with request_id

### Project Update (Async)

**Request**: POST /update-project-async
- Project ID
- Update data (name, document scope, document IDs, etc.)

**Process:**
1. Validate project exists
2. Enqueue async task
3. Background worker:
   - Apply updates
   - If document scope or document IDs changed:
     - Mark existing answers as needing regeneration
     - Trigger automatic regeneration if configured
   - Update project record

**Automatic Regeneration Trigger:**
- Configuration change (document scope, document IDs)
- New documents indexed (for ALL_DOCS projects)
- User can configure auto-regenerate on/off

## 4. Answer Generation with Citations & Confidence

### Answer Generation Process

**Input**:
- Project ID
- Question ID
- Question text

**Process:**
1. Retrieve project and validate document scope
2. **Layer 1 Retrieval**:
   - Generate question embedding
   - Search vector store for similar chunks
   - Get top-K chunks with relevance scores
3. **Layer 2 Citation Extraction**:
   - Retrieve full chunk metadata including bounding boxes
   - Format as Citation objects
4. **LLM Answer Generation**:
   - Construct prompt with question and retrieved chunks (via `LLMService.construct_answer_prompt()`)
   - Call LLM API (via `LLMService.generate_answer()`)
   - LLM generates answer with reference to chunks
   - LLM indicates if answer is possible based on context
5. **Post-Processing**:
   - Determine answerability (can question be answered with available docs?)
   - Calculate confidence score (based on relevance scores, chunk quality, LLM certainty)
   - Extract and validate citations
6. **Storage**:
   - Save answer with all metadata
   - Save citations linked to answer

**Output**: AnswerResponse with:
- answer_text
- is_answerable (boolean)
- confidence (float 0.0-1.0)
- citations (list of Citation objects)

### Answerability Determination

**Criteria:**
- At least one relevant chunk found (relevance > threshold)
- LLM indicates answer is possible
- Answer text is not empty or generic

**Fallback**: If no relevant documents:
- is_answerable = false
- answer_text = "No relevant information found in available documents"
- confidence = 0.0
- citations = []

### Confidence Score Calculation

**Factors:**
1. Relevance scores of retrieved chunks (weighted average)
2. Number of supporting citations (more = higher confidence)
3. LLM certainty indicators (if available)
4. Answer completeness (longer, detailed answers = higher confidence)

**Formula**: Weighted combination of factors, normalized to 0.0-1.0

## 5. Review & Manual Overrides

### Review Workflow

**Status Transitions:**
- **CONFIRMED**: User approves AI-generated answer
- **REJECTED**: User rejects AI answer (may provide manual answer)
- **MANUAL_UPDATED**: User provides manual answer to replace AI answer
- **MISSING_DATA**: User indicates required data is missing from documents

### Manual Answer Storage

**Schema**:
- `answer_text`: AI-generated answer (preserved)
- `manual_answer_text`: Human-provided answer (stored separately)
- `review_status`: Current review status

**Rationale**: Preserve both AI and human answers for:
- Comparison and evaluation
- Audit trail
- Learning/improvement

### Answer Update Process

**Request**: POST /update-answer
- Answer ID
- Review status
- Manual answer text (optional)

**Process:**
1. Validate answer exists
2. Validate status transition is allowed
3. Update answer record:
   - Set review_status
   - Set manual_answer_text (if provided)
   - Preserve answer_text (AI answer)
4. Update updated_at timestamp

**Status Transition Rules:**
- Any status → CONFIRMED (user approves)
- Any status → REJECTED (user rejects)
- Any status → MANUAL_UPDATED (requires manual_answer_text)
- Any status → MISSING_DATA (user indicates missing data)

## 6. Evaluation Framework

### Evaluation Process

**Input**: Project ID

**Process:**
1. Retrieve all answers for project where `manual_answer_text IS NOT NULL`
2. For each answer:
   - Get AI answer text (`answer_text`)
   - Get human answer text (`manual_answer_text`)
   - Calculate semantic similarity (using embeddings)
   - Calculate keyword overlap (using TF-IDF or similar)
   - Combine into similarity score
   - Generate qualitative explanation
3. Calculate aggregate statistics:
   - Average similarity score
   - Distribution of scores
   - Questions with low scores (need improvement)
4. Generate evaluation report

### Similarity Metrics

**Semantic Similarity:**
- Generate embeddings for both answers
- Calculate cosine similarity between embeddings
- Range: 0.0 (completely different) to 1.0 (identical meaning)

**Keyword Overlap:**
- Extract keywords from both answers (remove stop words)
- Calculate Jaccard similarity or overlap ratio
- Range: 0.0 (no overlap) to 1.0 (identical keywords)

**Combined Score:**
- Weighted average: 70% semantic + 30% keyword
- Range: 0.0 to 1.0

### Qualitative Explanation

**Generated for each answer:**
- Semantic similarity interpretation
- Keyword overlap summary
- Key differences identified
- Areas of agreement
- Suggested improvements (if score is low)

### Evaluation Report

**Contents:**
- Project information
- Total questions evaluated
- Average similarity score
- Score distribution (histogram)
- Individual results with explanations
- Recommendations for improvement

## 7. Optional Chat Extension

### Chat Functionality

**Purpose**: Allow users to ask questions about documents in natural language

**Shared Resources:**
- Same indexed document corpus
- Same vector store
- Same citation system

### Constraints to Avoid Conflicts

**Document Scope:**
- Chat queries use ALL_DOCS scope (all indexed documents)
- Questionnaire answers use project-specific scope
- No interference between chat and questionnaire flows

**Citation Format:**
- Chat citations use same format as questionnaire answers
- Bounding boxes and page references preserved

**State Management:**
- Chat sessions are independent of projects
- No modification of project answers from chat
- Chat history stored separately

## 8. Frontend Experience (High-Level)

### Project List Screen

**Display:**
- List of all projects with:
  - Project name
  - Status badge
  - Document scope indicator
  - Created/updated timestamps
  - Action buttons (view, delete)

**User Interactions:**
- Create new project button
- Filter by status
- Sort by date/name
- Click project to view details

### Project Detail Screen

**Display:**
- Project information (name, status, scope)
- Questionnaire sections and questions
- Answer status for each question
- Document list (if SPECIFIC scope)
- Action buttons (generate answers, evaluate)

**User Interactions:**
- Expand/collapse sections
- Click question to review answer
- Generate all answers button
- View evaluation report button

### Question Review Screen

**Display:**
- Question text
- AI-generated answer
- Citations with bounding box references
- Confidence score indicator
- Answerability indicator
- Review status selector
- Manual answer input field

**User Interactions:**
- Review status dropdown (CONFIRMED, REJECTED, MANUAL_UPDATED, MISSING_DATA)
- Enter manual answer text
- View citations (click to highlight in document)
- Save review
- Navigate to next/previous question

### Document Management Screen

**Display:**
- List of all documents
- Document status (indexed/not indexed)
- Upload date
- File size and format
- Indexing status

**User Interactions:**
- Upload new document
- View document details
- Delete document
- Re-index document
- Filter by format/status

### Evaluation Report Screen

**Display:**
- Project information
- Evaluation summary (average score, distribution)
- List of evaluated answers:
  - Question text
  - AI answer
  - Human answer
  - Similarity score
  - Qualitative explanation
- Score visualization (charts/graphs)

**User Interactions:**
- Run evaluation button
- Export report
- Filter by score range
- Sort by score

### Request Status Tracking

**Display:**
- List of async requests
- Request type
- Status badge
- Progress bar (if processing)
- Error message (if failed)
- Result summary (if completed)

**User Interactions:**
- Refresh status
- View detailed results
- Retry failed requests
- Cancel pending requests

## Error Handling

### Common Error Scenarios

1. **Document Parsing Failure**
   - Error: Unsupported format or corrupted file
   - Handling: Return error status, log details, allow retry

2. **Questionnaire Parsing Failure**
   - Error: Invalid structure or format
   - Handling: Return error status, provide parsing details

3. **No Relevant Documents**
   - Error: Question cannot be answered
   - Handling: Return answer with is_answerable=false, empty citations

4. **LLM Service Failure**
   - Error: API timeout or service unavailable
   - Handling: Retry with exponential backoff, return error status

5. **Vector Store Failure**
   - Error: Search timeout or connection error
   - Handling: Retry, fallback to keyword search if available

6. **Database Failure**
   - Error: Connection lost or query timeout
   - Handling: Retry, return error status, log for admin

### Missing Data Handling

- **Missing Documents**: Project creation fails if SPECIFIC scope with invalid document IDs
- **Missing Questions**: Answer generation fails gracefully with error message
- **Missing Citations**: Answer stored with empty citations, confidence adjusted
- **Missing Manual Answers**: Evaluation skips answers without ground truth

### Regeneration Logic

**Triggers:**
- Document scope changed
- New documents indexed (for ALL_DOCS projects)
- User manually triggers regeneration

**Process:**
1. Mark existing answers as needing regeneration
2. Clear or invalidate cached answers
3. Optionally auto-regenerate if configured
4. Update project status to PROCESSING
5. Generate new answers
6. Update project status to COMPLETED
