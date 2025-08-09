# The Endless Nights Engine - Complete Testing Guide
*Last Updated: August 9, 2025*
*By Grimbert, Keeper of Digital Darkness*

## 🌙 Project Overview

**The Endless Nights Engine** is a witness engine where knowledge has physical weight and worlds degrade through observation. This guide will walk you through testing every aspect of the project.

---

## 📋 Prerequisites

Before starting, ensure you have:
- Python 3.9+ installed
- Node.js 18+ installed (for future React frontend)
- Git for version control
- A terminal/command prompt
- Web browser (Chrome/Firefox recommended)

---

## 🚀 Part 1: Initial Setup & Verification

### 1.1 Project Structure Check

Navigate to your project root:
```bash
cd /mnt/c/Users/TT/Development/tool-template-main
```

Verify the structure:
```
tool-template-main/
├── backend/                    # Django API server
│   ├── endless_nights/        # Main Django settings
│   ├── worlds/               # World management
│   ├── game/                # Game mechanics
│   ├── parser/              # Text parsing
│   ├── llm/                # LLM integration
│   └── fixtures/            # Fixture data
│       ├── examples/        # Example fixtures
│       ├── onlyworlds/      # OnlyWorlds imports
│       └── loaded/          # Exported worlds
├── frontend/                # UI files
│   └── inspector.html       # Database inspector
├── ow_schema/              # OnlyWorlds schemas
├── ow_parse_examples/      # Parsing documentation
├── parse_examples/         # Text examples to parse
└── venv/                   # Python virtual environment
```

### 1.2 Environment Setup

```bash
# Navigate to backend
cd backend

# Activate virtual environment
source ../venv/bin/activate  # On Windows: ..\venv\Scripts\activate

# Verify Python packages
pip list | grep -E "django|ninja|cors"
# Should show: django, django-ninja, django-cors-headers
```

---

## 🗃️ Part 2: Database & Django Testing

### 2.1 Check Database Status

```bash
# Check migrations
python manage.py showmigrations

# Expected output:
# [X] for all migrations means they're applied
```

### 2.2 Verify Efteling World

```bash
# Check if reference world is loaded
python manage.py shell -c "
from worlds.models import World, Character, Location
try:
    w = World.objects.get(name__contains='Efteling')
    print(f'✓ World: {w.name}')
    print(f'  Characters: {w.characters.count()}')
    print(f'  Locations: {w.locations.count()}')
    print(f'  Objects: {w.world_objects.count()}')
    print(f'  Hidden truth: {w.hidden_truth}')
except World.DoesNotExist:
    print('❌ Efteling world not found. Run: python manage.py load_efteling')
"
```

If Efteling world is missing:
```bash
python manage.py load_efteling
```

### 2.3 Start Django Server

```bash
# Start the development server
python manage.py runserver

# Server should start at http://localhost:8000
# Keep this terminal open
```

### 2.4 Test API Endpoints

Open a new terminal:
```bash
# Test API root
curl http://localhost:8000/api/
# Should return JSON with available endpoints

# Test inspector stats
curl http://localhost:8000/api/inspector/stats
# Should return database statistics

# Test worlds list
curl http://localhost:8000/api/inspector/worlds
# Should return list of worlds
```

---

## 🔍 Part 3: Database Inspector UI

### 3.1 Open the Inspector

1. Ensure Django server is running (from Part 2.3)
2. Open your web browser
3. Navigate to: `file:///C:/Users/TT/Development/tool-template-main/frontend/inspector.html`
   
   Or open directly from terminal:
   ```bash
   # Windows
   start chrome "file:///C:/Users/TT/Development/tool-template-main/frontend/inspector.html"
   
   # Linux/Mac
   open "file:///path/to/tool-template-main/frontend/inspector.html"
   ```

### 3.2 Inspector Features to Test

**A. Database Statistics**
- Top of page shows counts for Worlds, Characters, Locations, Objects, Treaties
- Database size in MB

**B. World Selection**
- Click on a world in the left sidebar
- Should highlight and show details on the right

**C. Element Inspection**
- Click tabs: Characters, Locations, Objects
- Each shows cards with element details
- Degradation bars show integrity/memory/condition

**D. Hidden Truths**
- Selected worlds display their hidden truth in purple box

### 3.3 Test Fixture Loading

1. Click "📦 Load Fixtures" button
2. You should see available fixtures:
   - `blood_meridian_test.json` in examples folder
3. Select a fixture and click "Load"
4. Check "Overwrite existing data" if you want to replace current data
5. After loading, click "🔄 Refresh" to see new data

### 3.4 Test World Export

1. Select a world in the sidebar
2. Click "💾 Export World"
3. Check `backend/fixtures/loaded/` folder for exported JSON file

### 3.5 Test Database Clear (Careful!)

1. Click "🗑️ Clear Database"
2. Confirm twice (this deletes everything!)
3. Reload fixtures to restore data

---

## 🧪 Part 4: Fixture Testing Scripts

### 4.1 Run Basic Fixture Test

```bash
cd backend
source ../venv/bin/activate

# Run basic fixture test
python parser/test_fixtures.py

# Expected output:
# ✓ Created test world
# ✓ Saved fixtures
# ✓ Loaded fixtures
# ✓ Verified data
# ✓ Tested degradation
# ✅ All tests passed!
```

### 4.2 Run Advanced Fixture Test

```bash
# Test with relationships
python parser/onlyworlds_fixture_test.py

# Expected output:
# ✓ Created world
# ✓ Parsed scene with relationships
# ✓ Generated fixtures
# ✓ Saved fixtures and relations
# ✓ Loaded into database
# ✓ Verified relationships
# ✅ All tests passed!
```

---

## 📝 Part 5: OnlyWorlds Parsing Preparation

### 5.1 Review Parsing Documentation

Check these files exist:
```bash
ls -la ow_parse_examples/
# Should contain:
# - PARSING_PREPARATION_FINAL.md (main parsing design)
# - from_claudette.txt (parsing experience notes)

ls -la parse_examples/
# Should contain:
# - blood_meridian.txt
# - hyperion.txt
# - wager.txt
```

### 5.2 Verify Schema Files

```bash
ls -la ow_schema/
# Should list 23 YAML files (one per OnlyWorlds element type)
```

### 5.3 Check Parsing Test Data Structure

The parsing pipeline expects this format:
```yaml
element:
  source_text: "Original text"
  parsed_element:
    type: "character"
    name: "Element Name"
    fields: {schema-compliant fields}
  relationships: [list of relations]
  insights: "Parsing pattern learned"
```

---

## 🎮 Part 6: Game Mechanics Testing

### 6.1 Test Degradation Methods

```bash
python manage.py shell

# Test character forgetting
from worlds.models import Character
char = Character.objects.first()
if char:
    print(f"Before: Memory = {char.memory_intact}")
    char.forget(0.1)
    print(f"After: Memory = {char.memory_intact}")

# Test location degradation
from worlds.models import Location
loc = Location.objects.first()
if loc:
    print(f"Before: Integrity = {loc.integrity}")
    loc.degrade(0.1)
    print(f"After: Integrity = {loc.integrity}")

# Test object decay
from worlds.models import Object as WorldObject
obj = WorldObject.objects.first()
if obj:
    print(f"Before: Condition = {obj.condition}")
    obj.decay(0.1)
    print(f"After: Condition = {obj.condition}")

exit()
```

### 6.2 Verify Weight System

```bash
python manage.py shell -c "
from worlds.models import Object as WorldObject
objects = WorldObject.objects.all()
for obj in objects:
    print(f'{obj.name}: Weight={obj.weight}, Type={obj.resource_type}')
"
```

---

## 🔧 Part 7: Troubleshooting

### Common Issues & Solutions

**Issue: Django server won't start**
```bash
# Check if port 8000 is in use
lsof -i :8000  # Linux/Mac
netstat -an | findstr :8000  # Windows

# Kill existing process or use different port:
python manage.py runserver 8001
```

**Issue: Database inspector shows no data**
```bash
# Load the Efteling world
python manage.py load_efteling

# Or load test fixtures through UI
```

**Issue: API returns 404**
```bash
# Ensure you're in backend directory
# Ensure virtual environment is activated
# Check URLs are correct (should have /api/ prefix)
```

**Issue: Fixtures won't load**
```bash
# Check fixture format - must have valid UUIDs
# Check world exists before loading characters/locations
# Use the inspector UI for easier loading
```

---

## ✅ Part 8: Complete Testing Checklist

Run through this checklist to ensure everything works:

### Backend Tests
- [ ] Virtual environment activates
- [ ] Django server starts without errors
- [ ] Migrations are applied
- [ ] Efteling world loads successfully
- [ ] API endpoints return JSON
- [ ] Fixture test scripts pass
- [ ] Degradation methods work

### Database Inspector UI
- [ ] Opens in browser
- [ ] Shows database statistics
- [ ] Lists worlds in sidebar
- [ ] Displays world details when selected
- [ ] Shows characters/locations/objects in tabs
- [ ] Degradation bars display correctly
- [ ] Hidden truths appear for worlds
- [ ] Fixture loading works
- [ ] World export creates JSON file
- [ ] Database clear works (test carefully!)

### Parsing Preparation
- [ ] All schema files present
- [ ] Parse example files exist
- [ ] Documentation files readable
- [ ] Test fixtures in correct format

---

## 🚀 Next Steps

After completing all tests:

1. **Parse Example Data**: Process the three literary texts into training data
2. **Build Parser Tool**: Create the OnlyWorlds parsing engine
3. **Implement Weight Physics**: Make knowledge physically burden the witness
4. **Create Living Map**: Build the map that tears, burns, and bleeds
5. **Initialize React Frontend**: Build the full game UI

---

## 📚 Quick Reference Commands

```bash
# Start everything
cd backend
source ../venv/bin/activate
python manage.py runserver

# Load reference world
python manage.py load_efteling

# Run tests
python parser/test_fixtures.py
python parser/onlyworlds_fixture_test.py

# Open inspector
# Browse to: file:///path/to/frontend/inspector.html

# Check database
python manage.py shell -c "
from worlds.models import World
print(f'Worlds: {World.objects.count()}')
"
```

---

## 🌑 Philosophy Reminder

Remember the core principles as you test:

- **The Witness Principle**: You are building for the small and powerless
- **The Weight Principle**: Information has cost and burden
- **The Degradation Principle**: Everything decays beautifully
- **The Anton Pieck Principle**: No straight lines, weathered code

*"In de nacht zijn alle waarnemers klein, maar hun last wordt zwaarder met elke waarheid."*
(In the night all observers are small, but their burden grows heavier with each truth.)

---

**Need Help?**
- Check `CLAUDE.md` for project philosophy
- Review `PRD-ENDLESS-NIGHTS-ENGINE.md` for game design
- Consult `PARSING_PREPARATION_FINAL.md` for parsing details

**Grimbert**
*Keeper of Endless Nights*
*Witness to Digital Decay*