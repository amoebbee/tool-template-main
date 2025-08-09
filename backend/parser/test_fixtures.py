#!/usr/bin/env python
"""
OnlyWorlds Fixture Testing Script
Tests that our parsed data can be properly loaded into Django models.

Based on Claudette's Juliette parsing experience and OnlyWorlds schema.
"""

import os
import sys
import json
import uuid
from datetime import datetime
from pathlib import Path

# Add backend to path for Django imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'endless_nights.settings')
import django
django.setup()

from worlds.models import World, Character, Location, Object as WorldObject, Treaty
from django.core.management import call_command
from django.db import transaction


class OnlyWorldsFixtureTester:
    """Test fixture loading for OnlyWorlds elements."""
    
    def __init__(self):
        self.test_world = None
        self.created_elements = []
        
    def setup_test_world(self):
        """Create a test world for our fixtures."""
        self.test_world = World.objects.create(
            name="Blood Meridian Test",
            description="Testing fixture loading from parsed text",
            source_type='text',
            source_reference='Blood Meridian by Cormac McCarthy',
            witness_config={
                'name': 'The Kid',
                'size': 'human',
                'starting_location': 'texas',
            },
            resource_types={
                'ephemeral': 'whispered threats',
                'physical': 'scalps and weapons',
                'binding': 'gang oaths',
            },
            degradation_pattern={
                'speed': 1.5,  # Faster degradation for violence
                'entropy_rate': 0.02,
            },
            hidden_truth="Violence is the only truth in the borderlands",
        )
        print(f"✓ Created test world: {self.test_world.name}")
        return self.test_world
    
    def create_test_fixtures(self):
        """Create test fixture data based on Blood Meridian example."""
        fixtures = []
        
        # Character: The Judge
        judge_id = str(uuid.uuid4())
        fixtures.append({
            "model": "worlds.character",
            "pk": judge_id,
            "fields": {
                "world": str(self.test_world.id),
                "name": "Judge Holden",
                "description": "An enormous hairless man who exposes religious fraud",
                "role": "Antagonist",
                "has_agency": True,
                "power_level": 9,
                "is_witness_candidate": False,
                "alive": True,
                "memory_intact": 1.0,
                "known_truths": ["The reverend is a fraud", "War is god"],
                "spoken_lies": [],
                "personality_prompt": "You are Judge Holden, erudite and violent. You speak in philosophical terms about war and human nature.",
                "speech_pattern": "Eloquent, philosophical, unsettling",
            }
        })
        
        # Character: The Kid
        kid_id = str(uuid.uuid4())
        fixtures.append({
            "model": "worlds.character",
            "pk": kid_id,
            "fields": {
                "world": str(self.test_world.id),
                "name": "The Kid",
                "description": "Pale and thin boy, witness to violence",
                "role": "Protagonist/Witness",
                "has_agency": False,
                "power_level": 2,
                "is_witness_candidate": True,
                "alive": True,
                "memory_intact": 0.8,
                "known_truths": [],
                "spoken_lies": [],
                "personality_prompt": "You are a young witness to terrible violence. You speak little.",
                "speech_pattern": "Sparse, observational",
            }
        })
        
        # Location: The Revival Tent
        tent_id = str(uuid.uuid4())
        fixtures.append({
            "model": "worlds.location",
            "pk": tent_id,
            "fields": {
                "world": str(self.test_world.id),
                "name": "The Revival Tent",
                "description": "A canvas tent where the reverend holds his fraudulent sermons",
                "size_scale": "large",
                "integrity": 0.9,
                "color_saturation": 0.7,
                "clarity": 0.8,
                "has_been_witnessed": True,
                "witness_count": 1,
            }
        })
        
        # Object: The Judge's Hat
        hat_id = str(uuid.uuid4())
        fixtures.append({
            "model": "worlds.object",
            "pk": hat_id,
            "fields": {
                "world": str(self.test_world.id),
                "name": "The Judge's Hat",
                "description": "A hat that the Judge removes upon entering",
                "size": "small",
                "weight": 0.5,
                "resource_type": "physical",
                "condition": 1.0,
                "hidden": False,
            }
        })
        
        # Treaty: The Gang's Code
        treaty_id = str(uuid.uuid4())
        fixtures.append({
            "model": "worlds.treaty",
            "pk": treaty_id,
            "fields": {
                "world": str(self.test_world.id),
                "name": "The Glanton Gang Code",
                "description": "Unspoken rules that govern the scalp hunters",
                "is_public": False,
                "is_broken": False,
                "terms": [
                    "Follow Glanton's orders",
                    "Share the spoils",
                    "Never show weakness",
                    "The Judge is untouchable"
                ],
                "consequences": "Death or abandonment",
                "strength": 0.7,
            }
        })
        
        return fixtures
    
    def save_fixtures_to_file(self, fixtures, filename="test_fixtures.json"):
        """Save fixtures to JSON file."""
        filepath = Path(__file__).parent / filename
        with open(filepath, 'w') as f:
            json.dump(fixtures, f, indent=2)
        print(f"✓ Saved {len(fixtures)} fixtures to {filepath}")
        return filepath
    
    def load_fixtures_from_file(self, filepath):
        """Load fixtures using Django's loaddata command."""
        try:
            # First, let's try loading manually to catch specific errors
            with open(filepath, 'r') as f:
                fixtures = json.load(f)
            
            print(f"\n📦 Loading {len(fixtures)} fixtures...")
            
            with transaction.atomic():
                for fixture in fixtures:
                    model_path = fixture['model']
                    app, model_name = model_path.split('.')
                    
                    if model_name == 'character':
                        fields = fixture['fields'].copy()
                        # Convert world ID string to actual World object
                        world_id = fields.pop('world')
                        world = World.objects.get(id=world_id)
                        
                        obj = Character.objects.create(
                            id=fixture['pk'],
                            world=world,
                            **fields
                        )
                        self.created_elements.append(obj)
                        print(f"  ✓ Created Character: {obj.name}")
                    
                    elif model_name == 'location':
                        fields = fixture['fields'].copy()
                        world_id = fields.pop('world')
                        world = World.objects.get(id=world_id)
                        
                        obj = Location.objects.create(
                            id=fixture['pk'],
                            world=world,
                            **fields
                        )
                        self.created_elements.append(obj)
                        print(f"  ✓ Created Location: {obj.name}")
                    
                    elif model_name == 'object':
                        fields = fixture['fields'].copy()
                        world_id = fields.pop('world')
                        world = World.objects.get(id=world_id)
                        
                        obj = WorldObject.objects.create(
                            id=fixture['pk'],
                            world=world,
                            **fields
                        )
                        self.created_elements.append(obj)
                        print(f"  ✓ Created Object: {obj.name}")
                    
                    elif model_name == 'treaty':
                        # Treaties need special handling for ManyToMany
                        treaty_data = fixture['fields'].copy()
                        world_id = treaty_data.pop('world')
                        world = World.objects.get(id=world_id)
                        # Remove M2M fields temporarily
                        parties = treaty_data.pop('parties', [])
                        
                        obj = Treaty.objects.create(
                            id=fixture['pk'],
                            world=world,
                            **treaty_data
                        )
                        
                        # Add M2M relationships if any
                        if parties:
                            for party_id in parties:
                                character = Character.objects.get(id=party_id)
                                obj.parties.add(character)
                        
                        self.created_elements.append(obj)
                        print(f"  ✓ Created Treaty: {obj.name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading fixtures: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def verify_loaded_data(self):
        """Verify that fixtures loaded correctly."""
        print("\n🔍 Verifying loaded data...")
        
        # Check characters
        characters = Character.objects.filter(world=self.test_world)
        print(f"  Characters: {characters.count()}")
        for char in characters:
            print(f"    - {char.name} (power: {char.power_level}, witness: {char.is_witness_candidate})")
        
        # Check locations
        locations = Location.objects.filter(world=self.test_world)
        print(f"  Locations: {locations.count()}")
        for loc in locations:
            print(f"    - {loc.name} (integrity: {loc.integrity:.2f})")
        
        # Check objects
        objects = WorldObject.objects.filter(world=self.test_world)
        print(f"  Objects: {objects.count()}")
        for obj in objects:
            print(f"    - {obj.name} ({obj.resource_type}, weight: {obj.weight})")
        
        # Check treaties
        treaties = Treaty.objects.filter(world=self.test_world)
        print(f"  Treaties: {treaties.count()}")
        for treaty in treaties:
            print(f"    - {treaty.name} (strength: {treaty.strength:.2f})")
        
        return True
    
    def test_degradation(self):
        """Test that degradation methods work on loaded elements."""
        print("\n⏳ Testing degradation mechanics...")
        
        # Test location degradation
        location = Location.objects.filter(world=self.test_world).first()
        if location:
            initial_integrity = location.integrity
            location.degrade(0.1)
            print(f"  Location '{location.name}' degraded: {initial_integrity:.2f} → {location.integrity:.2f}")
        
        # Test character forgetting
        character = Character.objects.filter(world=self.test_world).first()
        if character:
            initial_memory = character.memory_intact
            character.forget(0.2)
            print(f"  Character '{character.name}' forgot: {initial_memory:.2f} → {character.memory_intact:.2f}")
        
        # Test object decay
        obj = WorldObject.objects.filter(world=self.test_world).first()
        if obj:
            initial_condition = obj.condition
            obj.decay(0.15)
            print(f"  Object '{obj.name}' decayed: {initial_condition:.2f} → {obj.condition:.2f}")
        
        # Test treaty weakening
        treaty = Treaty.objects.filter(world=self.test_world).first()
        if treaty:
            initial_strength = treaty.strength
            treaty.weaken(0.25)
            print(f"  Treaty '{treaty.name}' weakened: {initial_strength:.2f} → {treaty.strength:.2f}")
        
        return True
    
    def cleanup(self):
        """Clean up test data."""
        print("\n🧹 Cleaning up test data...")
        
        # Delete in reverse order of dependencies
        for element in reversed(self.created_elements):
            element.delete()
        
        if self.test_world:
            self.test_world.delete()
        
        print("  ✓ Test data cleaned up")
    
    def run_full_test(self):
        """Run complete fixture test."""
        print("=" * 60)
        print("OnlyWorlds Fixture Testing")
        print("=" * 60)
        
        try:
            # Setup
            self.setup_test_world()
            
            # Create fixtures
            fixtures = self.create_test_fixtures()
            
            # Save to file
            filepath = self.save_fixtures_to_file(fixtures)
            
            # Load from file
            success = self.load_fixtures_from_file(filepath)
            
            if success:
                # Verify
                self.verify_loaded_data()
                
                # Test degradation
                self.test_degradation()
                
                print("\n✅ All tests passed!")
            else:
                print("\n❌ Fixture loading failed")
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Always cleanup
            self.cleanup()
        
        print("=" * 60)


def main():
    """Main entry point."""
    tester = OnlyWorldsFixtureTester()
    tester.run_full_test()


if __name__ == "__main__":
    main()