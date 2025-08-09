"""
API endpoints for world parsing.
"""

from ninja import Router
from ninja.files import UploadedFile
from typing import Optional
from .models import ParseSession, ExtractedEntity
import uuid

router = Router()


@router.post("/start")
def start_parse_session(
    request,
    world_name: str,
    source_type: str,
    witness_type: str = "auto",
    source_text: Optional[str] = None,
    source_file: Optional[UploadedFile] = None,
):
    """Start a new parsing session."""
    session = ParseSession.objects.create(
        world_name=world_name,
        source_type=source_type,
        witness_type=witness_type,
        source_text=source_text or "",
    )
    
    if source_file:
        # Save uploaded file
        session.source_file = source_file
        session.save()
    
    return {
        "session_id": str(session.id),
        "world_name": world_name,
        "status": "created",
        "message": "Parse session created. Ready to extract entities."
    }


@router.get("/{session_id}/status")
def get_parse_status(request, session_id: str):
    """Get parsing session status."""
    session = ParseSession.objects.get(id=session_id)
    
    return {
        "session_id": str(session.id),
        "world_name": session.world_name,
        "stages": {
            "extraction": session.extraction_complete,
            "entities": session.entities_identified,
            "witness": session.witness_selected,
            "resources": session.resources_defined,
            "world": session.world_created,
        },
        "entity_count": session.extracted_entities.count(),
        "world_id": str(session.world.id) if session.world else None,
        "error": session.error_log if session.error_log else None,
    }


@router.post("/{session_id}/extract")
def extract_entities(request, session_id: str):
    """Extract entities from source material."""
    session = ParseSession.objects.get(id=session_id)
    
    # Placeholder for actual extraction logic
    # This would use NLP/LLM to extract entities
    
    session.extraction_complete = True
    session.entities_identified = True
    session.save()
    
    return {
        "session_id": str(session.id),
        "status": "extracted",
        "message": "Entities extracted from source material."
    }


@router.get("/{session_id}/entities")
def get_extracted_entities(request, session_id: str):
    """Get all extracted entities."""
    entities = ExtractedEntity.objects.filter(session_id=session_id)
    
    return [
        {
            "id": str(e.id),
            "type": e.entity_type,
            "name": e.name,
            "description": e.description,
            "importance": e.importance_score,
            "is_witness_candidate": e.is_witness_candidate,
        }
        for e in entities
    ]


@router.post("/{session_id}/create-world")
def create_world_from_parse(request, session_id: str):
    """Create the world from parsed entities."""
    session = ParseSession.objects.get(id=session_id)
    
    if not session.entities_identified:
        return {"error": "Entities must be extracted first"}
    
    # Placeholder for world creation logic
    # This would transform entities into world models
    
    session.world_created = True
    session.save()
    
    return {
        "session_id": str(session.id),
        "status": "complete",
        "world_id": str(session.world.id) if session.world else None,
        "message": "World created successfully. Ready to witness."
    }