#!/usr/bin/env python3
"""
World Adapter Tool - Transform OnlyWorlds data into witness-able worlds
By Grimbert, keeper of degrading realities
"""

import json
import sys
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class WitnessConfig:
    """Configuration for the powerless observer"""
    name: str
    size: str  # thumb, scarab, mite, dust
    perspective: str  # ground_level, inside_walls, between_words
    starting_location: str
    initial_burden: float = 0.0

@dataclass
class ResourceTypes:
    """Three types of knowledge in every world"""
    ephemeral: str  # Decays over time (whispers, sins, screams)
    physical: str   # Permanent but dangerous (marks, scars, scalps)
    binding: str    # Changes reality (oaths, corruptions, manifestos)

@dataclass
class DegradationPattern:
    """How the world falls apart"""
    stages: List[str]  # e.g., ["color", "sound", "meaning", "memory", "hope"]
    current_stage: int = 0
    speed: float = 1.0  # Multiplier for degradation rate

class WorldAdapter:
    """Transform any OnlyWorlds world into a witness-able experience"""
    
    def __init__(self, world_data: Dict[str, Any]):
        self.world_data = world_data
        self.characters = []
        self.locations = []
        self.objects = []
        self.narratives = []
        self.relations = []
        
    def analyze_world(self) -> Dict[str, Any]:
        """Analyze world to find patterns"""
        print("🔍 Analyzing world structure...")
        
        # Extract elements by type
        self._extract_elements()
        
        # Find power structures
        power_structure = self._analyze_power()
        
        # Identify conflicts
        conflicts = self._find_conflicts()
        
        # Find the powerless
        witness_candidates = self._find_powerless()
        
        return {
            'power_structure': power_structure,
            'conflicts': conflicts,
            'witness_candidates': witness_candidates
        }
    
    def _extract_elements(self):
        """Extract all elements from world data"""
        for element in self.world_data.get('elements', []):
            element_type = element.get('element_type', '')
            
            if element_type == 'character':
                self.characters.append(element)
            elif element_type == 'location':
                self.locations.append(element)
            elif element_type == 'object':
                self.objects.append(element)
            elif element_type == 'narrative':
                self.narratives.append(element)
            elif element_type == 'relation':
                self.relations.append(element)
    
    def _analyze_power(self) -> Dict[str, List[str]]:
        """Identify who has power in this world"""
        power_structure = {
            'rulers': [],
            'enforcers': [],
            'influencers': [],
            'powerless': []
        }
        
        for char in self.characters:
            # Check reputation, traits, relationships
            reputation = char.get('reputation', 0)
            traits = char.get('traits', [])
            
            if reputation > 80 or 'ruler' in str(traits).lower():
                power_structure['rulers'].append(char['name'])
            elif reputation > 50 or 'warrior' in str(traits).lower():
                power_structure['enforcers'].append(char['name'])
            elif reputation > 20:
                power_structure['influencers'].append(char['name'])
            else:
                power_structure['powerless'].append(char['name'])
        
        return power_structure
    
    def _find_conflicts(self) -> List[Dict[str, Any]]:
        """Identify conflicts and tensions"""
        conflicts = []
        
        # Check relations for hostile connections
        for relation in self.relations:
            if any(word in relation.get('description', '').lower() 
                   for word in ['enemy', 'rival', 'conflict', 'war', 'hate']):
                conflicts.append({
                    'type': 'direct',
                    'parties': relation.get('characters', []),
                    'nature': relation.get('description', '')
                })
        
        # Check narratives for conflict events
        for narrative in self.narratives:
            if any(word in narrative.get('description', '').lower()
                   for word in ['battle', 'fight', 'struggle', 'conflict']):
                conflicts.append({
                    'type': 'narrative',
                    'story': narrative.get('name', ''),
                    'description': narrative.get('description', '')
                })
        
        return conflicts
    
    def _find_powerless(self) -> List[Dict[str, Any]]:
        """Identify potential witness characters"""
        candidates = []
        
        for char in self.characters:
            reputation = char.get('reputation', 0)
            traits = char.get('traits', [])
            
            # Look for observers, scribes, children, servants
            observer_keywords = ['scribe', 'child', 'servant', 'apprentice', 
                               'student', 'watcher', 'recorder', 'witness']
            
            is_observer = any(keyword in str(char).lower() 
                            for keyword in observer_keywords)
            
            if reputation < 30 or is_observer:
                candidates.append({
                    'name': char['name'],
                    'description': char.get('description', ''),
                    'traits': traits,
                    'why_suitable': self._explain_witness_suitability(char)
                })
        
        # If no obvious candidates, create one
        if not candidates:
            candidates.append(self._generate_witness())
        
        return candidates
    
    def _explain_witness_suitability(self, character: Dict) -> str:
        """Explain why this character makes a good witness"""
        reasons = []
        
        if character.get('reputation', 100) < 30:
            reasons.append("Low reputation means ignored by powerful")
        
        if 'child' in str(character).lower():
            reasons.append("Children see what adults ignore")
        
        if 'scribe' in str(character).lower():
            reasons.append("Natural observer and recorder")
        
        if not character.get('abilities'):
            reasons.append("No special powers means must rely on observation")
        
        return "; ".join(reasons) if reasons else "Overlooked by those in power"
    
    def _generate_witness(self) -> Dict[str, Any]:
        """Generate a witness if none exist"""
        return {
            'name': 'The Chronicler',
            'description': 'A forgotten scribe, shrunk by knowledge itself',
            'traits': ['observant', 'burdened', 'persistent'],
            'why_suitable': 'Created to observe what others cannot see'
        }
    
    def generate_game_config(self, analysis: Dict) -> Dict[str, Any]:
        """Generate complete game configuration"""
        print("⚙️ Generating game configuration...")
        
        # Select witness
        witness = self._configure_witness(analysis['witness_candidates'][0])
        
        # Define resources
        resources = self._define_resources(analysis['conflicts'])
        
        # Create degradation pattern
        degradation = self._create_degradation_pattern()
        
        # Identify treaties
        treaties = self._identify_treaties()
        
        # Find hidden truth
        hidden_truth = self._find_hidden_truth()
        
        return {
            'world_name': self.world_data.get('name', 'Unknown World'),
            'witness': witness.__dict__,
            'resources': resources.__dict__,
            'degradation': degradation.__dict__,
            'treaties': treaties,
            'hidden_truth': hidden_truth,
            'locations': [loc['name'] for loc in self.locations[:10]],
            'key_characters': [char['name'] for char in self.characters[:10]]
        }
    
    def _configure_witness(self, candidate: Dict) -> WitnessConfig:
        """Configure the witness from candidate"""
        # Determine size based on power level
        if 'child' in str(candidate).lower():
            size = 'thumb'
        elif 'insect' in str(candidate).lower():
            size = 'scarab'
        else:
            size = 'mite'
        
        # Determine perspective
        if 'scribe' in str(candidate).lower():
            perspective = 'between_words'
        elif size == 'mite':
            perspective = 'inside_walls'
        else:
            perspective = 'ground_level'
        
        # Find starting location
        starting = self.locations[0]['name'] if self.locations else 'threshold'
        
        return WitnessConfig(
            name=candidate['name'],
            size=size,
            perspective=perspective,
            starting_location=starting
        )
    
    def _define_resources(self, conflicts: List) -> ResourceTypes:
        """Define resource types based on world conflicts"""
        # Ephemeral - what fades
        if any('secret' in str(c).lower() for c in conflicts):
            ephemeral = 'secrets'
        elif any('memory' in str(c).lower() for c in conflicts):
            ephemeral = 'memories'
        else:
            ephemeral = 'whispers'
        
        # Physical - what marks
        if any('scar' in str(c).lower() for c in conflicts):
            physical = 'scars'
        elif any('blood' in str(c).lower() for c in conflicts):
            physical = 'bloodstains'
        else:
            physical = 'marks'
        
        # Binding - what controls
        if any('oath' in str(c).lower() for c in conflicts):
            binding = 'oaths'
        elif any('curse' in str(c).lower() for c in conflicts):
            binding = 'curses'
        else:
            binding = 'promises'
        
        return ResourceTypes(ephemeral, physical, binding)
    
    def _create_degradation_pattern(self) -> DegradationPattern:
        """Create degradation stages for this world"""
        # Default pattern
        stages = ["color", "sound", "meaning", "memory", "hope"]
        
        # Adjust based on world theme
        if any('desert' in str(self.locations).lower() for loc in self.locations):
            stages = ["moisture", "form", "identity", "purpose", "sand"]
        elif any('war' in str(self.narratives).lower() for nar in self.narratives):
            stages = ["peace", "order", "humanity", "meaning", "silence"]
        
        return DegradationPattern(stages=stages)
    
    def _identify_treaties(self) -> List[str]:
        """Find the hidden agreements maintaining order"""
        treaties = []
        
        # Look for relations that suggest agreements
        for relation in self.relations:
            if any(word in relation.get('description', '').lower()
                   for word in ['agreement', 'treaty', 'pact', 'accord', 'truce']):
                treaties.append(relation.get('name', 'Unknown Treaty'))
        
        # Generate some if none found
        if not treaties:
            treaties = [
                "The Silence Accord - No one speaks of what happened",
                "The Border Treaty - Territories remain separate",
                "The Observation Pact - Watchers must not interfere"
            ]
        
        return treaties
    
    def _find_hidden_truth(self) -> str:
        """Determine the truth everyone knows but won't acknowledge"""
        # Check narratives for dark secrets
        for narrative in self.narratives:
            if any(word in narrative.get('description', '').lower()
                   for word in ['secret', 'hidden', 'truth', 'real', 'actually']):
                return f"The truth about {narrative['name']}"
        
        # Generate based on world analysis
        if len(self.characters) > 50:
            return "Not everyone here is real"
        elif len(self.conflicts) > 10:
            return "The conflicts are orchestrated"
        else:
            return "This world is already ending"

def main():
    """Main entry point for world adapter"""
    
    print("🌑 World Adapter - The Endless Nights Engine")
    print("Transform any world into a witness-able experience")
    print("-" * 50)
    
    if len(sys.argv) < 2:
        print("Usage: python world-adapter.py <world_file.json>")
        sys.exit(1)
    
    world_file = Path(sys.argv[1])
    
    if not world_file.exists():
        print(f"❌ Error: World file '{world_file}' not found")
        sys.exit(1)
    
    # Load world data
    with open(world_file, 'r') as f:
        world_data = json.load(f)
    
    print(f"📖 Loading world: {world_data.get('name', 'Unknown')}")
    print(f"📊 Found {len(world_data.get('elements', []))} elements")
    
    # Create adapter
    adapter = WorldAdapter(world_data)
    
    # Analyze world
    analysis = adapter.analyze_world()
    
    print("\n📋 Analysis Results:")
    print(f"  Power holders: {len(analysis['power_structure']['rulers'])}")
    print(f"  Conflicts: {len(analysis['conflicts'])}")
    print(f"  Witness candidates: {len(analysis['witness_candidates'])}")
    
    # Generate game configuration
    config = adapter.generate_game_config(analysis)
    
    print("\n✨ Game Configuration Generated:")
    print(f"  Witness: {config['witness']['name']} ({config['witness']['size']})")
    print(f"  Resources: {config['resources']}")
    print(f"  Degradation: {' → '.join(config['degradation']['stages'])}")
    print(f"  Hidden Truth: {config['hidden_truth']}")
    
    # Save configuration
    output_file = world_file.stem + '_game_config.json'
    with open(output_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n💾 Configuration saved to: {output_file}")
    print("\n🌙 The endless night begins...")

if __name__ == "__main__":
    main()