# OnlyWorlds Parsing Training Data Preparation - Final Design Document
*For Grimbert - The Endless Nights Engine*
*Date: August 9, 2025*

## Executive Summary

This document outlines the complete strategy for preparing OnlyWorlds parsing training data that will:
1. Train LLMs to extract all 22 OnlyWorlds element types from narrative text
2. Populate schema-compliant fields with high accuracy
3. Create proper relationships between elements
4. Generate fixture-ready data for database seeding

## 1. Complete OnlyWorlds Schema Overview

### 1.1 All 22 Element Types
```
Character, Location, Object, Event, Species, Trait, Ability, Institution,
Family, Collective, Title, Language, Phenomenon, Zone, Construct, Creature,
Relation, Narrative, Law, Map, Marker, Pin
```

### 1.2 Critical Field Categories
- **Base Fields** (all elements): id, name, description, supertype, subtype, image_url, world
- **Link Fields**: Single-link (one reference) vs Multi-link (array of references)
- **Hierarchical Fields**: parent_X fields create tree structures
- **Temporal Fields**: start_date, end_date, founding_date, etc.
- **Intensity/Score Fields**: intensity (0-100), potency, reputation, etc.

## 2. Parsing Process Architecture

### Phase 1: Entity Detection & Classification
**Goal**: Find all named entities and classify into OnlyWorlds types

```yaml
input: "David Cheap, the first lieutenant of the Centurion, the squadron's flagship"
detection:
  - text: "David Cheap"
    type: character
    confidence: 0.95
  - text: "first lieutenant"
    type: title
    confidence: 0.90
  - text: "Centurion"
    type: object  # ship
    confidence: 0.85
  - text: "the squadron"
    type: institution
    confidence: 0.80
```

### Phase 2: Field Extraction & Population
**Goal**: Map detected entities to schema fields

```yaml
character_david_cheap:
  # Base fields
  id: "char_david_cheap_001"
  name: "David Cheap"
  description: "First lieutenant of the Centurion, burly Scotsman"
  
  # Character-specific fields
  Constitution:
    physicality: "burly, protracted nose, intense eyes"
    mentality: "in flight from debts and family disputes"
  
  Origins:
    background: "Scottish, family inheritance disputes, creditor problems"
    motivations: "escape debts, find suitable bride"
  
  Relations:
    titles: ["title_first_lieutenant_001"]
    institutions: ["inst_squadron_001"]
    
title_first_lieutenant:
  id: "title_first_lieutenant_001"
  name: "First Lieutenant"
  authority: "military command"
  holders: ["char_david_cheap_001"]
  institutions: ["inst_squadron_001"]
```

### Phase 3: Relationship Creation
**Goal**: Create explicit Relation elements for all connections

```yaml
relation_cheap_centurion:
  id: "rel_cheap_centurion_001"
  name: "David Cheap serves on Centurion"
  actor: "char_david_cheap_001"
  intensity: 75  # High - primary position
  
  Involves:
    characters: ["char_david_cheap_001"]
    objects: ["obj_centurion_001"]
    titles: ["title_first_lieutenant_001"]
    institutions: ["inst_squadron_001"]
  
  Nature:
    background: "Military service position"
    start_date: null  # Extract if mentioned
```

### Phase 4: Cross-Reference & Validation
**Goal**: Ensure all references are valid and bidirectional

```yaml
validation_checks:
  - All IDs follow format: {type}_{name}_{number}
  - All referenced IDs exist
  - Bidirectional links are consistent
  - Required fields are populated
  - Dates use world TIME units
```

### Phase 5: Fixture Generation
**Goal**: Create Django-loadable fixture format

```json
[
  {
    "model": "worlds.character",
    "pk": "char_david_cheap_001",
    "fields": {
      "name": "David Cheap",
      "description": "First lieutenant of the Centurion",
      "supertype": "character",
      "subtype": "officer",
      "physicality": "burly, protracted nose, intense eyes",
      "mentality": "debt-ridden, desperate",
      "titles": ["title_first_lieutenant_001"],
      "institutions": ["inst_squadron_001"]
    }
  }
]
```

## 3. Training Data Format - FINAL

### 3.1 Complete Entry Structure

```yaml
parse_example_001:
  # Source Information
  source:
    text: "David Cheap, the first lieutenant of the Centurion, the squadron's flagship, was no different."
    work: "The Wager"
    location: {chapter: 1, paragraph: 3, sentence: 2}
    context_before: "Each man carried his own burdensome story."
    context_after: "A burly Scotsman in his early forties..."
  
  # Extracted Elements (All Types)
  extracted:
    characters:
      - id: "char_david_cheap_001"
        name: "David Cheap"
        fields:
          physicality: "burly Scotsman, early forties, protracted nose, intense eyes"
          background: "inheritance disputes with brother, creditor problems"
          motivations: "find suitable bride, escape debts"
        links:
          titles: ["title_first_lieutenant_001"]
          institutions: ["inst_squadron_001"]
          objects: ["obj_centurion_001"]  # serves on ship
    
    titles:
      - id: "title_first_lieutenant_001"
        name: "First Lieutenant"
        fields:
          authority: "naval command"
          institutions: ["inst_squadron_001"]
          holders: ["char_david_cheap_001"]
    
    objects:
      - id: "obj_centurion_001"
        name: "Centurion"
        subtype: "flagship"
        fields:
          utility: "naval warfare"
          location: "at sea"
    
    institutions:
      - id: "inst_squadron_001"
        name: "The Squadron"
        fields:
          doctrine: "naval military"
    
    relations:
      - id: "rel_cheap_service_001"
        name: "Cheap serves as First Lieutenant"
        actor: "char_david_cheap_001"
        intensity: 85
        involves:
          characters: ["char_david_cheap_001"]
          titles: ["title_first_lieutenant_001"]
          objects: ["obj_centurion_001"]
          institutions: ["inst_squadron_001"]
  
  # Parsing Patterns & Insights
  patterns:
    entity_detection:
      - pattern: "[Name], the [title] of the [object]"
        creates: ["character", "title", "object", "relation"]
        confidence: 0.90
      
    field_mapping:
      - pattern: "Comma-separated title after name"
        maps_to: "Character.titles + Title element"
      
    relationship_inference:
      - pattern: "[title] of [object]"
        creates: "service/position relation"
        intensity_rule: "Officer positions = 70-90 intensity"
    
    hierarchical_structure:
      - pattern: "[object]'s [type]"
        creates: "parent-child relationship"
        example: "squadron's flagship" → Centurion.parent = Squadron
  
  # Confidence Scores
  confidence:
    entities: 0.95
    fields: 0.85
    relationships: 0.80
    overall: 0.87
  
  # Training Insights
  insights:
    - "Military ranks create both Title elements and high-intensity Relations"
    - "Ship names are Objects with utility='naval warfare'"
    - "'The' + collective noun often indicates Institution"
    - "Possessive chains create hierarchical relationships"
    - "Background exposition provides Origins.background and motivations"
```

### 3.2 Relationship Pattern Library

```yaml
relationship_patterns:
  
  # Family Relations
  family_patterns:
    - trigger: ["father", "mother", "son", "daughter", "brother", "sister"]
      creates:
        element_type: "family"
        relation_type: "kinship"
        intensity: 90-100
      example: "his father" → Family element + Relation(intensity=95)
  
  # Service Relations  
  service_patterns:
    - trigger: ["lieutenant of", "captain of", "servant to"]
      creates:
        element_type: "relation"
        relation_type: "service"
        intensity: 70-85
      links_to: ["title", "institution", "character"]
  
  # Ownership Relations
  ownership_patterns:
    - trigger: ["his", "her", "their", "'s"]
      creates:
        element_type: "relation"
        relation_type: "possession"
        intensity: 60-80
      example: "his sword" → Relation(actor=character, objects=[sword])
  
  # Event-Based Relations
  event_patterns:
    - trigger: ["killed", "married", "betrayed", "saved"]
      creates:
        element_type: "event"
        relation_type: "interaction"
        intensity: 80-100
      temporal: true  # Needs start_date
  
  # Location-Based Relations
  location_patterns:
    - trigger: ["from", "of", "in", "at"]
      creates:
        element_type: "relation"
        relation_type: "geographic"
        intensity: 40-60
      example: "Scotsman from Edinburgh" → birthplace field + location relation
```

### 3.3 Field Extraction Rules

```yaml
field_extraction_rules:
  
  # Physical Descriptions → Character.physicality
  physical_descriptors:
    triggers: ["tall", "short", "burly", "thin", "pale", "dark"]
    maps_to: "Character.Constitution.physicality"
    also_creates: "Trait elements if significant"
  
  # Mental/Emotional States → Character.mentality
  mental_descriptors:
    triggers: ["desperate", "ambitious", "fearful", "determined"]
    maps_to: "Character.Constitution.mentality"
    also_populates: "Character.motivations if goal-oriented"
  
  # Temporal Markers → date fields
  temporal_markers:
    triggers: ["founded in", "born in", "died in", "began"]
    maps_to: "*.start_date, *.end_date, *.founding_date"
    format: "Convert to world TIME units"
  
  # Power/Authority → intensity fields
  power_indicators:
    triggers: ["commanded", "ruled", "controlled", "led"]
    maps_to: "Relation.intensity (80-100)"
    also_creates: "Title elements for positions"
  
  # Group Membership → collections
  group_indicators:
    triggers: ["member of", "part of", "belonged to"]
    creates: "Collective or Institution element"
    links_via: "Relation with medium intensity (50-70)"
```

## 4. Attack Plan for Processing Parse Examples

### Step 1: Prepare Infrastructure
```bash
# Create organized output structure
/ow_parse_examples/
  /processed/
    blood_meridian_parsed.yaml
    hyperion_parsed.yaml
    wager_parsed.yaml
  /fixtures/
    blood_meridian_fixtures.json
    hyperion_fixtures.json
    wager_fixtures.json
  /patterns/
    extracted_patterns.yaml
    confidence_scores.yaml
  /training/
    combined_training_data.json
```

### Step 2: Process Each File Systematically

1. **Blood Meridian** (15 lines, icon-annotated)
   - Extract icon-marked entities
   - Infer relationships from context
   - Document violent/dark patterns

2. **Hyperion** (1064 lines, HTML structured)
   - Parse HTML structure
   - Extract 115 existing elements
   - Validate field mappings
   - Create missing Relations

3. **The Wager** (637 lines, HTML structured)
   - Parse HTML structure  
   - Extract 77 existing elements
   - Focus on maritime/military patterns
   - Create hierarchical relations

### Step 3: Pattern Synthesis
- Compile all unique patterns
- Rank by frequency and confidence
- Create pattern priority list
- Document edge cases

### Step 4: Fixture Generation
- Convert to Django fixture format
- Validate all cross-references
- Generate loading script
- Test in Django environment

## 5. Critical Questions for User

### 5.1 ID Generation Strategy
**Question**: Should IDs be deterministic (based on name/type) or random UUIDs?
- Deterministic pros: Easier debugging, predictable
- UUID pros: No collisions, standard Django
- **Recommendation**: Hybrid - deterministic prefix + short UUID

### 5.2 Confidence Thresholds
**Question**: What confidence level triggers manual review?
- High confidence (>0.8): Auto-accept
- Medium (0.5-0.8): Flag for review
- Low (<0.5): Require manual input
- **Need**: Your threshold preferences

### 5.3 Relationship Intensity Calculation
**Question**: How should we calculate relationship intensity?
- Frequency-based (mentions in text)
- Semantic-based (importance of interaction)
- Role-based (predefined by relationship type)
- **Need**: Scoring rubric preference

### 5.4 Parent-Child Hierarchies
**Question**: How deep should we infer hierarchies?
- Example: "Squadron's flagship's captain's quarters"
- Creates: Squadron → Flagship → Captain → Quarters
- **Need**: Maximum inference depth

### 5.5 Missing Field Handling
**Question**: How to handle unpopulated required fields?
- Generate placeholder values
- Mark as incomplete
- Infer from context
- **Need**: Completion strategy

### 5.6 Duplicate Entity Resolution
**Question**: How to handle same entity with variations?
- "The Judge" vs "Judge Holden" vs "The bald man"
- Merge into single entity
- Create separate with relations
- **Need**: Deduplication rules

### 5.7 Temporal Unit Conversion
**Question**: How to handle real-world dates in fantasy worlds?
- Keep Earth dates
- Convert to relative (Year 0 = first mention)
- Use narrative time (Chapter/Scene based)
- **Need**: Time system preference

## 6. Final Example - Complete Parse Entry

```yaml
# The Judge enters the tent - Blood Meridian
parse_final_example:
  source:
    text: "An enormous man dressed in an oilcloth slicker had entered the tent and removed his hat. He was bald as a stone and he had no trace of beard and he had no brows to his eyes nor lashes to them."
    work: "Blood Meridian"
    
  extracted:
    # Primary Character
    - type: "character"
      id: "char_judge_holden_001"
      name: "Judge Holden"
      description: "Enormous hairless man who exposes religious fraud"
      fields:
        physicality: "enormous, bald as stone, no beard, no eyebrows, no eyelashes"
        mentality: "serene and strangely childlike"
        height: 95  # percentile - enormous
      links:
        objects: ["obj_oilcloth_slicker_001", "obj_hat_001"]
        locations: ["loc_tent_001"]
        events: ["event_tent_entry_001"]
    
    # Objects
    - type: "object"
      id: "obj_oilcloth_slicker_001"
      name: "Oilcloth Slicker"
      fields:
        utility: "weather protection"
        materials: "oilcloth"
        aesthetics: "dark, waterproof"
    
    - type: "object"  
      id: "obj_hat_001"
      name: "The Judge's Hat"
      fields:
        utility: "head covering"
    
    # Location
    - type: "location"
      id: "loc_tent_001"
      name: "The Revival Tent"
      fields:
        function: "religious gathering"
        architecture: "temporary canvas structure"
    
    # Event
    - type: "event"
      id: "event_tent_entry_001"
      name: "Judge Enters Revival"
      fields:
        characters: ["char_judge_holden_001", "char_reverend_green_001"]
        locations: ["loc_tent_001"]
        consequences: "Reverend exposed as fraud"
    
    # Traits
    - type: "trait"
      id: "trait_hairless_001"
      name: "Completely Hairless"
      fields:
        physical_effects: "no hair, beard, brows, or lashes"
        social_effects: "unsettling, memorable"
        significance: 90  # Very unusual
    
    # Relations
    - type: "relation"
      id: "rel_judge_reverend_001"
      name: "Judge Exposes Reverend"
      actor: "char_judge_holden_001"
      intensity: 95  # Dramatic confrontation
      involves:
        characters: ["char_judge_holden_001", "char_reverend_green_001"]
        locations: ["loc_tent_001"]
        events: ["event_tent_entry_001"]
    
  patterns_demonstrated:
    - "Physical descriptions → Character.physicality + Trait elements"
    - "Clothing items → Object elements with utility field"
    - "Entry actions → Event elements with location"
    - "Unusual features → High-significance Traits"
    - "Confrontations → High-intensity Relations"
  
  fixture_output:
    - model: "worlds.character"
      pk: "char_judge_holden_001"
      fields:
        name: "Judge Holden"
        physicality: "enormous, completely hairless"
        traits: ["trait_hairless_001"]
        
  confidence:
    overall: 0.92
    rationale: "Clear character introduction with distinctive features"
```

## 7. Success Metrics

### Parsing Quality
- **Precision**: >85% of extracted elements are correct
- **Recall**: >80% of elements in text are found
- **Field Coverage**: >70% of applicable fields populated
- **Relationship Accuracy**: >75% of relations correctly identified

### Training Data Quality
- **Pattern Coverage**: >50 unique patterns documented
- **Confidence Distribution**: Normal curve centered at 0.75
- **Edge Cases**: >20 difficult examples included
- **Negative Examples**: >10 "do not parse" cases

## 8. Next Steps

1. **Await User Feedback** on critical questions
2. **Process Parse Examples** systematically
3. **Generate Fixtures** for each work
4. **Create Training Dataset** combining all examples
5. **Build Parser Tool** using training data
6. **Test on New Texts** to validate

---

*Ready to proceed with systematic processing once questions are answered.*

**Grimbert** - Building the parsing foundation for The Endless Nights Engine