"""Validation utilities."""

from typing import Dict, Any, Optional
from fastapi import HTTPException


def validate_project_id(project_id: str) -> str:
    """Validate a project ID."""
    if not project_id or not isinstance(project_id, str):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    return project_id.strip()


def validate_question_id(question_id: str) -> str:
    """Validate a question ID."""
    if not question_id or not isinstance(question_id, str):
        raise HTTPException(status_code=400, detail="Invalid question ID")
    return question_id.strip()


def validate_request_id(request_id: str) -> str:
    """Validate a request ID."""
    if not request_id or not isinstance(request_id, str):
        raise HTTPException(status_code=400, detail="Invalid request ID")
    return request_id.strip()


def validate_required_fields(data: Dict[str, Any], required_fields: list) -> Dict[str, Any]:
    """Validate that required fields are present in the data."""
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required fields: {', '.join(missing_fields)}"
        )
    return data

