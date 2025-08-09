"""
API endpoints for LLM character interactions.
"""

from ninja import Router
from typing import Optional
from .models import ConversationContext, CharacterMemory
from game.models import Conversation, Message
from worlds.models import Character

router = Router()


@router.post("/conversation/start")
def start_conversation(request, session_id: str, character_id: str):
    """Start a conversation with a character."""
    from game.models import GameSession
    
    session = GameSession.objects.get(id=session_id)
    character = Character.objects.get(id=character_id)
    
    conversation = Conversation.objects.create(
        session=session,
        character=character,
        location=session.current_location,
        night_occurred=session.night_count,
        text_clarity=max(0.1, 1.0 - session.text_degradation),
        response_coherence=max(0.1, character.memory_intact),
    )
    
    # Create context
    context = ConversationContext.objects.create(
        conversation=conversation,
        degradation_level=session.text_degradation,
        coherence_target=conversation.response_coherence,
        truth_tendency=0.5,  # Could be based on character traits
    )
    
    context.generate_prompt()
    
    return {
        "conversation_id": str(conversation.id),
        "character_name": character.name,
        "text_clarity": conversation.text_clarity,
        "response_coherence": conversation.response_coherence,
        "message": f"You approach {character.name}. They look at you with eyes that have seen {session.night_count} endless nights."
    }


@router.post("/conversation/{conversation_id}/message")
def send_message(request, conversation_id: str, content: str):
    """Send a message to a character."""
    conversation = Conversation.objects.get(id=conversation_id)
    
    # Create witness message
    witness_message = Message.objects.create(
        conversation=conversation,
        speaker='witness',
        original_content=content,
        degraded_content=content,  # Witness text doesn't degrade on input
    )
    
    # Generate character response (placeholder)
    # This would use the LLM provider to generate response
    response_content = f"[{conversation.character.name} responds through the weight of endless nights]"
    
    # Create character response
    character_message = Message.objects.create(
        conversation=conversation,
        speaker='character',
        original_content=response_content,
        degraded_content=response_content,
    )
    
    # Apply degradation
    character_message.degrade_text(conversation.session.text_degradation)
    
    return {
        "witness_message": content,
        "character_response": character_message.degraded_content,
        "degradation_level": conversation.session.text_degradation,
    }


@router.post("/conversation/{conversation_id}/end")
def end_conversation(request, conversation_id: str):
    """End a conversation."""
    conversation = Conversation.objects.get(id=conversation_id)
    conversation.is_active = False
    conversation.save()
    
    # Character forgets a little
    conversation.character.forget(0.02)
    
    return {
        "conversation_id": str(conversation.id),
        "character_memory": conversation.character.memory_intact,
        "message": f"{conversation.character.name} turns away, already forgetting."
    }


@router.get("/character/{character_id}/memories")
def get_character_memories(request, character_id: str):
    """Get a character's accessible memories."""
    memories = CharacterMemory.objects.filter(
        character_id=character_id,
        accessibility__gt=0.1,  # Only somewhat accessible memories
        is_suppressed=False,
    )
    
    return [
        {
            "id": str(m.id),
            "type": m.memory_type,
            "content": m.content if m.clarity > 0.5 else "[unclear memory]",
            "clarity": m.clarity,
            "accessibility": m.accessibility,
        }
        for m in memories
    ]