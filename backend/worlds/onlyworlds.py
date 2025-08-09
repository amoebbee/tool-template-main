"""
OnlyWorlds integration for importing and exporting worlds.
"""

import requests
from typing import Dict, List, Optional
from .models import World, Location, Character, Object, Treaty
import json


class OnlyWorldsAdapter:
    """Adapter for OnlyWorlds API integration."""
    
    def __init__(self, api_key: str, pin: str):
        self.api_key = api_key
        self.pin = pin
        self.base_url = "https://api.onlyworlds.com"  # Placeholder
        
    def import_world(self, world_id: str) -> World:
        """Import a complete world from OnlyWorlds."""
        # Fetch world data
        world_data = self._fetch_world_data(world_id)
        
        # Create base world
        world = World.objects.create(
            name=world_data.get('name', 'Unknown World'),
            description=world_data.get('description', ''),
            source_type='onlyworlds',
            source_reference=world_id,
            onlyworlds_api_key=self.api_key,
            onlyworlds_pin=self.pin,
        )
        
        # Import elements
        elements = self._fetch_elements(world_id)
        
        # Process each element type
        for element in elements:
            self._process_element(world, element)
        
        # Analyze for witness
        self._identify_witness(world)
        
        # Define resources based on world content
        self._define_resources(world)
        
        # Set degradation pattern
        self._set_degradation_pattern(world)
        
        return world
    
    def _fetch_world_data(self, world_id: str) -> Dict:
        """Fetch world metadata from OnlyWorlds."""
        # Placeholder for actual API call
        return {
            "name": "Imported World",
            "description": "A world imported from OnlyWorlds",
        }
    
    def _fetch_elements(self, world_id: str) -> List[Dict]:
        """Fetch all elements from a world."""
        # Placeholder for actual API call
        return []
    
    def _process_element(self, world: World, element: Dict):
        """Process a single OnlyWorlds element."""
        element_type = element.get('type', 'unknown')
        
        if element_type == 'character':
            self._create_character(world, element)
        elif element_type == 'location':
            self._create_location(world, element)
        elif element_type == 'object' or element_type == 'item':
            self._create_object(world, element)
        elif element_type == 'agreement' or element_type == 'treaty':
            self._create_treaty(world, element)
    
    def _create_character(self, world: World, data: Dict) -> Character:
        """Create a character from OnlyWorlds data."""
        # Analyze power level from description
        power_level = self._analyze_power_level(data)
        
        character = Character.objects.create(
            world=world,
            name=data.get('name', 'Unknown'),
            description=data.get('description', ''),
            role=data.get('role', ''),
            has_agency=power_level > 2,
            power_level=power_level,
            is_witness_candidate=power_level <= 3,
        )
        
        return character
    
    def _create_location(self, world: World, data: Dict) -> Location:
        """Create a location from OnlyWorlds data."""
        location = Location.objects.create(
            world=world,
            name=data.get('name', 'Unknown Place'),
            description=data.get('description', ''),
            size_scale=self._determine_scale(data),
        )
        
        return location
    
    def _create_object(self, world: World, data: Dict) -> Object:
        """Create an object from OnlyWorlds data."""
        obj = Object.objects.create(
            world=world,
            name=data.get('name', 'Unknown Object'),
            description=data.get('description', ''),
            size=self._determine_object_size(data),
            resource_type=self._determine_resource_type(data),
        )
        
        return obj
    
    def _create_treaty(self, world: World, data: Dict) -> Treaty:
        """Create a treaty from OnlyWorlds data."""
        treaty = Treaty.objects.create(
            world=world,
            name=data.get('name', 'Unknown Agreement'),
            description=data.get('description', ''),
            terms=data.get('terms', []),
        )
        
        return treaty
    
    def _analyze_power_level(self, data: Dict) -> int:
        """Analyze a character's power level from their description."""
        description = data.get('description', '').lower()
        
        # Keywords indicating power levels
        if any(word in description for word in ['ruler', 'king', 'queen', 'lord', 'master']):
            return 8
        elif any(word in description for word in ['knight', 'warrior', 'captain', 'leader']):
            return 6
        elif any(word in description for word in ['merchant', 'craftsman', 'citizen']):
            return 4
        elif any(word in description for word in ['servant', 'slave', 'prisoner']):
            return 2
        elif any(word in description for word in ['child', 'orphan', 'beggar']):
            return 1
        
        return 5  # Default middle power
    
    def _determine_scale(self, data: Dict) -> str:
        """Determine the scale of a location."""
        description = data.get('description', '').lower()
        
        if any(word in description for word in ['vast', 'endless', 'infinite']):
            return 'vast'
        elif any(word in description for word in ['large', 'grand', 'massive']):
            return 'large'
        elif any(word in description for word in ['small', 'tiny', 'cramped']):
            return 'small'
        elif any(word in description for word in ['microscopic', 'minuscule']):
            return 'microscopic'
        
        return 'human'
    
    def _determine_object_size(self, data: Dict) -> str:
        """Determine object size from description."""
        description = data.get('description', '').lower()
        
        if any(word in description for word in ['tiny', 'small', 'miniature']):
            return 'tiny'
        elif any(word in description for word in ['large', 'huge', 'massive']):
            return 'large'
        elif any(word in description for word in ['medium', 'regular']):
            return 'medium'
        
        return 'small'
    
    def _determine_resource_type(self, data: Dict) -> str:
        """Determine what type of resource an object represents."""
        description = data.get('description', '').lower()
        name = data.get('name', '').lower()
        
        # Ephemeral: rumors, whispers, secrets
        if any(word in description + name for word in ['whisper', 'rumor', 'secret', 'tale']):
            return 'ephemeral'
        
        # Binding: contracts, oaths, promises
        elif any(word in description + name for word in ['oath', 'contract', 'promise', 'vow']):
            return 'binding'
        
        # Physical: everything else
        return 'physical'
    
    def _identify_witness(self, world: World):
        """Identify the best witness candidate."""
        # Find the smallest, most powerless character
        candidates = Character.objects.filter(
            world=world,
            power_level__lte=3,
            alive=True,
        ).order_by('power_level')
        
        if candidates.exists():
            witness = candidates.first()
            world.witness_config = {
                'name': witness.name,
                'size': 'thumb',
                'starting_location': 'ground',
                'character_id': str(witness.id),
            }
        else:
            # Create a default witness
            world.witness_config = {
                'name': 'The Small Observer',
                'size': 'thumb',
                'starting_location': 'shadows',
            }
        
        world.save()
    
    def _define_resources(self, world: World):
        """Define resource types based on world content."""
        world.resource_types = {
            'ephemeral': 'whispers',
            'physical': 'marks',
            'binding': 'oaths',
        }
        world.save()
    
    def _set_degradation_pattern(self, world: World):
        """Set the degradation pattern for the world."""
        world.degradation_pattern = {
            'stages': ['color', 'sound', 'meaning', 'memory', 'hope'],
            'speed': 1.0,
            'entropy_rate': 0.01,
        }
        world.save()
    
    def export_to_onlyworlds(self, session_id: str) -> Dict:
        """Export a game session's discoveries back to OnlyWorlds."""
        from game.models import GameSession
        
        session = GameSession.objects.get(id=session_id)
        
        # Create narrative element
        narrative = {
            'element_type': 'narrative',
            'name': f"Chronicle of {session.witness_name}",
            'description': f"Witnessed through {session.night_count} endless nights",
            'content': self._compile_discoveries(session),
            'metadata': {
                'witness': session.witness_name,
                'nights': session.night_count,
                'weight_carried': session.total_weight,
                'world_entropy': session.world_entropy,
            }
        }
        
        # Placeholder for actual API call
        return narrative
    
    def _compile_discoveries(self, session) -> str:
        """Compile all discoveries into a narrative."""
        discoveries = []
        
        for knowledge in session.knowledge.all():
            discoveries.append(f"Night {knowledge.night_discovered}: {knowledge.content}")
        
        for discovery in session.discoveries.all():
            discoveries.append(f"Night {discovery.night_discovered}: {discovery.description}")
        
        return "\n".join(discoveries)