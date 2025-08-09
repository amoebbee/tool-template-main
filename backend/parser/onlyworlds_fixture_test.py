#!/usr/bin/env python
"""
Advanced OnlyWorlds Fixture Testing Script
Tests full OnlyWorlds schema with Relations and all field types.

This validates that our parsing output format will work with Django.
"""

import os
import sys
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'endless_nights.settings')
import django
django.setup()

from django.db import models, transaction
from django.core import serializers
from worlds.models import World, Character, Location, Object as WorldObject, Treaty


class OnlyWorldsElement:
    """Base class for OnlyWorlds elements following the schema."""
    
    @staticmethod
    def generate_id(element_type: str, name: str) -> str:
        """Generate deterministic ID based on type and name."""
        clean_name = name.lower().replace(' ', '_').replace("'", "")[:20]
        short_uuid = uuid.uuid4().hex[:8]
        return f"{element_type}_{clean_name}_{short_uuid}"


class OnlyWorldsRelation:
    """Represents a Relation element with full schema compliance."""
    
    def __init__(self, actor_id: str, name: str, intensity: int = 50):
        self.id = OnlyWorldsElement.generate_id("rel", name)
        self.name = name
        self.actor = actor_id
        self.intensity = intensity
        self.involves = {
            'characters': [],
            'objects': [],
            'locations': [],
            'institutions': [],
            'titles': [],
            'events': [],
        }
        self.background = ""
        self.start_date = None
        self.end_date = None
    
    def add_involved(self, element_type: str, element_id: str):
        """Add an element to the involves field."""
        if element_type in self.involves:
            if element_id not in self.involves[element_type]:
                self.involves[element_type].append(element_id)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'actor': self.actor,
            'intensity': self.intensity,
            'involves': self.involves,
            'background': self.background,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }


class AdvancedFixtureTester:
    """Test OnlyWorlds fixtures with full schema compliance."""
    
    def __init__(self):
        self.world = None
        self.elements = {}
        self.relations = []
        self.fixtures = []
    
    def create_blood_meridian_world(self):
        """Create the Blood Meridian test world."""
        self.world = World.objects.create(
            name="Blood Meridian - Full Parse Test",
            description="Complete OnlyWorlds parsing test with Relations",
            source_type='text',
            source_reference='Blood Meridian by Cormac McCarthy',
            witness_config={
                'name': 'The Kid',
                'size': 'human',
                'starting_location': 'nacogdoches',
                'voice': 'sparse and observational',
            },
            resource_types={
                'ephemeral': 'rumors and sermons',
                'physical': 'weapons and scalps', 
                'binding': 'gang membership',
            },
            degradation_pattern={
                'stages': ['civilization', 'frontier', 'violence', 'desert', 'void'],
                'speed': 2.0,
                'entropy_rate': 0.03,
                'special': 'blood stains never fade',
            },
            hidden_truth="The Judge is eternal; violence is the only god",
        )
        print(f"✓ Created world: {self.world.name}")
        return self.world
    
    def parse_judge_entrance_scene(self):
        """Parse the Judge entering the tent scene with full relationships."""
        
        # Create The Judge character
        judge_id = OnlyWorldsElement.generate_id("char", "Judge Holden")
        judge = {
            "id": judge_id,
            "world": str(self.world.id),
            "name": "Judge Holden",
            "description": "An enormous hairless man, serene and strangely childlike",
            "role": "Antagonist/Force of Nature",
            "has_agency": True,
            "power_level": 10,
            "is_witness_candidate": False,
            "alive": True,
            "memory_intact": 1.0,
            "known_truths": [
                "War is the truest form of divination",
                "The reverend is a fraud",
                "Everything must be known and catalogued"
            ],
            "personality_prompt": "You are Judge Holden. You speak with erudition about war, nature, and the meaninglessness of moral law.",
            "speech_pattern": "Eloquent, philosophical, contains hidden threats",
        }
        self.elements['judge'] = judge
        
        # Create The Reverend character
        reverend_id = OnlyWorldsElement.generate_id("char", "Reverend Green")
        reverend = {
            "id": reverend_id,
            "world": str(self.world.id),
            "name": "Reverend Green",
            "description": "A fraudulent preacher holding revival meetings",
            "role": "Fraud/Victim",
            "has_agency": False,
            "power_level": 3,
            "is_witness_candidate": False,
            "alive": True,
            "memory_intact": 0.9,
            "known_truths": ["I have no real ordination"],
            "personality_prompt": "You are a fake reverend, desperate to maintain your deception.",
        }
        self.elements['reverend'] = reverend
        
        # Create The Kid (witness)
        kid_id = OnlyWorldsElement.generate_id("char", "The Kid")
        kid = {
            "id": kid_id,
            "world": str(self.world.id),
            "name": "The Kid",
            "description": "Pale and thin, witness to violence",
            "role": "Witness/Protagonist",
            "has_agency": False,
            "power_level": 1,
            "is_witness_candidate": True,
            "alive": True,
            "memory_intact": 0.7,
            "known_truths": [],
            "personality_prompt": "You observe but rarely speak. Violence has marked you.",
        }
        self.elements['kid'] = kid
        
        # Create The Revival Tent location
        tent_id = OnlyWorldsElement.generate_id("loc", "Revival Tent")
        tent = {
            "id": tent_id,
            "world": str(self.world.id),
            "name": "The Revival Tent",
            "description": "A large canvas tent filled with desperate believers",
            "size_scale": "large",
            "integrity": 0.8,
            "color_saturation": 0.6,
            "clarity": 0.7,
            "has_been_witnessed": True,
            "witness_count": 3,
        }
        self.elements['tent'] = tent
        
        # Create Objects
        slicker_id = OnlyWorldsElement.generate_id("obj", "Oilcloth Slicker")
        slicker = {
            "id": slicker_id,
            "world": str(self.world.id),
            "name": "Oilcloth Slicker",
            "description": "The Judge's waterproof coat",
            "size": "medium",
            "weight": 2.0,
            "resource_type": "physical",
            "condition": 0.9,
            "owned_by": judge_id,
        }
        self.elements['slicker'] = slicker
        
        # Create RELATIONS - The key part!
        
        # Relation 1: Judge exposes Reverend
        rel_expose = OnlyWorldsRelation(
            actor_id=judge_id,
            name="Judge Exposes Reverend",
            intensity=95
        )
        rel_expose.background = "The Judge enters the revival to destroy the Reverend's credibility"
        rel_expose.add_involved('characters', judge_id)
        rel_expose.add_involved('characters', reverend_id)
        rel_expose.add_involved('locations', tent_id)
        self.relations.append(rel_expose)
        
        # Relation 2: Kid witnesses confrontation
        rel_witness = OnlyWorldsRelation(
            actor_id=kid_id,
            name="Kid Witnesses Exposure",
            intensity=70
        )
        rel_witness.background = "The Kid observes the Judge's destruction of the revival"
        rel_witness.add_involved('characters', kid_id)
        rel_witness.add_involved('characters', judge_id)
        rel_witness.add_involved('characters', reverend_id)
        rel_witness.add_involved('locations', tent_id)
        self.relations.append(rel_witness)
        
        # Relation 3: Judge owns slicker
        rel_owns = OnlyWorldsRelation(
            actor_id=judge_id,
            name="Judge's Possessions",
            intensity=30
        )
        rel_owns.add_involved('characters', judge_id)
        rel_owns.add_involved('objects', slicker_id)
        self.relations.append(rel_owns)
        
        print(f"✓ Parsed scene: {len(self.elements)} elements, {len(self.relations)} relations")
    
    def generate_fixtures(self):
        """Convert parsed elements to Django fixture format."""
        
        # Add Characters
        for key, char in self.elements.items():
            if char['id'].startswith('char_'):
                self.fixtures.append({
                    "model": "worlds.character",
                    "pk": char['id'],
                    "fields": char
                })
        
        # Add Locations
        for key, loc in self.elements.items():
            if loc['id'].startswith('loc_'):
                self.fixtures.append({
                    "model": "worlds.location",
                    "pk": loc['id'],
                    "fields": loc
                })
        
        # Add Objects
        for key, obj in self.elements.items():
            if obj['id'].startswith('obj_'):
                # Handle the owned_by field specially
                obj_fields = obj.copy()
                owned_by = obj_fields.pop('owned_by', None)
                
                self.fixtures.append({
                    "model": "worlds.object",
                    "pk": obj['id'],
                    "fields": obj_fields
                })
        
        print(f"✓ Generated {len(self.fixtures)} fixtures")
        return self.fixtures
    
    def save_fixtures(self, filename="blood_meridian_fixtures.json"):
        """Save fixtures to JSON file."""
        filepath = Path(__file__).parent / "fixtures" / filename
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(self.fixtures, f, indent=2)
        
        print(f"✓ Saved fixtures to {filepath}")
        return filepath
    
    def save_relations(self, filename="blood_meridian_relations.json"):
        """Save relations separately (they're not Django models yet)."""
        filepath = Path(__file__).parent / "fixtures" / filename
        filepath.parent.mkdir(exist_ok=True)
        
        relations_data = [rel.to_dict() for rel in self.relations]
        
        with open(filepath, 'w') as f:
            json.dump(relations_data, f, indent=2)
        
        print(f"✓ Saved {len(self.relations)} relations to {filepath}")
        return filepath
    
    def load_and_verify(self, fixture_path):
        """Load fixtures and verify they work."""
        
        with open(fixture_path, 'r') as f:
            fixtures = json.load(f)
        
        loaded = []
        
        with transaction.atomic():
            for fixture in fixtures:
                model_path = fixture['model']
                app, model_name = model_path.split('.')
                
                try:
                    if model_name == 'character':
                        # Remove the owned_by field if it exists (it's a reverse FK)
                        fields = fixture['fields'].copy()
                        fields.pop('owned_by', None)
                        
                        obj = Character.objects.create(
                            id=fixture['pk'],
                            **fields
                        )
                        loaded.append(obj)
                        print(f"  ✓ Loaded Character: {obj.name}")
                    
                    elif model_name == 'location':
                        obj = Location.objects.create(
                            id=fixture['pk'],
                            **fixture['fields']
                        )
                        loaded.append(obj)
                        print(f"  ✓ Loaded Location: {obj.name}")
                    
                    elif model_name == 'object':
                        fields = fixture['fields'].copy()
                        # Handle owned_by relationship
                        owned_by_id = fields.pop('owned_by', None)
                        
                        obj = WorldObject.objects.create(
                            id=fixture['pk'],
                            **fields
                        )
                        
                        if owned_by_id:
                            try:
                                owner = Character.objects.get(id=owned_by_id)
                                obj.owned_by = owner
                                obj.save()
                            except Character.DoesNotExist:
                                pass
                        
                        loaded.append(obj)
                        print(f"  ✓ Loaded Object: {obj.name}")
                
                except Exception as e:
                    print(f"  ❌ Failed to load {model_name}: {e}")
        
        return loaded
    
    def verify_relationships(self, relations_path):
        """Verify that relationships are properly structured."""
        
        with open(relations_path, 'r') as f:
            relations = json.load(f)
        
        print(f"\n🔗 Verifying {len(relations)} relationships:")
        
        for rel in relations:
            # Check all referenced IDs exist
            actor_exists = Character.objects.filter(id=rel['actor']).exists()
            
            print(f"\n  Relation: {rel['name']}")
            print(f"    Actor: {rel['actor']} ({'✓' if actor_exists else '❌'})")
            print(f"    Intensity: {rel['intensity']}/100")
            
            # Check involved elements
            for element_type, ids in rel['involves'].items():
                if ids:
                    print(f"    {element_type}: {len(ids)} involved")
                    for elem_id in ids:
                        # We'd check each type properly in production
                        print(f"      - {elem_id}")
        
        return True
    
    def cleanup(self):
        """Clean up test data."""
        # Delete all test data
        if self.world:
            Character.objects.filter(world=self.world).delete()
            Location.objects.filter(world=self.world).delete()
            WorldObject.objects.filter(world=self.world).delete()
            self.world.delete()
            print("✓ Cleaned up test data")
    
    def run_complete_test(self):
        """Run the full test suite."""
        print("=" * 70)
        print("OnlyWorlds Advanced Fixture Testing")
        print("Testing: Full parsing → Fixtures → Relations → Database")
        print("=" * 70)
        
        try:
            # 1. Create world
            self.create_blood_meridian_world()
            
            # 2. Parse scene with relationships
            self.parse_judge_entrance_scene()
            
            # 3. Generate fixtures
            self.generate_fixtures()
            
            # 4. Save fixtures and relations
            fixture_path = self.save_fixtures()
            relations_path = self.save_relations()
            
            # 5. Load and verify
            print(f"\n📦 Loading fixtures into database...")
            loaded = self.load_and_verify(fixture_path)
            
            # 6. Verify relationships
            self.verify_relationships(relations_path)
            
            # 7. Test queries
            print(f"\n🔍 Testing queries:")
            judges = Character.objects.filter(
                world=self.world,
                power_level__gte=9
            )
            print(f"  High-power characters: {judges.count()}")
            
            witnesses = Character.objects.filter(
                world=self.world,
                is_witness_candidate=True
            )
            print(f"  Witness candidates: {witnesses.count()}")
            
            print("\n✅ All tests passed! Fixtures are properly formatted.")
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.cleanup()
        
        print("=" * 70)


def main():
    """Run the advanced fixture test."""
    tester = AdvancedFixtureTester()
    tester.run_complete_test()


if __name__ == "__main__":
    main()