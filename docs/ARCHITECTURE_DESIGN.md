# Architecture Design

## System Overview

The Questionnaire Agent is a full-stack AI system that automates due diligence questionnaire completion. It ingests company documents, parses questionnaire files, generates AI-powered answers with citations, and supports human review workflows with evaluation capabilities.

## Component Boundaries

### Backend Components

1. **API Layer** (`src/api/`)
   - FastAPI REST endpoints
   - Request/response validation
   - Error handling and status codes

2. **Service Layer** (`src/services/`)
   - Business logic orchestration
   - Project management
   - Answer generation
   - Questionnaire parsing
   - Document ingestion
   - Evaluation framework

3. **AI/LLM Layer** (`src/services/llm_service.py`)
   - LLM integration (OpenAI, Anthropic, etc.)
   - Answer generation from context
   - Embedding generation
   - Semantic similarity calculation
   - Prompt construction and management

4. **Indexing Layer** (`src/indexing/`)
   - Multi-layer indexing pipeline
   - Document chunking
   - Embedding generation (via LLM service)
   - Semantic retrieval

5. **Storage Layer** (`src/storage/`)
   - Relational database (projects, questions, answers, questionnaires)
   - Vector store (embeddings for semantic search)
   - Object storage (document files)

6. **Worker Layer** (`src/workers/`)
   - Async task queue
   - Background job processing
   - Status tracking

7. **Utility Layer** (`src/utils/`)
   - Document parsing (PDF, DOCX, XLSX, PPTX)
   - Validation helpers
   - Constants and configuration

### Frontend Components

1. **Pages** (`src/pages/`)
   - Project list view
   - Project detail view
   - Question review interface
   - Document management
   - Evaluation report

2. **Components** (`src/components/`)
   - Reusable UI components
   - Citation display
   - Confidence indicators
   - Status badges

3. **Services** (`src/services/`)
   - API client
   - Request helpers
   - Error handling

4. **State Management** (`src/state/`)
   - Client-side state
   - Cache management
   - Real-time updates

## Data Flow

### Document Ingestion Flow
```
User uploads document
  → DocumentService.ingest_document()
  → DocumentParser.parse_document()
  → ObjectStorage.upload_file()
  → IndexingPipeline.index_document()
  → VectorStore.store_embeddings()
  → Database.save_document()
  → DocumentService.mark_projects_outdated() (if ALL_DOCS projects exist)
```

### Project Creation Flow
```
User creates project with questionnaire
  → API: POST /create-project-async
  → TaskQueue.enqueue_task()
  → Worker: Parse questionnaire
  → QuestionnaireService.parse_questionnaire()
  → Database.save_questionnaire()
  → Database.save_project()
  → Update status to READY
```

### Answer Generation Flow
```
User requests answer generation
  → API: POST /generate-single-answer
  → AnswerService.generate_single_answer()
  → IndexingPipeline.retrieve_relevant_chunks() (Layer 1: semantic search)
  → VectorStore.search_similar()
  → IndexingPipeline.get_citation_chunks() (Layer 2: citation extraction)
  → LLMService.generate_answer() (AI generates answer from context)
  → AnswerService calculates confidence & answerability
  → Database.save_answer()
  → Return AnswerResponse with citations
```

### Review Workflow Flow
```
User reviews answer
  → API: POST /update-answer
  → AnswerService.update_answer()
  → Validate review_status transition
  → Store manual_answer_text (if provided)
  → Preserve AI answer for comparison
  → Database.update_answer()
```

### Evaluation Flow
```
User requests evaluation
  → API: POST /evaluate-project
  → EvaluationService.evaluate_project()
  → Get all answers with manual_answer_text
  → For each answer:
    → Calculate semantic similarity
    → Calculate keyword overlap
    → Generate combined score
    → Create qualitative explanation
  → Generate EvaluationReport
  → Database.save_evaluation_report()
```

## Storage Layout

### Database Schema (Relational)

**projects**
- project_id (PK)
- name
- description
- status (enum: creating, ready, processing, completed, outdated, error)
- document_scope (enum: ALL_DOCS, SPECIFIC)
- questionnaire_id (FK)
- created_at, updated_at
- metadata (JSON)

**questionnaires**
- questionnaire_id (PK)
- name
- source_file_path
- created_at
- metadata (JSON)

**sections**
- section_id (PK)
- questionnaire_id (FK)
- section_name
- order
- metadata (JSON)

**questions**
- question_id (PK)
- section_id (FK)
- question_text
- question_number
- order
- metadata (JSON)

**documents**
- document_id (PK)
- document_name
- file_path
- file_format
- file_size
- indexed (boolean)
- indexed_at
- created_at
- metadata (JSON)

**project_documents** (junction table for SPECIFIC scope)
- project_id (FK)
- document_id (FK)

**answers**
- answer_id (PK)
- project_id (FK)
- question_id (FK)
- question_text
- answer_text (AI-generated)
- manual_answer_text (human-provided)
- is_answerable (boolean)
- confidence (float 0.0-1.0)
- review_status (enum: pending, confirmed, rejected, manual_updated, missing_data)
- created_at, updated_at
- metadata (JSON)

**citations**
- citation_id (PK)
- answer_id (FK)
- document_id (FK)
- chunk_id
- chunk_text
- page_number
- bounding_box (JSON: {x0, y0, x1, y1})
- relevance_score (float)
- order

**evaluation_results**
- evaluation_id (PK)
- project_id (FK)
- answer_id (FK)
- similarity_score (float)
- semantic_similarity (float)
- keyword_overlap (float)
- qualitative_explanation (text)
- created_at

**async_requests**
- request_id (PK)
- request_type (enum)
- status (enum: pending, processing, completed, failed)
- progress (float 0.0-1.0)
- result (JSON)
- error (text)
- created_at, updated_at

### Vector Store Schema

**embeddings**
- chunk_id (PK)
- document_id
- chunk_text
- embedding_vector (array of floats)
- metadata (JSON: page_number, bounding_box, etc.)

### Object Storage

**Structure**: `{project_id}/{document_id}/{filename}`
- Stores original document files
- Supports versioning if needed

## Status Transitions

### Project Status
```
creating → ready → processing → completed
                ↓
            outdated (when new docs indexed for ALL_DOCS projects)
                ↓
            error (on failure)
```

### Answer Review Status
```
pending → confirmed
       → rejected
       → manual_updated
       → missing_data
```

### Async Request Status
```
pending → processing → completed
                      ↓
                   failed
```

## Integration Points

1. **LLM Service**: External API for answer generation
   - OpenAI GPT-4, Anthropic Claude, or similar
   - Used via `LLMService` wrapper class
   - Handles prompt construction, API calls, response parsing

2. **Embedding Service**: External API for vector embeddings
   - OpenAI text-embedding-ada-002, or similar
   - Used via `LLMService.generate_embedding()`
   - Creates vector representations for semantic search

3. **File Storage**: S3-compatible object storage
   - AWS S3, MinIO, or similar
   - Stores original document files

4. **Vector Database**: Pinecone, Weaviate, or similar
   - Stores document embeddings for semantic search
   - Enables fast similarity queries

5. **Relational Database**: PostgreSQL or SQLite
   - Stores projects, questions, answers, questionnaires
   - Maintains relationships and metadata
