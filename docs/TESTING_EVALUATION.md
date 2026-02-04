# Testing & Evaluation

## Dataset Testing Plan

### Test Dataset

**Location**: `data/` directory

**Files**:
- `ILPA_Due_Diligence_Questionnaire_v1.2.pdf` - Questionnaire input
- `20260110_MiniMax_Accountants_Report.pdf` - Reference document
- `20260110_MiniMax_Audited_Consolidated_Financial_Statements.pdf` - Reference document
- `20260110_MiniMax_Global_Offering_Prospectus.pdf` - Reference document
- `20260110_MiniMax_Industry_Report.pdf` - Reference document

### Test Scenarios

#### Scenario 1: Basic Workflow Validation

**Steps**:
1. Index all reference PDFs (4 documents)
2. Create project with questionnaire PDF
3. Set document scope to ALL_DOCS
4. Generate answers for all questions
5. Verify answers include:
   - Answer text
   - is_answerable flag
   - Confidence score (0.0-1.0)
   - Citations with bounding boxes

**Expected Results**:
- All documents indexed successfully
- Project created with status READY
- Answers generated with proper structure
- Citations reference correct documents and pages

**Acceptance Criteria**:
- ✅ All documents indexed
- ✅ Project status = READY
- ✅ All answers have required fields
- ✅ Citations contain valid document references

#### Scenario 2: ALL_DOCS Outdated Behavior

**Steps**:
1. Index initial 4 reference documents
2. Create project with ALL_DOCS scope
3. Generate answers
4. Index a new document (5th document)
5. Check project status

**Expected Results**:
- Project status changes to OUTDATED after new document indexed
- Existing answers remain but marked as potentially incomplete

**Acceptance Criteria**:
- ✅ Project status = OUTDATED after new document indexed
- ✅ Timestamp updated_at reflects change
- ✅ Existing answers preserved

#### Scenario 3: Citation Validation

**Steps**:
1. Generate answer for specific question
2. Verify citations include:
   - Document ID and name
   - Page number
   - Bounding box coordinates
   - Chunk text
   - Relevance score

**Expected Results**:
- Citations are valid and reference actual document content
- Bounding boxes are within page dimensions
- Chunk text matches document content

**Acceptance Criteria**:
- ✅ All citations have required fields
- ✅ Bounding boxes are valid (0 <= x0 < x1 <= page_width, same for y)
- ✅ Chunk text appears in source document
- ✅ Relevance scores are between 0.0 and 1.0

#### Scenario 4: Review Workflow

**Steps**:
1. Generate answer
2. Review and set status to CONFIRMED
3. Generate another answer
4. Review and set status to MANUAL_UPDATED with manual text
5. Verify both AI and manual answers stored

**Expected Results**:
- Review status updates correctly
- Manual answer stored alongside AI answer
- Both answers preserved for comparison

**Acceptance Criteria**:
- ✅ Status transitions work correctly
- ✅ Manual answer text stored
- ✅ AI answer text preserved
- ✅ Both answers accessible for evaluation

#### Scenario 5: Evaluation Framework

**Steps**:
1. Generate answers for multiple questions
2. Provide manual answers (ground truth) for subset
3. Run evaluation
4. Verify evaluation report includes:
   - Similarity scores
   - Semantic similarity metrics
   - Keyword overlap metrics
   - Qualitative explanations

**Expected Results**:
- Evaluation runs successfully
- Scores calculated correctly
- Explanations are meaningful
- Report includes aggregate statistics

**Acceptance Criteria**:
- ✅ Evaluation completes without errors
- ✅ Scores are between 0.0 and 1.0
- ✅ Explanations provided for each answer
- ✅ Aggregate statistics calculated correctly

## QA Checklist

### Functional Testing

- [ ] Document ingestion (PDF, DOCX, XLSX, PPTX)
- [ ] Questionnaire parsing with sections and questions
- [ ] Project creation with ALL_DOCS scope
- [ ] Project creation with SPECIFIC scope
- [ ] Answer generation with citations
- [ ] Answer generation with confidence scores
- [ ] Answer generation with answerability indicator
- [ ] Review workflow (all status transitions)
- [ ] Manual answer storage
- [ ] Evaluation framework
- [ ] ALL_DOCS outdated behavior
- [ ] Async request status tracking

### Non-Functional Testing

- [ ] API response times (< 2s for synchronous endpoints)
- [ ] Async task completion (< 5min for large projects)
- [ ] Error handling (graceful failures)
- [ ] Data validation (invalid inputs rejected)
- [ ] Concurrent request handling
- [ ] Large document processing (> 100 pages)
- [ ] Large questionnaire processing (> 100 questions)

### Integration Testing

- [ ] Database connectivity and transactions
- [ ] Vector store connectivity and queries
- [ ] Object storage upload/download
- [ ] LLM service integration
- [ ] Embedding service integration
- [ ] Frontend-backend API communication

### Edge Cases

- [ ] Empty questionnaire
- [ ] Questionnaire with no questions
- [ ] Document with no text content
- [ ] Question with no relevant documents
- [ ] Concurrent document indexing
- [ ] Project update during answer generation
- [ ] Evaluation with no manual answers

## Evaluation Metrics

### Answer Quality Metrics

**Confidence Score Distribution**:
- Track distribution of confidence scores
- Identify questions with consistently low confidence
- Target: > 70% of answers with confidence > 0.7

**Answerability Rate**:
- Percentage of questions that are answerable
- Target: > 80% answerability for well-indexed documents

**Citation Quality**:
- Average number of citations per answer
- Relevance scores of citations
- Target: Average 3-5 citations per answer, relevance > 0.6

### Evaluation Metrics

**Similarity Score Distribution**:
- Track distribution of similarity scores (AI vs human)
- Target: Average similarity > 0.75

**Semantic Similarity**:
- Average semantic similarity score
- Target: > 0.70

**Keyword Overlap**:
- Average keyword overlap score
- Target: > 0.60

### System Performance Metrics

**Document Indexing Time**:
- Time to index document by size
- Target: < 30s per 10 pages

**Answer Generation Time**:
- Time to generate single answer
- Target: < 5s per answer

**Project Creation Time**:
- Time to create project and parse questionnaire
- Target: < 60s for 100-question questionnaire

### User Experience Metrics

**Review Workflow Efficiency**:
- Time to review and update answer
- Target: < 30s per answer

**Error Rate**:
- Percentage of failed requests
- Target: < 1% error rate

**Status Update Latency**:
- Time for async status to update
- Target: < 1s polling interval

## Test Data Preparation

### Sample Questionnaire
- Use `ILPA_Due_Diligence_Questionnaire_v1.2.pdf`
- Expected: Multiple sections, 50+ questions
- Validate parsing extracts all questions correctly

### Sample Documents
- Use all 4 MiniMax reference documents
- Expected: Various document types (financials, reports, prospectus)
- Validate indexing extracts text and bounding boxes

### Ground Truth Answers
- Create manual answers for subset of questions (10-20 questions)
- Use for evaluation testing
- Include various answer types (short, long, technical)

## Regression Testing

### Automated Tests

**Unit Tests**:
- Document parser for each format
- Questionnaire parser
- Answer generation logic
- Evaluation metrics calculation
- Status transition validation

**Integration Tests**:
- End-to-end workflow (index → create → generate → review → evaluate)
- API endpoint testing
- Database operations
- Vector store operations

**Performance Tests**:
- Load testing (concurrent requests)
- Stress testing (large documents/questions)
- Endurance testing (long-running operations)

### Manual Testing

**User Acceptance Testing**:
- Complete workflow with real users
- Review UI/UX
- Validate business requirements
- Collect feedback

**Exploratory Testing**:
- Test edge cases
- Test error scenarios
- Test with various document types
- Test with various question types

## Continuous Improvement

### Metrics Tracking

- Log all evaluation scores
- Track answer quality over time
- Monitor system performance
- Identify improvement opportunities

### Feedback Loop

- Collect user feedback on answer quality
- Analyze evaluation results
- Update LLM prompts based on results
- Refine confidence calculation
- Improve citation extraction


