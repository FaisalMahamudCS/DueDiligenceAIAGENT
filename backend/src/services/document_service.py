"""Service for document ingestion and management."""

from typing import Dict, Any, List, Optional
from src.models.schemas import DocumentInfo


class DocumentService:
    """Handles document ingestion, parsing, and management."""

    def __init__(self):
        """Initialize the document service."""
        pass

    async def ingest_document(
        self,
        file_path: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DocumentInfo:
        """Ingest a document (PDF, DOCX, XLSX, PPTX) and extract content."""
        # TODO: Implement document ingestion logic
        # - Support multiple formats (PDF, DOCX, XLSX, PPTX)
        # - Extract text content
        # - Extract metadata
        # - Store document info
        raise NotImplementedError

    async def get_document(self, document_id: str) -> Optional[DocumentInfo]:
        """Get document information by ID."""
        # TODO: Implement document retrieval logic
        raise NotImplementedError

    async def list_documents(
        self,
        project_id: Optional[str] = None
    ) -> List[DocumentInfo]:
        """List all documents, optionally filtered by project."""
        # TODO: Implement document listing logic
        raise NotImplementedError

    async def mark_projects_outdated(self, document_id: str):
        """Mark all ALL_DOCS projects as OUTDATED when a new document is indexed."""
        # TODO: Implement logic to mark ALL_DOCS projects as outdated
        # - Find all projects with document_scope = ALL_DOCS
        # - Update their status to OUTDATED
        raise NotImplementedError

