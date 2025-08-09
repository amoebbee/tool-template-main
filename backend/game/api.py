"""
API endpoints for game sessions.
"""

from ninja import Router
from typing import Optional
from .models import GameSession, Knowledge, Conversation, Message, Discovery
from worlds.models import World
import uuid

router = Router()


@router.post("/start")
def start_session(request, world_id: str, witness_name: str, witness_size: str = "thumb"):
    """Start a new witness session."""
    world = World.objects.get(id=world_id)
    world.times_witnessed += 1
    world.save()
    
    session = GameSession.objects.create(
        world=world,
        witness_name=witness_name,
        witness_size=witness_size,
        player_id=str(uuid.uuid4()) if not request.user.is_authenticated else None,
        player=request.user if request.user.is_authenticated else None,
    )
    
    # Add first whisper
    Knowledge.objects.create(
        session=session,
        knowledge_type='whisper',
        content='The night has no intention of ending',
        base_weight=0,  # First one's free
        night_discovered=1,
    )
    
    return {
        "session_id": str(session.id),
        "witness_name": session.witness_name,
        "world_name": world.name,
        "night_count": 1,
        "message": "The endless night begins..."
    }


@router.get("/{session_id}/state")
def get_session_state(request, session_id: str):
    """Get current session state."""
    session = GameSession.objects.get(id=session_id)
    
    return {
        "session_id": str(session.id),
        "night_count": session.night_count,
        "total_weight": session.total_weight,
        "movement_speed": session.movement_speed,
        "world_entropy": session.world_entropy,
        "text_degradation": session.text_degradation,
        "color_loss": session.color_loss,
        "current_location": str(session.current_location.id) if session.current_location else None,
        "knowledge_count": session.knowledge.count(),
        "is_active": session.is_active,
    }


@router.post("/{session_id}/advance-night")
def advance_night(request, session_id: str):
    """Advance to the next night."""
    session = GameSession.objects.get(id=session_id)
    session.advance_night()
    
    # Degrade world
    if session.current_location:
        session.current_location.degrade()
    
    return {
        "night_count": session.night_count,
        "world_entropy": session.world_entropy,
        "message": f"Night {session.night_count} falls. Everything degrades a little more."
    }


@router.post("/{session_id}/discover")
def add_discovery(request, session_id: str, content: str, knowledge_type: str = "whisper"):
    """Add a new piece of knowledge."""
    session = GameSession.objects.get(id=session_id)
    
    knowledge = Knowledge.objects.create(
        session=session,
        knowledge_type=knowledge_type,
        content=content,
        night_discovered=session.night_count,
        discovered_at=session.current_location,
    )
    
    weight = knowledge.calculate_weight()
    session.add_weight(weight)
    
    return {
        "knowledge_id": str(knowledge.id),
        "weight_added": weight,
        "total_weight": session.total_weight,
        "movement_speed": session.movement_speed,
        "message": f"The weight of knowledge grows heavier. Speed: {session.movement_speed:.2f}"
    }