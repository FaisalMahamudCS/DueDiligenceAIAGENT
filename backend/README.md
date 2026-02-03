Backend Skeleton (Minimal Framework)

Purpose
This folder holds the backend service implementation for the Questionnaire
Agent. It uses a minimal FastAPI setup and serves as the starting point for
implementation.

The system automates due diligence questionnaires by:
- Indexing company documents (PDF, DOCX, XLSX, PPTX)
- Parsing questionnaire files into structured questions
- Generating AI answers with citations and confidence scores
- Supporting human review workflows
- Evaluating answers against ground-truth

Planned Modules
- src/api/        HTTP route handlers for the listed endpoints
- src/models/     Data models mirroring the spec data structures
- src/services/   Core business logic (project, answers, ingestion, evaluation)
- src/indexing/   Multi-layer indexing pipeline and chunking
- src/storage/    Persistence layer (DB, vector store, object storage)
- src/workers/    Async/background processing and request status tracking
- src/utils/      Shared helpers, validation, and constants

Endpoints (to be implemented)
- POST /create-project-async      Create project with questionnaire parsing
- POST /generate-single-answer    Generate answer with citations & confidence
- POST /generate-all-answers      Generate all answers for a project (async)
- POST /update-project-async      Update project configuration (async)
- POST /update-answer             Update answer review status
- GET /get-project-info           Get project information
- GET /get-project-status         Get project status
- POST /index-document-async      Index document with multi-layer pipeline (async)
- GET /get-request-status         Get async request status
- POST /evaluate-project          Evaluate AI answers vs human ground truth

Key Features
- Multi-layer indexing: answer retrieval + citation chunks with bounding boxes
- Document scope: ALL_DOCS projects automatically marked OUTDATED on new docs
- Answer review workflow: CONFIRMED, REJECTED, MANUAL_UPDATED, MISSING_DATA
- Evaluation framework: semantic similarity + keyword overlap metrics
- Async processing: background tasks with status tracking
