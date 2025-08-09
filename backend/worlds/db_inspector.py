"""
Database Inspector API for The Endless Nights Engine
Allows peeking into the database and loading fixtures through UI
"""

from ninja import Router, Schema
from typing import List, Dict, Any, Optional
from django.db import connection
from django.core import serializers
from django.core.management import call_command
from django.db.models import Count, Q
import json
import os
from pathlib import Path
from datetime import datetime

from worlds.models import World, Character, Location, Object as WorldObject, Treaty
from game.models import GameSession, Knowledge, Discovery
from parser.models import ParseSession, ExtractedEntity

router = Router()


class WorldSummary(Schema):
    id: str
    name: str
    description: str
    character_count: int
    location_count: int
    object_count: int
    treaty_count: int
    created_at: datetime
    hidden_truth: str
    degradation_speed: float = 1.0


class CharacterDetail(Schema):
    id: str
    name: str
    description: str
    power_level: int
    is_witness_candidate: bool
    memory_intact: float
    alive: bool
    known_truths: List[str]


class LocationDetail(Schema):
    id: str
    name: str
    description: str
    integrity: float
    color_saturation: float
    clarity: float
    witness_count: int


class ObjectDetail(Schema):
    id: str
    name: str
    description: str
    weight: float
    resource_type: str
    condition: float


class DatabaseStats(Schema):
    total_worlds: int
    total_characters: int
    total_locations: int
    total_objects: int
    total_treaties: int
    total_sessions: int
    database_size_mb: float
    most_witnessed_world: Optional[str]


class FixtureInfo(Schema):
    filename: str
    path: str
    size_kb: float
    element_count: int
    created_at: Optional[datetime]


class LoadFixtureRequest(Schema):
    fixture_path: str
    overwrite: bool = False


class LoadFixtureResponse(Schema):
    success: bool
    message: str
    loaded_count: int
    errors: List[str]


@router.get("/stats", response=DatabaseStats)
def get_database_stats(request):
    """Get overall database statistics."""
    
    # Get counts
    stats = {
        'total_worlds': World.objects.count(),
        'total_characters': Character.objects.count(),
        'total_locations': Location.objects.count(),
        'total_objects': WorldObject.objects.count(),
        'total_treaties': Treaty.objects.count(),
        'total_sessions': GameSession.objects.count(),
    }
    
    # Get database size
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT page_count * page_size as size
            FROM pragma_page_count(), pragma_page_size()
        """)
        size_bytes = cursor.fetchone()[0]
        stats['database_size_mb'] = round(size_bytes / (1024 * 1024), 2)
    
    # Get most witnessed world
    most_witnessed = World.objects.order_by('-times_witnessed').first()
    stats['most_witnessed_world'] = most_witnessed.name if most_witnessed else None
    
    return stats


@router.get("/worlds", response=List[WorldSummary])
def list_worlds(request):
    """List all worlds with summary information."""
    worlds = []
    
    for world in World.objects.all():
        degradation = world.degradation_pattern or {}
        
        worlds.append({
            'id': str(world.id),
            'name': world.name,
            'description': world.description,
            'character_count': world.characters.count(),
            'location_count': world.locations.count(),
            'object_count': world.world_objects.count(),
            'treaty_count': world.treaties.count(),
            'created_at': world.created_at,
            'hidden_truth': world.hidden_truth,
            'degradation_speed': degradation.get('speed', 1.0),
        })
    
    return worlds


@router.get("/world/{world_id}/characters", response=List[CharacterDetail])
def get_world_characters(request, world_id: str):
    """Get all characters in a specific world."""
    characters = []
    
    for char in Character.objects.filter(world_id=world_id):
        characters.append({
            'id': str(char.id),
            'name': char.name,
            'description': char.description,
            'power_level': char.power_level,
            'is_witness_candidate': char.is_witness_candidate,
            'memory_intact': char.memory_intact,
            'alive': char.alive,
            'known_truths': char.known_truths,
        })
    
    return characters


@router.get("/world/{world_id}/locations", response=List[LocationDetail])
def get_world_locations(request, world_id: str):
    """Get all locations in a specific world."""
    locations = []
    
    for loc in Location.objects.filter(world_id=world_id):
        locations.append({
            'id': str(loc.id),
            'name': loc.name,
            'description': loc.description,
            'integrity': loc.integrity,
            'color_saturation': loc.color_saturation,
            'clarity': loc.clarity,
            'witness_count': loc.witness_count,
        })
    
    return locations


@router.get("/world/{world_id}/objects", response=List[ObjectDetail])
def get_world_objects(request, world_id: str):
    """Get all objects in a specific world."""
    objects = []
    
    for obj in WorldObject.objects.filter(world_id=world_id):
        objects.append({
            'id': str(obj.id),
            'name': obj.name,
            'description': obj.description,
            'weight': obj.weight,
            'resource_type': obj.resource_type,
            'condition': obj.condition,
        })
    
    return objects


@router.get("/fixtures", response=List[FixtureInfo])
def list_fixtures(request):
    """List available fixture files."""
    fixtures = []
    base_path = Path(__file__).parent.parent / 'fixtures'
    
    # Scan all subdirectories
    for subdir in ['onlyworlds', 'examples', 'loaded']:
        dir_path = base_path / subdir
        if dir_path.exists():
            for file_path in dir_path.glob('*.json'):
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        element_count = len(data) if isinstance(data, list) else 1
                    
                    stat = file_path.stat()
                    fixtures.append({
                        'filename': file_path.name,
                        'path': str(file_path.relative_to(base_path)),
                        'size_kb': round(stat.st_size / 1024, 2),
                        'element_count': element_count,
                        'created_at': datetime.fromtimestamp(stat.st_mtime),
                    })
                except Exception as e:
                    print(f"Error reading fixture {file_path}: {e}")
    
    return fixtures


@router.post("/load-fixture", response=LoadFixtureResponse)
def load_fixture(request, data: LoadFixtureRequest):
    """Load a fixture file into the database."""
    base_path = Path(__file__).parent.parent / 'fixtures'
    fixture_path = base_path / data.fixture_path
    
    if not fixture_path.exists():
        return {
            'success': False,
            'message': f'Fixture file not found: {data.fixture_path}',
            'loaded_count': 0,
            'errors': ['File not found'],
        }
    
    errors = []
    loaded_count = 0
    
    try:
        with open(fixture_path, 'r') as f:
            fixtures = json.load(f)
        
        if data.overwrite:
            # Clear existing data
            World.objects.all().delete()
        
        # Load fixtures manually for better error handling
        for fixture in fixtures:
            try:
                model_path = fixture['model']
                app, model_name = model_path.split('.')
                
                if model_name == 'world':
                    World.objects.create(
                        id=fixture['pk'],
                        **fixture['fields']
                    )
                    loaded_count += 1
                
                elif model_name == 'character':
                    fields = fixture['fields'].copy()
                    world_id = fields.pop('world')
                    world = World.objects.get(id=world_id)
                    
                    Character.objects.create(
                        id=fixture['pk'],
                        world=world,
                        **fields
                    )
                    loaded_count += 1
                
                elif model_name == 'location':
                    fields = fixture['fields'].copy()
                    world_id = fields.pop('world')
                    world = World.objects.get(id=world_id)
                    
                    Location.objects.create(
                        id=fixture['pk'],
                        world=world,
                        **fields
                    )
                    loaded_count += 1
                
                elif model_name == 'object':
                    fields = fixture['fields'].copy()
                    world_id = fields.pop('world')
                    world = World.objects.get(id=world_id)
                    
                    WorldObject.objects.create(
                        id=fixture['pk'],
                        world=world,
                        **fields
                    )
                    loaded_count += 1
                
                elif model_name == 'treaty':
                    fields = fixture['fields'].copy()
                    world_id = fields.pop('world')
                    world = World.objects.get(id=world_id)
                    parties = fields.pop('parties', [])
                    
                    treaty = Treaty.objects.create(
                        id=fixture['pk'],
                        world=world,
                        **fields
                    )
                    
                    # Add parties if any
                    for party_id in parties:
                        try:
                            char = Character.objects.get(id=party_id)
                            treaty.parties.add(char)
                        except Character.DoesNotExist:
                            pass
                    
                    loaded_count += 1
                    
            except Exception as e:
                errors.append(f"Error loading {fixture.get('pk', 'unknown')}: {str(e)}")
        
        return {
            'success': loaded_count > 0,
            'message': f'Loaded {loaded_count} fixtures successfully',
            'loaded_count': loaded_count,
            'errors': errors,
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to load fixtures: {str(e)}',
            'loaded_count': 0,
            'errors': [str(e)],
        }


@router.post("/export-world/{world_id}")
def export_world(request, world_id: str):
    """Export a world as fixtures."""
    try:
        world = World.objects.get(id=world_id)
        fixtures = []
        
        # Export world
        fixtures.append({
            "model": "worlds.world",
            "pk": str(world.id),
            "fields": {
                "name": world.name,
                "description": world.description,
                "source_type": world.source_type,
                "source_reference": world.source_reference,
                "witness_config": world.witness_config,
                "resource_types": world.resource_types,
                "degradation_pattern": world.degradation_pattern,
                "hidden_truth": world.hidden_truth,
                "times_witnessed": world.times_witnessed,
            }
        })
        
        # Export characters
        for char in world.characters.all():
            fixtures.append({
                "model": "worlds.character",
                "pk": str(char.id),
                "fields": {
                    "world": str(world.id),
                    "name": char.name,
                    "description": char.description,
                    "role": char.role,
                    "has_agency": char.has_agency,
                    "power_level": char.power_level,
                    "is_witness_candidate": char.is_witness_candidate,
                    "alive": char.alive,
                    "memory_intact": char.memory_intact,
                    "known_truths": char.known_truths,
                    "spoken_lies": char.spoken_lies,
                    "personality_prompt": char.personality_prompt,
                    "speech_pattern": char.speech_pattern,
                }
            })
        
        # Export locations
        for loc in world.locations.all():
            fixtures.append({
                "model": "worlds.location",
                "pk": str(loc.id),
                "fields": {
                    "world": str(world.id),
                    "name": loc.name,
                    "description": loc.description,
                    "size_scale": loc.size_scale,
                    "integrity": loc.integrity,
                    "color_saturation": loc.color_saturation,
                    "clarity": loc.clarity,
                    "has_been_witnessed": loc.has_been_witnessed,
                    "witness_count": loc.witness_count,
                }
            })
        
        # Export objects
        for obj in world.world_objects.all():
            fixtures.append({
                "model": "worlds.object",
                "pk": str(obj.id),
                "fields": {
                    "world": str(world.id),
                    "name": obj.name,
                    "description": obj.description,
                    "size": obj.size,
                    "weight": obj.weight,
                    "resource_type": obj.resource_type,
                    "condition": obj.condition,
                    "hidden": obj.hidden,
                }
            })
        
        # Save to file
        filename = f"{world.name.lower().replace(' ', '_')}_export.json"
        export_path = Path(__file__).parent.parent / 'fixtures' / 'loaded' / filename
        export_path.parent.mkdir(exist_ok=True)
        
        with open(export_path, 'w') as f:
            json.dump(fixtures, f, indent=2, default=str)
        
        return {
            'success': True,
            'filename': filename,
            'element_count': len(fixtures),
        }
        
    except World.DoesNotExist:
        return {
            'success': False,
            'error': 'World not found',
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
        }


@router.delete("/clear-database")
def clear_database(request):
    """Clear all data from the database (dangerous!)."""
    try:
        # Delete in order of dependencies
        GameSession.objects.all().delete()
        Knowledge.objects.all().delete()
        Discovery.objects.all().delete()
        Treaty.objects.all().delete()
        WorldObject.objects.all().delete()
        Location.objects.all().delete()
        Character.objects.all().delete()
        World.objects.all().delete()
        
        return {
            'success': True,
            'message': 'Database cleared successfully',
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
        }