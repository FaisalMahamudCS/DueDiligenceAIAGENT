# Due Diligence Questionnaire Agent

A full-stack AI system to automate due diligence questionnaires. It indexes company documents (e.g., financials and reports), parses questionnaire files into structured questions, generates AI answers with citations and confidence scores, and supports human review plus evaluation against ground-truth answers.

## Submission Contents

This submission includes:

### 📚 Comprehensive Design Documentation
- **`docs/ARCHITECTURE_DESIGN.md`** - System architecture, component boundaries, data flow, and storage layout
- **`docs/FUNCTIONAL_DESIGN.md`** - Detailed functional specifications covering all 8 scope areas with acceptance criteria
- **`docs/TESTING_EVALUATION.md`** - Testing plan, QA checklist, and evaluation metrics
- **`docs/QUESTIONNAIRE_STRUCTURE.md`** - ILPA questionnaire structure analysis and parsing strategy
- **`docs/QUESTIONNAIRE_PARSING_EXPLAINED.md`** - Step-by-step explanation of how questionnaire parsing works
- **`docs/CORE_CONCEPTS.md`** - Simple explanations of questionnaire parsing and AI/LLM layer

### 💻 Code Skeleton (Demonstration of Structure)
- **`backend/`** - FastAPI backend skeleton with organized modules and endpoint stubs
- **`frontend/`** - React + Vite frontend skeleton with planned UI structure

### 📋 Project Structure
- **`backend/src/`** - Backend modules (API, services, models, indexing, storage, workers, utils)
- **`frontend/src/`** - Frontend modules (pages, components, services, state)
- **`data/`** - Sample PDFs for testing (questionnaire + reference documents)
- **`docs/`** - Complete design documentation

## Documentation Coverage

✅ **All 8 Scope Areas Documented:**
1. Product & Data Model Alignment
2. Document Ingestion & Indexing (multi-layer indexing)
3. Questionnaire Parsing & Project Lifecycle
4. Answer Generation with Citations & Confidence
5. Review & Manual Overrides
6. Evaluation Framework
7. Optional Chat Extension
8. Frontend Experience

✅ **All Acceptance Criteria Met:**
- Documentation completeness
- Functional accuracy
- Review & auditability
- Evaluation framework
- Non-functional requirements
- Frontend UX

## Design Decisions & Tradeoffs

### Approach
- **Primary Focus**: Comprehensive design documentation (fulfills "task descriptions only" requirement)
- **Bonus**: Code skeleton demonstrating technical structure and organization
- **Rationale**: Shows both design thinking and implementation understanding

### Technology Stack
- **Backend**: FastAPI (Python) - modern, async-capable, auto-documentation
- **Frontend**: React + TypeScript + Vite - component-based, type-safe, fast dev experience
- **Storage**: PostgreSQL (relational), Vector DB (embeddings), S3-compatible (objects)

### Key Design Choices
1. **Multi-layer Indexing**: Layer 1 (semantic retrieval) + Layer 2 (citation chunks with bounding boxes)
2. **Async Processing**: All heavy operations (indexing, project creation) are async with status tracking
3. **ALL_DOCS Outdated Logic**: Projects automatically marked OUTDATED when new documents indexed
4. **Dual Answer Storage**: AI and manual answers preserved separately for evaluation
5. **Combined Evaluation Metrics**: Semantic similarity (70%) + keyword overlap (30%)

## Dataset Testing Plan

Sample PDFs in `data/` directory:
- `ILPA_Due_Diligence_Questionnaire_v1.2.pdf` - Questionnaire input
- `20260110_MiniMax_*.pdf` - Reference documents for answering

Testing scenarios documented in `docs/TESTING_EVALUATION.md`:
1. Basic workflow validation
2. ALL_DOCS outdated behavior
3. Citation validation
4. Review workflow
5. Evaluation framework

## Getting Started

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Submission Notes

This submission demonstrates:
- **Design Thinking**: Comprehensive documentation covering all requirements
- **Technical Understanding**: Well-organized code skeleton showing implementation approach
- **System Design**: Clear architecture, data flows, and component boundaries
- **Practical Considerations**: Error handling, async processing, evaluation metrics

See `SUBMISSION_GUIDE.md` for detailed submission information.
