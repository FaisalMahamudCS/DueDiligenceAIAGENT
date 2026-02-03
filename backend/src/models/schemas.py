"""Pydantic models for request/response schemas."""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from enum import Enum


# Enums
class AnswerReviewStatus(str, Enum):
    """Review status for answers."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    MANUAL_UPDATED = "manual_updated"
    MISSING_DATA = "missing_data"


class DocumentScope(str, Enum):
    """Document scope for projects."""
    ALL_DOCS = "ALL_DOCS"
    SPECIFIC = "SPECIFIC"


# Citation models
class BoundingBox(BaseModel):
    """Bounding box coordinates for citation references."""
    page: int
    x0: float
    y0: float
    x1: float
    y1: float


class Citation(BaseModel):
    """Citation reference with chunk and bounding box."""
    document_id: str
    document_name: str
    chunk_id: str
    chunk_text: str
    page_number: int
    bounding_box: Optional[BoundingBox] = None
    relevance_score: Optional[float] = None


# Project models
class ProjectCreate(BaseModel):
    """Schema for creating a new project."""
    name: str
    questionnaire_file_path: Optional[str] = None
    questionnaire_file_url: Optional[str] = None
    document_scope: DocumentScope = DocumentScope.ALL_DOCS
    document_ids: Optional[List[str]] = None  # Required if scope is SPECIFIC
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ProjectInfo(BaseModel):
    """Schema for project information."""
    project_id: str
    name: str
    description: Optional[str] = None
    status: str  # creating, ready, processing, completed, outdated, error
    document_scope: DocumentScope
    document_ids: Optional[List[str]] = None
    questionnaire_id: Optional[str] = None
    created_at: str
    updated_at: str
    metadata: Optional[Dict[str, Any]] = None


# Questionnaire models
class Question(BaseModel):
    """Schema for a questionnaire question."""
    question_id: str
    section_id: str
    section_name: Optional[str] = None
    question_text: str
    question_number: Optional[str] = None
    order: int
    metadata: Optional[Dict[str, Any]] = None


class Section(BaseModel):
    """Schema for a questionnaire section."""
    section_id: str
    section_name: str
    order: int
    questions: List[Question]
    metadata: Optional[Dict[str, Any]] = None


class Questionnaire(BaseModel):
    """Schema for a parsed questionnaire."""
    questionnaire_id: str
    name: str
    sections: List[Section]
    total_questions: int
    created_at: str
    metadata: Optional[Dict[str, Any]] = None


# Answer models
class AnswerRequest(BaseModel):
    """Schema for generating/updating an answer."""
    project_id: str
    question_id: str
    question_text: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class AnswerResponse(BaseModel):
    """Schema for answer response with citations and confidence."""
    answer_id: str
    project_id: str
    question_id: str
    question_text: str
    answer_text: str
    is_answerable: bool  # Indicates if answer is possible
    confidence: float  # Confidence score (0.0 to 1.0)
    citations: List[Citation]  # Citation chunks with bounding boxes
    review_status: AnswerReviewStatus = AnswerReviewStatus.PENDING
    manual_answer_text: Optional[str] = None  # Human-provided answer
    created_at: str
    updated_at: str


class AnswerUpdate(BaseModel):
    """Schema for updating an answer (review workflow)."""
    answer_id: str
    review_status: AnswerReviewStatus
    manual_answer_text: Optional[str] = None
    notes: Optional[str] = None


# Document indexing models
class DocumentIndexRequest(BaseModel):
    """Schema for indexing a document."""
    document_path: Optional[str] = None
    document_url: Optional[str] = None
    document_name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class DocumentInfo(BaseModel):
    """Schema for document information."""
    document_id: str
    document_name: str
    file_path: str
    file_format: str
    file_size: int
    indexed: bool
    indexed_at: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# Status models
class RequestStatus(BaseModel):
    """Schema for async request status."""
    request_id: str
    status: str  # pending, processing, completed, failed
    progress: Optional[float] = None  # 0.0 to 1.0
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: str
    updated_at: str


# Evaluation models
class EvaluationResult(BaseModel):
    """Schema for evaluation result comparing AI vs human answers."""
    evaluation_id: str
    project_id: str
    answer_id: str
    question_id: str
    ai_answer_text: str
    human_answer_text: str
    similarity_score: float  # 0.0 to 1.0
    semantic_similarity: float
    keyword_overlap: float
    qualitative_explanation: str
    created_at: str


class EvaluationReport(BaseModel):
    """Schema for evaluation report across all answers."""
    report_id: str
    project_id: str
    total_questions: int
    evaluated_questions: int
    average_similarity_score: float
    results: List[EvaluationResult]
    created_at: str
