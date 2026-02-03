"""Shared constants and configuration."""

# API Constants
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Task/Request Status
TASK_STATUS_PENDING = "pending"
TASK_STATUS_PROCESSING = "processing"
TASK_STATUS_COMPLETED = "completed"
TASK_STATUS_FAILED = "failed"

# Project Status
PROJECT_STATUS_CREATING = "creating"
PROJECT_STATUS_READY = "ready"
PROJECT_STATUS_PROCESSING = "processing"
PROJECT_STATUS_COMPLETED = "completed"
PROJECT_STATUS_OUTDATED = "outdated"  # When new docs are indexed for ALL_DOCS projects
PROJECT_STATUS_ERROR = "error"

# Answer Review Status
ANSWER_STATUS_PENDING = "pending"
ANSWER_STATUS_CONFIRMED = "confirmed"
ANSWER_STATUS_REJECTED = "rejected"
ANSWER_STATUS_MANUAL_UPDATED = "manual_updated"
ANSWER_STATUS_MISSING_DATA = "missing_data"

# Document Scope
DOCUMENT_SCOPE_ALL_DOCS = "ALL_DOCS"  # Project uses all indexed documents
DOCUMENT_SCOPE_SPECIFIC = "SPECIFIC"  # Project uses specific document IDs

# Supported Document Formats
SUPPORTED_FORMATS = [".pdf", ".docx", ".xlsx", ".pptx"]

# Default Values
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_TOP_K = 5
DEFAULT_CONFIDENCE_THRESHOLD = 0.7

# Indexing Layers
INDEX_LAYER_ANSWER_RETRIEVAL = "answer_retrieval"  # Layer 1: section or semantic retrieval
INDEX_LAYER_CITATION_CHUNKS = "citation_chunks"  # Layer 2: citation chunks with bounding boxes
