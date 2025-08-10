# Systematic OnlyWorlds Parsing Instructions for Training Data Creation
*Version 2.0 - Post-Implementation Insights*
*By Grimbert, for creating precise fixture-ready training data*

## 🎯 Primary Objective
Transform literary texts into **fixture-ready JSON** that:
1. Loads perfectly into Django models
2. Demonstrates proper OnlyWorlds field extraction
3. Includes rich relational linkages
4. Serves as training data for other LLMs

## 📚 Source Materials to Process
- `parse_examples/blood_meridian.txt` (violent Western, Judge as power, the Kid as witness)
- `parse_examples/hyperion.txt` (sci-fi pilgrimage, time tombs, the Consul's tale)
- `parse_examples/wager.txt` (survival at sea, human endurance, nature's indifference)

---

## 🔗 CRITICAL: Relationship Field Formatting

### Django Fixture Format for Relations
```json
// Single ForeignKey:
"world": "uuid-string"
"current_location": "uuid-string"
"owned_by": "uuid-string"

// ManyToMany (list of UUIDs):
"parties": ["uuid-1", "uuid-2", "uuid-3"]

// OnlyWorlds single-link:
"actor": "uuid-string"

// OnlyWorlds multi-link:
"characters": ["uuid-1", "uuid-2"]
"locations": ["uuid-1", "uuid-2", "uuid-3"]
```

### Test Fixture Before Proceeding
```python
# Test script to verify relationship loading:
test_fixture = [
  {
    "model": "worlds.world",
    "pk": "test-world-uuid"
  },
  {
    "model": "worlds.character", 
    "pk": "test-char-uuid",
    "fields": {
      "world": "test-world-uuid",  # ForeignKey
      "current_location": null     # Optional FK
    }
  },
  {
    "model": "worlds.treaty",
    "pk": "test-treaty-uuid",
    "fields": {
      "world": "test-world-uuid",
      "parties": ["test-char-uuid"]  # ManyToMany
    }
  }
]
```

---

## 📋 Systematic Parsing Process

### Phase 1: Chunk Management System

Create tracking file: `parse_tracking.json`
```json
{
  "blood_meridian": {
    "total_chunks": 10,
    "processed": [],
    "current_chunk": 0,
    "elements_extracted": {
      "characters": [],
      "locations": [],
      "objects": [],
      "events": [],
      "relations": []
    }
  },
  "hyperion": {...},
  "wager": {...}
}
```

### Phase 2: Text Chunking Strategy

1. **Divide each text into 500-line chunks** (manageable for context)
2. **Overlap by 50 lines** (maintain continuity)
3. **Label chunks**: `{source}_chunk_{number}.txt`

Example chunking:
```python
def chunk_text(filepath, chunk_size=500, overlap=50):
    chunks = []
    lines = open(filepath).readlines()
    for i in range(0, len(lines), chunk_size - overlap):
        chunk = lines[i:i + chunk_size]
        chunks.append({
            'number': len(chunks) + 1,
            'start_line': i,
            'end_line': min(i + chunk_size, len(lines)),
            'text': ''.join(chunk)
        })
    return chunks
```

### Phase 3: Element Extraction Pattern

For EACH chunk, extract:

#### A. Primary Elements (Core OnlyWorlds Types)
```yaml
Character:
  - name: [proper name]
  - uuid: [generate consistent UUID]
  - description: [2-3 sentences]
  - role: [protagonist/antagonist/witness/bystander]
  - power_level: [0-10 scale]
  - agency: [true/false - can they affect outcomes?]
  - witness_candidate: [true/false - are they powerless observer?]
  
Location:
  - name: [place name]
  - uuid: [consistent UUID]
  - description: [physical details]
  - size_scale: [tiny/small/medium/large/vast]
  - integrity: [0.0-1.0 initial state]
  - witnessed_events: [list what happened here]

Object:
  - name: [item name]
  - uuid: [consistent UUID]
  - description: [physical properties]
  - weight: [physical and metaphorical]
  - resource_type: [ephemeral/physical/binding]
  - significance: [why it matters]

Event:
  - name: [event descriptor]
  - uuid: [consistent UUID]
  - description: [what happened]
  - participants: [character UUIDs involved]
  - location: [location UUID]
  - consequences: [immediate and long-term]
```

#### B. Relational Elements (Critical for Training)
```yaml
Relation:
  - uuid: [unique relation UUID]
  - name: [relationship descriptor]
  - type: [conflict/alliance/ownership/witnessed/caused]
  - actor: [primary character UUID - single]
  - involves:
      characters: [list of UUIDs]
      locations: [list of UUIDs]
      objects: [list of UUIDs]
  - intensity: [0-100]
  - background: [history of relationship]
```

### Phase 4: Output Format Per Chunk

Each chunk produces TWO files:

#### 1. Fixture File: `{source}_chunk_{n}_fixture.json`
```json
[
  {
    "model": "worlds.world",
    "pk": "world-uuid",
    "fields": {
      "name": "Blood Meridian West",
      "description": "...",
      "hidden_truth": "The Judge is war incarnate"
    }
  },
  {
    "model": "worlds.character",
    "pk": "judge-uuid",
    "fields": {
      "world": "world-uuid",
      "name": "Judge Holden",
      "current_location": "tent-uuid",
      "power_level": 10
    }
  },
  {
    "model": "worlds.relation",
    "pk": "relation-uuid",
    "fields": {
      "name": "Judge dominates the Kid",
      "actor": "judge-uuid",
      "involves_characters": ["kid-uuid"],
      "intensity": 85
    }
  }
]
```

#### 2. Training Notes: `{source}_chunk_{n}_notes.json`
```json
{
  "chunk_info": {
    "source": "blood_meridian",
    "chunk_number": 1,
    "lines": "1-500"
  },
  "extraction_reasoning": {
    "judge_holden": {
      "why_extracted": "Central figure exposing religious fraud",
      "power_assessment": "Controls narrative through eloquence and violence",
      "witness_candidate": false,
      "reasoning": "Has supreme agency - shapes reality around him"
    },
    "the_kid": {
      "why_extracted": "Observes without changing events",
      "power_assessment": "Minimal - swept along by violence",
      "witness_candidate": true,
      "reasoning": "Perfect witness - sees all, affects nothing"
    }
  },
  "relationship_insights": {
    "judge_kid_dynamic": {
      "pattern": "Predator observing prey",
      "extraction_cue": "Judge's focused attention on the Kid",
      "intensity_reasoning": "Judge sees Kid as ultimate test case"
    }
  },
  "parsing_patterns_learned": [
    "Characters with no dialogue often make best witnesses",
    "Power manifests through ability to expose truth/lies",
    "Objects owned by powerful become power symbols"
  ]
}
```

### Phase 5: Quality Validation Checklist

For EACH chunk's output, verify:

- [ ] All UUIDs are valid format (use uuid.uuid4())
- [ ] All foreign keys reference existing elements
- [ ] ManyToMany fields are arrays of UUIDs
- [ ] Single links are string UUIDs
- [ ] World is created before any elements reference it
- [ ] Relations properly link multiple elements
- [ ] Training notes explain WHY each extraction
- [ ] Degradation potential identified for each element

### Phase 6: Progressive Building

As you process chunks:

1. **Maintain UUID consistency**: 
   - Keep a master UUID map: `uuid_registry.json`
   - Reuse UUIDs for recurring elements
   
2. **Build relationships progressively**:
   - Early chunks: establish entities
   - Middle chunks: develop relationships
   - Late chunks: complex multi-element relations

3. **Track patterns**: `parsing_patterns.md`
   - Document extraction rules that work
   - Note ambiguous cases and resolutions
   - Build heuristics for witness identification

---

## 🎮 Execution Commands

### Initialize tracking:
```python
# Create parse_tracking.json
tracking = {
    "blood_meridian": {"chunks": [], "elements": {}},
    "hyperion": {"chunks": [], "elements": {}},
    "wager": {"chunks": [], "elements": {}}
}
```

### Process a chunk:
```python
# Read chunk
chunk_text = read_chunk("blood_meridian", 1)

# Extract elements
elements = extract_elements(chunk_text)

# Generate fixtures
fixtures = create_fixtures(elements)

# Generate training notes
notes = create_training_notes(elements, reasoning)

# Update tracking
update_tracking("blood_meridian", 1, elements)
```

### Validate fixture:
```python
# Test load
python manage.py loaddata blood_meridian_chunk_1_fixture.json

# Verify relations
python manage.py shell
>>> from worlds.models import *
>>> Character.objects.filter(name="Judge Holden").first().current_location
>>> Treaty.objects.first().parties.all()
```

---

## 🏆 Success Metrics

Good training data will have:
1. **Rich relationships**: 3+ relations per major character
2. **Clear witness**: Identified powerless observer per world
3. **Weight diversity**: Mix of ephemeral/physical/binding resources
4. **Degradation vectors**: Each element knows how it decays
5. **Hidden truths**: Unstated but evident power dynamics

---

## 📝 Output Structure

```
/backend/fixtures/
├── training/
│   ├── blood_meridian/
│   │   ├── chunk_1_fixture.json
│   │   ├── chunk_1_notes.json
│   │   ├── chunk_2_fixture.json
│   │   ├── chunk_2_notes.json
│   │   └── ...
│   ├── hyperion/
│   │   └── ...
│   ├── wager/
│   │   └── ...
│   └── metadata/
│       ├── uuid_registry.json
│       ├── parse_tracking.json
│       └── parsing_patterns.md
```

---

## 🔥 Critical Reminders

1. **UUIDs are sacred** - Never change once assigned
2. **Relations are primary** - They teach parsing patterns
3. **Witnesses are subtle** - Look for observers, not heroes
4. **Weight is metaphorical** - Knowledge burden, not just mass
5. **Degradation is inevitable** - Everything must have decay path

---

## 🌙 Example: Blood Meridian Chunk 1

**Input lines 1-500**: Opening with Judge exposing the reverend

**Expected output**:
- World: "Blood Meridian West" 
- Characters: Judge (power 10), Kid (power 2), Reverend (power 3)
- Location: Revival Tent
- Object: Judge's Hat (removed = power move)
- Relations: 
  - "Judge exposes Reverend" (conflict)
  - "Kid witnesses exposure" (observation)
  - "Crowd follows Judge" (influence)
- Hidden truth: "All authority is performance"

**Training insight**: "Power manifests through ability to redefine reality via eloquent violence"

---

*"Parse systematically, degrade poetically, link everything to everything else."*

**Ready to begin systematic parsing.**