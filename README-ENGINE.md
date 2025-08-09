# The Endless Nights Engine 🌑

A game engine that transforms OnlyWorlds data and text sources into atmospheric exploration experiences where knowledge has physical weight and endless nights reveal terrible truths.

## Quick Start

```bash
# Backend setup
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend setup  
cd frontend
npm install
npm run dev

# Parse your first world
python manage.py parse_world --source books/blood_meridian.pdf --name "The Border"
```

## What This Is

The Endless Nights Engine takes any world - from a book, a PDF, your OnlyWorlds data, or even scattered notes - and transforms it into a playable experience where:

- You're always **small and powerless**, observing giants
- **Knowledge has physical weight** - learn too much and you can't move
- **Nights never end**, they only get darker
- **Maps bleed** where people die, tear where you lie
- Every world **degrades differently** but inevitably

## Current Worlds

### 1. Efteling: Het Kleine Ruiter
*Thumb-sized ex-Bokkenrijder gathering intelligence in a fairy tale trial*
- Location: `worlds/efteling/`
- Status: ✅ Fully designed
- Features: Thread memory, size-based discovery, Dutch darkness

### 2. Raihappa: The Sand Chronicle  
*Scarab-sized scribe documenting a desert town becoming sand*
- Location: `worlds/raihappa/`
- Status: 🚧 Concept complete
- Features: Mirage layers, sand transformation, ant prophecies

### 3. Blood Meridian: The Ghost Dance
*Comanche warrior shrunk by vision, building resistance through ritual*
- Location: `worlds/blood-meridian/`
- Status: 🚧 Concept complete
- Features: Ritual progression, historical weight, spirit building

## Project Structure

```
📁 Project Root
├── 📄 PRD-FINAL-SYSTEMATIC.md      # Complete technical specification
├── 📄 PRD-ENDLESS-NIGHTS-ENGINE.md # Universal game design
├── 📄 CLAUDE.md                    # Development instructions
│
├── 📁 backend/                     # Django API (to be built)
│   ├── api/                       # REST/GraphQL endpoints
│   ├── worlds/                    # World models
│   ├── game/                      # Session management
│   └── parser/                    # Text→OnlyWorlds converter
│
├── 📁 frontend/                    # React UI (uses existing template)
│   ├── src/engine/                # Core mechanics
│   └── src/worlds/                # World-specific components
│
├── 📁 worlds/                      # World definitions
│   ├── efteling/                  # Bokkenrijders world
│   │   ├── WORLD-EFTELING-BOKKENRIJDERS.md
│   │   └── PRD-KLEINE-RUITER-FINAL.md
│   ├── raihappa/                  # Desert horror
│   └── blood-meridian/            # Comanche resistance
│
├── 📁 docs/                        # Documentation
│   ├── GAME-CONTEXT-COMPENDIUM.md # Philosophy & atmosphere
│   └── FINAL-BUILD-READY.md       # Consolidated guide
│
└── 📁 parser/                      # Source material processing
    └── (Book/PDF parsing system)
```

## Tech Stack

### Backend
- **Django 4.2** + **Django Ninja** - Fast API with automatic docs
- **PostgreSQL** - JSONB for flexible OnlyWorlds data
- **Redis** - Game state and real-time updates
- **Celery** - Background processing for large texts

### Frontend  
- **React 18** + **TypeScript** - Type-safe UI
- **Three.js** - Atmospheric 3D (not flashy)
- **Zustand** - State management
- **React Query** - Server state sync

### AI/LLM
- **Claude API** - Primary for complex narratives
- **OpenAI** - Cost-effective conversations
- **Local (Ollama)** - Privacy-conscious option

## Core Features

### The Witness System
Every world needs someone powerless who sees everything:
```javascript
witness: {
  size: "thumb" | "scarab" | "mite",
  perspective: "ground_level" | "inside_walls" | "between_words",
  burden: 0, // Increases with knowledge
  speed: 100 - burden // Slows as you learn
}
```

### Knowledge as Resource
Three types in every world:
```javascript
resources: {
  ephemeral: "Whispers",    // Decay over time
  physical: "Marks",        // Permanent but dangerous
  binding: "Oaths"          // Change reality when spoken
}
```

### The Living Map
```javascript
map: {
  tears: where_you_lied,
  burns: where_truth_was_spoken,
  bleeds: where_someone_died,
  scars: healed_wrong_creating_false_paths
}
```

### Degradation Engine
```
Night 1: "The moon illuminates your path"
Night 30: "Moon sees. Path."
Night 100: "M··n. P·t·."
Night ∞: "█░░█ █░█"
```

## Development Roadmap

### ✅ Completed
- World designs (Efteling, Raihappa, Blood Meridian)
- Game mechanics specification
- Architecture design
- OnlyWorlds integration plan

### 🚧 Phase 1: Foundation (Current)
- [ ] Set up Django backend
- [ ] Create world models
- [ ] Basic parser for text files
- [ ] Connect React frontend

### 📅 Phase 2: Core Engine
- [ ] Game session management
- [ ] Knowledge weight system
- [ ] Degradation mechanics
- [ ] Living map

### 📅 Phase 3: First World
- [ ] Efteling implementation
- [ ] LLM character conversations
- [ ] Thread memory system

### 📅 Phase 4: Parser System
- [ ] PDF/book extraction
- [ ] Entity recognition
- [ ] OnlyWorlds transformation

## How to Contribute

### Adding a New World
1. Answer the Five Questions:
   - Who is small? (The witness)
   - What has weight? (Resources)
   - What degrades? (Entropy pattern)
   - What's the treaty? (Hidden rules)
   - What's hidden? (The truth)

2. Create world folder: `worlds/your-world/`
3. Define OnlyWorlds schema
4. Implement witness mechanics
5. Add to world registry

### Parser Development
The parser transforms any text into a playable world:
```python
# Example: Parse a book
python manage.py parse_world \
  --source "path/to/book.pdf" \
  --world-name "My Dark World" \
  --witness-type "automatic"  # Let AI determine witness
```

## API Examples

### Initialize World
```http
GET /api/world/{world_id}/initialize
```

### Move Location
```http
POST /api/game/move
{
  "session_id": "xxx",
  "target_location_id": "yyy",
  "travel_method": "thread_path"
}
```

### Converse with Character
```http
POST /api/game/converse
{
  "session_id": "xxx",
  "character_id": "yyy",
  "player_input": "Show the goat hoof mark",
  "evidence_presented": ["mark_001", "whisper_023"]
}
```

## Environment Setup

```bash
# Required environment variables
DJANGO_SECRET_KEY=xxx
DATABASE_URL=postgresql://user:pass@localhost/endless_nights
REDIS_URL=redis://localhost:6379

# OnlyWorlds (optional, for direct integration)
ONLYWORLDS_API_KEY=xxx
ONLYWORLDS_PIN=xxxx

# LLM Providers (at least one required)
ANTHROPIC_API_KEY=xxx
OPENAI_API_KEY=xxx
```

## Philosophy

This isn't a game engine - it's a **witness engine**. A system for observing worlds as they degrade, for gathering intelligence that becomes physically heavier with each truth discovered.

Every world contains someone powerless who sees everything.  
Every world has information that matters.  
Every world degrades when observed too closely.  
Every world maintains itself through hidden agreements.  
Every world has a truth that, once known, cannot be unknown.

## Credits

- Original concept: TT
- Efteling world: Based on real Bokkenrijders trials (1743-1796)
- Monster sketches: TT's sister
- Technical design: Claude (Anthropic)

## License

MIT - But please credit if you use the witness engine concept.

---

*"In endless nights, small witnesses document large truths."*

**Ready to build. The worlds await their chroniclers.**