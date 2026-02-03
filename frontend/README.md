Frontend Skeleton (Minimal Framework)

Purpose
This folder holds the frontend implementation for the Questionnaire Agent.
It uses a minimal Vite + React + TypeScript setup and serves as the starting
point for implementation.

Structure
- src/pages/       Page-level containers (6 screens)
- src/components/  Reusable UI components
- src/services/    API clients and request helpers
- src/state/       Client state management

Pages (Skeleton Created)
- ProjectList.tsx          - View all projects and their status
- ProjectDetail.tsx        - Sections, questions, and answers with review actions
- QuestionReview.tsx       - Approve/reject/manual edit with citations and confidence
- DocumentManagement.tsx  - Upload, scope, and indexing status
- EvaluationReport.tsx    - Compare AI vs human answers with similarity scores
- RequestStatus.tsx       - Async task tracking and error details

Components (Skeleton Created)
- StatusBadge.tsx         - Status badge display component
- CitationDisplay.tsx     - Citation list with document references
- ConfidenceIndicator.tsx - Visual confidence score indicator

Services (Skeleton Created)
- api.ts                  - Centralized API client for backend communication

State (Skeleton Created)
- store.ts                - Client state management setup

All skeleton files include TODO comments indicating where implementation
logic should be added. The structure demonstrates the planned architecture
without full implementation.
