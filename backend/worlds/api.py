"""
API endpoints for world management.
"""

from ninja import Router
from typing import List
from .models import World, Location, Character, Object, Treaty

router = Router()


@router.get("/list")
def list_worlds(request):
    """List all available worlds."""
    worlds = World.objects.all()
    return [
        {
            "id": str(w.id),
            "name": w.name,
            "description": w.description,
            "times_witnessed": w.times_witnessed,
            "source_type": w.source_type,
        }
        for w in worlds
    ]


@router.get("/{world_id}")
def get_world(request, world_id: str):
    """Get detailed world information."""
    world = World.objects.get(id=world_id)
    return {
        "id": str(world.id),
        "name": world.name,
        "description": world.description,
        "witness_config": world.witness_config,
        "resource_types": world.resource_types,
        "degradation_pattern": world.degradation_pattern,
        "hidden_truth": world.hidden_truth,
        "locations": world.locations.count(),
        "characters": world.characters.count(),
        "objects": world.objects.count(),
    }


@router.get("/{world_id}/locations")
def get_locations(request, world_id: str):
    """Get all locations in a world."""
    locations = Location.objects.filter(world_id=world_id)
    return [
        {
            "id": str(loc.id),
            "name": loc.name,
            "description": loc.description,
            "integrity": loc.integrity,
            "color_saturation": loc.color_saturation,
            "has_been_witnessed": loc.has_been_witnessed,
        }
        for loc in locations
    ]


@router.get("/{world_id}/characters")
def get_characters(request, world_id: str):
    """Get all characters in a world."""
    characters = Character.objects.filter(world_id=world_id)
    return [
        {
            "id": str(char.id),
            "name": char.name,
            "description": char.description,
            "has_agency": char.has_agency,
            "power_level": char.power_level,
            "alive": char.alive,
            "memory_intact": char.memory_intact,
        }
        for char in characters
    ]