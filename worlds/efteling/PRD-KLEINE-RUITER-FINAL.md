# Het Kleine Ruiter - Final Game Design Document
*The Little Rider: A Game of Endless Nights and Gathering Shadows*

## Core Premise: The Oath That Binds

You are **Het Kleine Ruiter** - a thumb-sized former Bokkenrijder, cursed to ride through endless nights in the Efteling. You were shrunk not as punishment, but as protection - the Brotherhood couldn't kill what they couldn't find. Now you gather intelligence in a world where information is the only currency that matters, where every fairy tale character might be a hidden Bokkenrijder, and where the dawn never truly comes.

The curse is simple: you're small, you're alone, and you remember everything while everyone else forgets each dawn that never arrives.

## The Dread: Endless Night Mechanics

### The Pressure That Never Names Itself
- **No explicit timer** - but shadows grow longer each "hour"
- **The Thirteenth Hour** - after midnight strikes twelve times, it strikes again... and again...
- **Degradation** - colors slowly drain, sounds become muffled, eventually only whispers remain
- **The Watchers** - silhouettes appear in peripheral vision, growing more numerous
- **The Oath Whispers** - fragments of the Bokkenrijder oath echo randomly, getting louder

### The Night Counter
```
Night 1: "The moon is bright"
Night 7: "The moon has eyes"
Night 13: "The moon remembers your name"
Night 31: "There was never a sun"
Night 100: "..."
Night ∞: [text becomes unreadable]
```

## Knowledge as Resource: The Intelligence System

### The Three Currencies of Information

#### 1. **Whispers** (Ephemeral Knowledge)
- Overheard conversations that fade unless preserved
- Can be traded to characters for immediate favors
- Deteriorate: lose 1 clarity per hour
- Visual: Float as semi-transparent text fragments around your character

#### 2. **Marks** (Physical Evidence)
- Bokkenrijder signs carved in wood, drawn in dirt
- Town defenses, escape routes, meeting places
- Permanent once found but dangerous to carry
- Visual: Appear as glowing symbols on your map

#### 3. **Oaths** (Binding Knowledge)
- Fragments of the Bokkenrijder oath and counter-oaths
- Village protection charms and identification methods
- Can be combined to create new powers or curses
- Visual: Written in your horse's mane, growing like strange hair

### Knowledge Transmutation Mechanics

```javascript
// Knowledge can be combined and transformed
const transmutationRecipes = {
  // Defensive Transmutations
  "protection_charm": {
    requires: ["whisper_of_fear", "mark_of_threshold", "oath_fragment"],
    creates: "ward_against_riders",
    description: "Protects a location from Bokkenrijder entry for one night"
  },
  
  // Offensive Transmutations
  "accusation": {
    requires: ["whisper_of_suspicion", "mark_of_meeting", "name"],
    creates: "evidence_bundle",
    description: "Enough to condemn someone as a Bokkenrijder"
  },
  
  // Neutral Transmutations
  "memory_thread": {
    requires: ["whisper_fading", "horse_hair", "true_name"],
    creates: "permanent_memory",
    description: "Preserves knowledge across nights"
  }
};
```

### The Intelligence Map

The map is abstract but physical - drawn on parchment that tears and stains:

```
         [Villa Volta]
              ◊----whisper: "Hugo never sleeps"
             /|\
            / | \
    [Chapel]  |  [Crossroads]
        ○-----+-----●----mark: goat hoof
        |           |
   [Gnome Village] [Mill]
        ◊-----------○
     oath: "renounce the light"
```

- **Lines** = Known paths (solid) or suspected connections (dotted)
- **Symbols** = Type of intelligence gathered
- **Decay** = Map physically deteriorates, must be redrawn from memory
- **Overlays** = Multiple transparent maps can be layered to reveal patterns

## Bokkenrijder Integration: The Brotherhood Dynamics

### The Living Roster
Every character in the Efteling might be a Bokkenrijder. You must identify:

#### Confirmed Riders
- **Hugo van den Loonsche Duinen** (Villa Volta) - Your former captain
- **The Ezel** (Donkey) - Doesn't poop gold, poops *guild coins* with faces
- **De Rode Schoentjes** - Not cursed shoes, but transportation between meetings

#### Suspected Riders
- Characters give themselves away through:
  - Using specific phrases from the oath
  - Recognizing old Bokkenrijder signs
  - Reacting to your former rank insignia
  - Fear when certain names are mentioned

#### The Innocent
- Proving innocence is harder than proving guilt
- Some pretend to be Riders for protection
- Others are falsely accused for revenge

### Intra-Bokkenrijder Diplomacy

```javascript
// Reputation system within the Brotherhood
const brotherhoodStanding = {
  "hugo_volta": {
    relationship: "former_captain",
    trust: -2, // Knows you betrayed the oath
    leverage: "knows your true name",
    useful_for: "accessing Villa Volta's archives"
  },
  
  "the_silent_ones": {
    relationship: "parallel_cell",
    trust: 0, // Neutral, watching
    leverage: "mutual blackmail",
    useful_for: "safe passage through certain areas"
  },
  
  "the_hanged": {
    relationship: "martyrs",
    trust: +1, // Respect your curse as punishment
    leverage: "shared suffering",
    useful_for: "learning counter-oaths"
  }
};
```

### The Oath Mechanics

Players discover fragments of the Bokkenrijder oath. Speaking them has power but also consequences:

1. **"I renounce..."** - Makes you invisible to holy protection
2. **"...the Devil's mount..."** - Allows fast travel but marks your path
3. **"...brothers in shadow..."** - Reveals other Riders but also reveals you
4. **Complete Oath** - Terrible power, terrible price

## UI Design: Information Warfare Interface

### Main Screen Layout

```
┌─────────────────────────────────────────────────┐
│  [Mist]           [Moon Phase]          [Night ∞]│
├─────────────────────────────────────────────────┤
│                                                  │
│           [3D Efteling - Tiny Perspective]      │
│                                                  │
│     🐎 <- You are here (actual size)            │
│                                                  │
├──────────────┬──────────────────────────────────┤
│ WHISPERS (3) │        INTELLIGENCE MAP          │
│              │    [Torn Parchment Aesthetic]    │
│ "moon at chapel"                                │
│ fading...    │      ◊---?---●                   │
│              │      |       |                   │
│ "hugo knows" │      ○       ▲ (you)             │
│ clear        │                                  │
├──────────────┼──────────────────────────────────┤
│ MARKS (5)    │ OATHS COLLECTED                  │
│ ○ ◊ ● ▲ ✗    │ "I ren___ce G_d an_ sw__r..."   │
└──────────────┴──────────────────────────────────┘
```

### The Knowledge Journal (Right Panel)

Appears as a worn leather book, pages physically accumulate:

```
┌─────────────────────────┐
│ PERSONS OF INTEREST     │
├─────────────────────────┤
│ Lange Jan               │
│ Status: [UNKNOWN]       │
│ Evidence:               │
│ • Grows during oaths    │
│ • Avoids crossroads     │
│ • [WHISPER SLOT]        │
│ • [MARK SLOT]           │
│ Verdict: ___________    │
├─────────────────────────┤
│ Holle Bolle Gijs        │
│ Status: [SUSPECTED]     │
│ Evidence:               │
│ • Eats written oaths    │
│ • Coins found inside    │
│ • Knows your old name   │
│ Verdict: RIDER?         │
└─────────────────────────┘
```

### The Tiny Perspective Camera

- **Ground Level View**: See between cobblestones, under doors
- **Climb Mode**: Scale vertical surfaces slowly, revealing hidden marks
- **Ride Mode**: On insects/rats for faster travel but less control
- **Hide Mode**: Inside cracks, behind objects - hear but don't see

### Conversation Interface

```
┌─────────────────────────────────────────┐
│ [Character Portrait - You look up at them] │
├─────────────────────────────────────────┤
│ LANGE JAN: "Strange... you're so small,  │
│ yet you cast such a long shadow..."      │
├─────────────────────────────────────────┤
│ > [WHISPER] "The moon saw you at chapel" │
│ > [MARK] Show the goat hoof sign         │
│ > [OATH] "By the mount we rode..."       │
│ > [SILENCE] Say nothing, observe         │
├─────────────────────────────────────────┤
│ Trust: ▓▓▓░░ | Fear: ▓▓▓▓▓ | Knows: ?   │
└─────────────────────────────────────────┘
```

## Game Mechanics: The Dread and the Discovery

### Information Gameplay Loop

1. **Gather** - Overhear, observe marks, find oath fragments
2. **Preserve** - Quick decisions about what to keep before it fades
3. **Connect** - Draw lines between intelligence on your map
4. **Confront** - Use information to pressure, protect, or expose
5. **Survive** - Each revelation changes who hunts you

### The Weight of Knowledge

```javascript
// Knowledge has physical weight in the game
class IntelligenceInventory {
  constructor() {
    this.capacity = 7; // Lucky number, or cursed?
    this.whispers = [];
    this.marks = [];
    this.oaths = [];
  }
  
  addWhisper(whisper) {
    if (this.totalWeight() >= this.capacity) {
      // Must forget something to learn something new
      this.promptForget();
    }
    whisper.decay = setInterval(() => {
      whisper.clarity--;
      if (whisper.clarity <= 0) {
        this.whispers = this.whispers.filter(w => w !== whisper);
      }
    }, 60000); // Decay every "hour"
  }
  
  combineIntelligence(pieces) {
    // Combining intelligence creates new truths but destroys originals
    const result = this.transmute(pieces);
    pieces.forEach(p => this.destroy(p));
    return result;
  }
}
```

### Environmental Storytelling Through Size

```javascript
// Your tiny size reveals different information
const sizeRevelations = {
  "between_cobblestones": {
    discover: "Hidden messages written in ant trails",
    risk: "Can be stepped on",
    mood: "Claustrophobic safety"
  },
  
  "inside_walls": {
    discover: "Contracts, confessions, condemned names",
    risk: "Getting lost in the dark",
    mood: "Reading history's accusations"
  },
  
  "under_doors": {
    discover: "Private conversations, secret meetings",
    risk: "Being discovered and trapped",
    mood: "Spy's anxiety"
  },
  
  "in_gijs_mouth": {
    discover: "What he's really swallowing - oaths, names, evidence",
    risk: "Being swallowed with the secrets",
    mood: "Digestive horror"
  }
};
```

## Building Steps: Technical Implementation

### Phase 1: The Dread Foundation (Week 1)
```javascript
// Core atmosphere system
const DreadEngine = {
  nightCounter: 1,
  dreadLevel: 0,
  
  async incrementNight() {
    this.nightCounter++;
    this.dreadLevel = Math.log(this.nightCounter);
    
    // Environmental changes
    await this.adjustColors(this.dreadLevel);
    await this.muteSound(this.dreadLevel);
    await this.addWatchers(Math.floor(this.dreadLevel));
    
    // UI degradation
    if (this.nightCounter > 30) {
      document.querySelector('.ui').style.filter = `blur(${this.dreadLevel}px)`;
    }
  }
};
```

### Phase 2: Intelligence Systems (Week 2)
```javascript
// Knowledge management
class KnowledgeSystem {
  constructor() {
    this.storage = new Map();
    this.connections = new Graph();
    this.decay = new DecaySystem();
  }
  
  captureWhisper(text, location, speaker) {
    const whisper = {
      id: uuid(),
      content: text,
      clarity: 100,
      source: speaker,
      location: location,
      timestamp: this.currentNight,
      connections: []
    };
    
    // Auto-connect to related knowledge
    this.findConnections(whisper);
    
    // Start decay
    this.decay.track(whisper);
    
    return whisper;
  }
}
```

### Phase 3: Bokkenrijder AI (Week 3)
```javascript
// Character AI with hidden loyalties
class BokkenrijderAI {
  constructor(character, worldState) {
    this.character = character;
    this.isRider = this.rollSecret(); // Player must discover
    this.oathFragments = this.generateOathKnowledge();
    this.fearOfExposure = Math.random();
  }
  
  async respond(playerAction, evidence) {
    // Check if player has leverage
    const leverage = this.assessLeverage(evidence);
    
    // Generate response based on fear/trust
    const response = await this.llm.generate({
      temperature: 0.7 + (this.fearOfExposure * 0.2),
      
      systemPrompt: `
        You are ${this.character.name} in the Efteling after dark.
        Secret: You ${this.isRider ? 'ARE' : 'are NOT'} a Bokkenrijder.
        
        The tiny rider presents: ${evidence}
        Your fear level: ${this.fearOfExposure}
        
        If you ARE a Rider:
        - Deflect suspicion unless cornered
        - Use oath phrases subtly when nervous
        - Try to identify if the tiny rider is Brotherhood
        
        If you're NOT a Rider:
        - You might pretend to be one for protection
        - OR desperately try to prove innocence
        - OR accuse others to deflect suspicion
        
        The endless night weighs on everyone. Hope died nights ago.
        Speak with the exhaustion of eternal darkness.
      `,
      
      messages: this.conversationHistory
    });
    
    return this.processResponse(response, leverage);
  }
}
```

### Phase 4: The Living Map (Week 4)
```javascript
// Dynamic intelligence mapping
class IntelligenceMap {
  constructor(canvas) {
    this.canvas = canvas;
    this.nodes = new Map(); // Locations
    this.edges = new Map(); // Connections
    this.decay = 0;
  }
  
  render() {
    // Parchment aesthetic
    this.applyWear();
    
    // Draw with increasing uncertainty
    this.nodes.forEach(node => {
      const age = this.currentNight - node.discovered;
      const opacity = Math.max(0.2, 1 - (age * 0.1));
      
      this.drawNode(node, {
        opacity,
        shake: age * 2, // Older memories shake
        blur: this.decay
      });
    });
    
    // Connections fade or strengthen
    this.edges.forEach(edge => {
      const strength = edge.evidence.length;
      this.drawEdge(edge, {
        style: strength > 3 ? 'solid' : 'dotted',
        width: Math.min(strength, 5)
      });
    });
  }
}
```

## Three New Little Knight Variations

### 1. **The Oath Breaker's Child**
You're not a Bokkenrijder but the child of one who betrayed the Brotherhood. They shrunk you as a message to your father, who watches from normal size but cannot touch you. Every night, you gather evidence to either damn or redeem your father's name. The twist: your father is one of the fairy tale characters, transformed and hidden, and you don't know which one. Each conversation might be with him, neither of you recognizing the other through the curse.

### 2. **The Youngest Recruit**
You were the Brotherhood's newest member, only 12 years old, initiated just before the great betrayal. You knew nothing of their real crimes, thinking it all a grand adventure. The fairy tale magic shrunk you to match your innocence - thumb-sized, like a child's understanding of evil. Now you must navigate between hardened criminals who see you as a liability and fairy tale characters who pity your naive corruption. Your unique position: you remember the faces of every Bokkenrijder, but not their crimes.

### 3. **The Coin Bearer**
You were the Brotherhood's treasurer, carrying their gold in a pouch made from the Ezel's skin. When captured, you swallowed the coins to hide them. The fairy tale curse shrunk you to coin-size, and now you *are* the treasure - if caught and melted down, you'd become 30 pieces of silver. The Ezel (now alive again) seeks you to reclaim his skin, Holle Bolle Gijs hungers to swallow you whole, and every Bokkenrijder wants the fortune you've become. Your body literally grows heavier with guilt, making movement harder as you discover more truths.

## The Dread Atmosphere: Final Design Notes

### Visual Degradation Over Nights
```css
/* CSS for progressive decay */
.night-1 { filter: sepia(10%); }
.night-7 { filter: sepia(30%) contrast(90%); }
.night-13 { filter: sepia(50%) contrast(80%) blur(0.5px); }
.night-31 { filter: sepia(70%) contrast(60%) blur(1px); }
.night-100 { 
  filter: sepia(90%) contrast(40%) blur(2px);
  animation: flicker 3s infinite;
}
```

### Audio Design
- Heartbeat that gets louder each night
- Whispers that might be the wind or might be oaths
- The wooden horse creaking more desperately
- Silence that feels wrong, too heavy

### The Map That Remembers
Your map physically tears where you've been caught lying. Burns where you've accused correctly. Bleeds ink where someone has died. It becomes a record not just of intelligence but of consequences.

### Knowledge as Burden
The more you know, the slower you move. The heavier the truth, the harder to carry. Sometimes forgetting is the only way forward, but what you choose to forget shapes what remains.

---

*"In de nacht zijn alle ruiters klein, maar hun schaduwen reiken tot de maan."*
*(In the night all riders are small, but their shadows reach the moon.)*

**Het Kleine Ruiter - Where Knowledge is Power, and Power is a Curse**
*Designed for those who find comfort in beautiful dread*