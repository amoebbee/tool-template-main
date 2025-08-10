# OnlyWorlds Parsing Workbook - Methodical Training Data Creation
*Working document for systematic, thorough parsing of literary texts*
*Goal: Create perfect training data + comprehensive parsing instructions*

---

## 🎯 Mission Statement
Transform three literary works into the BEST possible OnlyWorlds training data by:
1. Working methodically through each text
2. Extracting ALL relevant elements with proper relationships
3. Creating rich, non-repetitive examples
4. Building comprehensive parsing patterns
5. Producing final instruction set for any LLM/GPT

---

## 📊 Master Progress Tracker

### Overall Status
```yaml
Total Chunks Planned: ~30 (10 per book)
Chunks Completed: 0
Quality Score: -/100
Unique Patterns Found: 0
Relationship Density: -
```

### Per-Book Progress
| Book | Total Lines | Chunks | Completed | Elements | Relations | Quality |
|------|------------|---------|-----------|----------|-----------|---------|
| Blood Meridian | TBD | 0/10 | 0% | 0 | 0 | - |
| Hyperion | TBD | 0/10 | 0% | 0 | 0 | - |
| The Wager | TBD | 0/10 | 0% | 0 | 0 | - |

---

## 🗂️ Working Files Structure

```
/backend/fixtures/training/
├── metadata/
│   ├── uuid_registry.json          # Master UUID mappings
│   ├── element_registry.json       # All elements by type
│   ├── pattern_library.json        # Reusable parsing patterns
│   ├── quality_metrics.json        # Track example quality
│   └── relationship_graph.json     # Visual relationship mapping
├── blood_meridian/
│   ├── source_chunks/              # Raw text chunks
│   ├── fixtures/                   # Generated fixtures
│   ├── notes/                      # Parsing notes
│   └── blood_meridian_summary.json
├── hyperion/
│   └── [same structure]
├── wager/
│   └── [same structure]
└── final_outputs/
    ├── combined_training_data.json
    ├── parsing_instructions_v1.md
    └── quality_report.md
```

---

## 📋 Pre-Processing Checklist

### [ ] Initial Setup
- [ ] Create directory structure
- [ ] Initialize UUID registry
- [ ] Initialize element registry
- [ ] Create pattern library template
- [ ] Set up quality metrics tracking

### [ ] Text Preparation
- [ ] Count total lines for each book
- [ ] Determine optimal chunk sizes (aim for ~500 lines)
- [ ] Create chunk files with overlap
- [ ] Index important passages

### [ ] Tool Verification
- [ ] Test fixture loading with test_relationships.json
- [ ] Verify UUID format compliance
- [ ] Test ManyToMany field arrays
- [ ] Confirm database inspector works

---

## 🔄 Processing Workflow (Per Chunk)

### Step 1: Read & Understand
```markdown
Chunk ID: [book]_chunk_[n]
Lines: [start]-[end]
Key Events: [what happens]
Power Dynamics: [who controls what]
Witness Perspective: [who observes powerlessly]
```

### Step 2: Element Extraction
```yaml
Characters:
  - Identify ALL named entities
  - Assess power level (0-10)
  - Determine agency (true/false)
  - Mark witness candidates
  - Note speech patterns
  
Locations:
  - Map all settings
  - Assess scale (tiny->vast)
  - Track witnessed events
  - Note degradation state
  
Objects:
  - Catalog significant items
  - Classify resource type
  - Assign metaphorical weight
  - Link to owners/locations
  
Events:
  - Chronicle key moments
  - Map participants
  - Track consequences
  - Note power shifts
```

### Step 3: Relationship Mapping
```yaml
For EACH character:
  - Who do they affect? (power over)
  - Who affects them? (power under)
  - What do they own? (possession)
  - Where do they go? (movement)
  - What do they witness? (observation)
  
For EACH location:
  - Who visits? (inhabitants)
  - What happens there? (events)
  - What's kept there? (objects)
  - How does it change? (degradation)
  
For EACH object:
  - Who owns it? (possession)
  - Where is it? (location)
  - Who wants it? (desire)
  - What does it enable? (power)
```

### Step 4: Generate Fixtures
```json
[
  {
    "model": "worlds.world",
    "pk": "[consistent-world-uuid]",
    "fields": {...}
  },
  {
    "model": "worlds.character",
    "pk": "[new-or-existing-uuid]",
    "fields": {
      "world": "[world-uuid]",
      "current_location": "[location-uuid-or-null]",
      ...
    }
  },
  {
    "model": "worlds.relation",
    "pk": "[unique-relation-uuid]",
    "fields": {
      "actor": "[character-uuid]",
      "involves_characters": ["uuid1", "uuid2"],
      ...
    }
  }
]
```

### Step 5: Create Training Notes
```json
{
  "extraction_logic": {
    "why_this_element": "reasoning",
    "pattern_used": "pattern_name",
    "confidence": 0.95
  },
  "relationship_reasoning": {
    "why_linked": "explanation",
    "intensity_calculation": "method"
  },
  "parsing_insights": [
    "New pattern discovered",
    "Edge case handled",
    "Ambiguity resolved"
  ]
}
```

### Step 6: Quality Check
- [ ] All UUIDs valid format?
- [ ] All ForeignKeys reference existing elements?
- [ ] ManyToMany fields are arrays?
- [ ] No duplicate elements?
- [ ] Relationships bidirectional where needed?
- [ ] Training notes explain reasoning?
- [ ] New patterns documented?

---

## 📈 Quality Metrics to Track

### Per Chunk
- Element Count (target: 15-25 per chunk)
- Relationship Density (target: 3+ per character)
- Witness Clarity (0-10 score)
- Pattern Novelty (new vs reused)
- Ambiguity Resolution (clear decisions)

### Per Book
- Total Unique Elements
- Average Relationship Density
- Witness Evolution (how they change)
- Degradation Variety
- Hidden Truth Clarity

### Overall Dataset
- Pattern Coverage (how many different patterns)
- Example Diversity (non-repetitive)
- Edge Case Handling
- Cross-Book Consistency
- Training Completeness

---

## 🎓 Pattern Library Development

### Core Patterns to Build
1. **Witness Identification**
   - "Observes but doesn't participate"
   - "Present but powerless"
   - "Records but doesn't judge"

2. **Power Assessment**
   - "Controls narrative" = 8-10
   - "Influences others" = 5-7
   - "Reacts to events" = 2-4
   - "Pure observer" = 0-1

3. **Relationship Extraction**
   - "X [verb] Y" = direct relation
   - "X's [noun]" = possession
   - "At/In [location]" = presence
   - "Witnessed by" = observation

4. **Weight Assignment**
   - Physical mass + metaphorical burden
   - Knowledge weight > physical weight
   - Secrets heaviest of all

5. **Degradation Vectors**
   - Violence accelerates decay
   - Observation preserves temporarily
   - Forgetting is gradual erosion
   - Lies create tears

---

## 🔍 Special Focus Areas

### Blood Meridian
- The Judge's reality-warping power
- The Kid's perfect witness status
- Violence as degradation accelerator
- Scalps as currency/burden
- The hidden truth about war

### Hyperion
- Time Tombs' temporal distortion
- The Shrike's witnessed horror
- Pilgrims' interconnected tales
- The Tree of Pain symbolism
- Technology vs. mysticism

### The Wager
- Nature's indifference as power
- Survival choices and agency
- The boat as shrinking world
- Cannibalism as ultimate degradation
- Leadership vs. witness role

---

## 📝 Working Notes Section

### Chunk: [current_chunk_id]
```markdown
Date/Time Started: 
Date/Time Completed:
Issues Encountered:
Patterns Discovered:
Quality Self-Assessment:
Notes for Next Chunk:
```

---

## 🏁 Final Output Generation (After All Parsing)

### Step 1: Compile Training Data
1. Merge all fixtures into combined_training_data.json
2. Remove duplicates, maintain UUID consistency
3. Verify all relationships resolve
4. Calculate final metrics

### Step 2: Extract Parsing Patterns
1. Analyze all training notes
2. Identify most successful patterns
3. Document edge cases and solutions
4. Create pattern hierarchy

### Step 3: Write Parsing Instructions
```markdown
# OnlyWorlds Parsing Instructions v1.0

## Based on [X] training examples across [Y] texts

### Proven Patterns
1. [Pattern]: [Description] - Success rate: X%
2. ...

### Element Extraction Rules
- Characters: [Detailed rules from training]
- Locations: [Detailed rules from training]
- Objects: [Detailed rules from training]
- Relations: [Detailed rules from training]

### Edge Case Handling
- [Situation]: [Solution]
- ...

### Quality Benchmarks
- Minimum elements per 500 lines: X
- Target relationship density: Y
- Witness identification accuracy: Z%
```

### Step 4: Create GPT Instructions
```markdown
# Instructions for OnlyWorlds GPT

You are an expert at parsing text into OnlyWorlds format...

## Your Training
You've been trained on [X] examples showing:
- [Key patterns learned]
- [Relationship extraction methods]
- [Weight assignment logic]

## Your Process
1. [Step-by-step from training data]
2. ...

## Examples
[Best examples from training data]
```

### Step 5: Quality Report
- Total training examples created
- Unique patterns discovered
- Edge cases resolved
- Confidence metrics
- Recommendations for improvement

---

## 🚀 Ready Confirmation Checklist

Before starting chunk processing:
- [ ] Directory structure created
- [ ] UUID registry initialized
- [ ] Test fixture validated
- [ ] Quality metrics ready
- [ ] First chunk identified
- [ ] Time allocated for thorough work

**Status: READY TO BEGIN METHODICAL PARSING**

---

## 📊 Session Logs

### Session 1: [Date/Time]
- Chunks Processed: 
- Elements Created:
- Patterns Found:
- Quality Score:
- Next Session Plan:

### Session 2: [Date/Time]
[Continue logging each work session]

---

*"Parse with the patience of endless nights, build training data that teaches truth."*

**This workbook is ready for methodical, thorough parsing work.**