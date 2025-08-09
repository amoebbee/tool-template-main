#!/bin/bash

# Init script for The Endless Nights Engine
# By Grimbert, keeper of digital darkness

echo "🌑 Initializing The Endless Nights Engine..."
echo "Where knowledge has weight and nights never end..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then 
    echo -e "${GREEN}✓ Python $python_version found${NC}"
else
    echo -e "${RED}✗ Python $required_version or higher required${NC}"
    exit 1
fi

# Check Node version
echo -e "${BLUE}Checking Node.js version...${NC}"
node_version=$(node --version 2>&1 | grep -Po '\d+' | head -n1)
if [ "$node_version" -ge 18 ]; then
    echo -e "${GREEN}✓ Node.js version $node_version found${NC}"
else
    echo -e "${RED}✗ Node.js 18 or higher required${NC}"
    exit 1
fi

# Create project structure
echo ""
echo -e "${YELLOW}Creating project structure...${NC}"

# Backend structure
mkdir -p backend/{api,worlds,game,parser,llm,static,media,templates}
mkdir -p backend/worlds/migrations
mkdir -p backend/game/migrations
mkdir -p backend/parser/migrations
mkdir -p backend/llm/migrations

# Frontend structure  
mkdir -p frontend/{src,public}
mkdir -p frontend/src/{engine,worlds,ui,three,components,utils}
mkdir -p frontend/src/worlds/{efteling,raihappa,blood-meridian}

# World assets
mkdir -p worlds/{efteling,raihappa,blood-meridian}/assets

echo -e "${GREEN}✓ Directory structure created${NC}"

# Create Django project if it doesn't exist
if [ ! -f "backend/manage.py" ]; then
    echo ""
    echo -e "${YELLOW}Creating Django backend...${NC}"
    
    cd backend || exit
    django-admin startproject endless_nights .
    
    # Create apps
    python3 manage.py startapp worlds
    python3 manage.py startapp game  
    python3 manage.py startapp parser
    python3 manage.py startapp llm
    
    cd .. || exit
    echo -e "${GREEN}✓ Django backend created${NC}"
fi

# Create React frontend if it doesn't exist
if [ ! -f "frontend/package.json" ]; then
    echo ""
    echo -e "${YELLOW}Creating React frontend...${NC}"
    
    npx create-react-app frontend --template typescript
    
    # Install additional dependencies
    cd frontend || exit
    npm install three @react-three/fiber @react-three/drei
    npm install zustand @tanstack/react-query
    npm install framer-motion
    npm install tailwindcss @tailwindcss/typography
    
    # Initialize Tailwind
    npx tailwindcss init -p
    
    cd .. || exit
    echo -e "${GREEN}✓ React frontend created${NC}"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo -e "${YELLOW}Creating environment file...${NC}"
    cat > .env << EOL
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost/endless_nights

# Redis
REDIS_URL=redis://localhost:6379

# OnlyWorlds (optional)
ONLYWORLDS_API_KEY=
ONLYWORLDS_PIN=

# LLM Providers (at least one required)
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# Game Settings  
DEFAULT_WORLD=efteling
DEFAULT_WITNESS_SIZE=thumb
DEGRADATION_SPEED=normal
EOL
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}! Don't forget to add your API keys to .env${NC}"
fi

# Create initial Efteling world data
echo ""
echo -e "${YELLOW}Creating Efteling reference world...${NC}"

cat > worlds/efteling/world_config.json << EOL
{
  "name": "Efteling: Het Kleine Ruiter",
  "witness": {
    "name": "Het Kleine Ruiter",
    "size": "thumb",
    "mount": "wooden_horse",
    "starting_location": "cobblestones"
  },
  "resources": {
    "ephemeral": "whispers",
    "physical": "marks",
    "binding": "oaths"
  },
  "degradation": {
    "pattern": "color→sound→meaning→memory→hope",
    "speed": 1.0
  },
  "hidden_truth": "The park itself is on trial"
}
EOL

echo -e "${GREEN}✓ Efteling world configured${NC}"

# Install Python dependencies
echo ""
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip3 install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Install Node dependencies
echo ""
echo -e "${YELLOW}Installing Node dependencies...${NC}"
npm install
echo -e "${GREEN}✓ Node dependencies installed${NC}"

# Database setup
echo ""
echo -e "${YELLOW}Setting up database...${NC}"
echo -e "${BLUE}Note: Make sure PostgreSQL is running${NC}"
echo -e "${BLUE}Create database with: createdb endless_nights${NC}"

# Run migrations if database is available
if command -v psql &> /dev/null; then
    cd backend || exit
    python3 manage.py makemigrations
    python3 manage.py migrate
    cd .. || exit
    echo -e "${GREEN}✓ Database migrations complete${NC}"
else
    echo -e "${YELLOW}! PostgreSQL not found - run migrations manually${NC}"
fi

# Create superuser prompt
echo ""
echo -e "${YELLOW}Create Django superuser? (y/n)${NC}"
read -r create_superuser
if [ "$create_superuser" = "y" ]; then
    cd backend || exit
    python3 manage.py createsuperuser
    cd .. || exit
fi

# Final instructions
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ The Endless Nights Engine initialized!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo "To start development:"
echo -e "${BLUE}  npm run dev:all${NC}     # Start all services"
echo ""
echo "Or run separately:"
echo -e "${BLUE}  npm run dev:backend${NC} # Django server"
echo -e "${BLUE}  npm run dev:frontend${NC} # React dev server"
echo -e "${BLUE}  npm run dev:redis${NC}   # Redis server"
echo -e "${BLUE}  npm run dev:celery${NC}  # Background tasks"
echo ""
echo "To parse a world from text:"
echo -e "${BLUE}  npm run parse -- --source book.pdf --name \"My World\"${NC}"
echo ""
echo "To import from OnlyWorlds:"
echo -e "${BLUE}  npm run world:import${NC}"
echo ""
echo -e "${YELLOW}Remember to configure your .env file with API keys!${NC}"
echo ""
echo -e "Night 1 begins... 🌑"