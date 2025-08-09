"""
Management command to load the Efteling reference world.
Het Kleine Ruiter rides through the Bokkenrijders trial.
"""

from django.core.management.base import BaseCommand
from worlds.models import World, Location, Character, Object as WorldObject, Treaty
import json


class Command(BaseCommand):
    help = 'Load the Efteling reference world'
    
    def handle(self, *args, **options):
        self.stdout.write("Loading Efteling: Het Kleine Ruiter...")
        
        # Create the world
        world = self._create_world()
        
        # Create locations
        locations = self._create_locations(world)
        
        # Create characters
        characters = self._create_characters(world, locations)
        
        # Create objects
        objects = self._create_objects(world, locations)
        
        # Create treaties
        treaties = self._create_treaties(world, characters)
        
        self.stdout.write(self.style.SUCCESS(
            f"Efteling world loaded: {len(characters)} characters, "
            f"{len(locations)} locations, {len(objects)} objects"
        ))
    
    def _create_world(self) -> World:
        """Create the Efteling world."""
        world = World.objects.create(
            name="Efteling: Het Kleine Ruiter",
            description=(
                "The theme park where fairy tales come to trial. "
                "Het Kleine Ruiter, a thumb-sized wooden boy on a red horse, "
                "witnesses the Bokkenrijders' judgment while the park itself stands accused."
            ),
            source_type='manual',
            source_reference='Efteling Theme Park / Bokkenrijders legend',
            witness_config={
                'name': 'Het Kleine Ruiter',
                'size': 'thumb',
                'mount': 'red wooden horse',
                'starting_location': 'cobblestones',
                'voice': 'tiny wooden whisper',
            },
            resource_types={
                'ephemeral': 'fairy tale whispers',
                'physical': 'carousel marks',
                'binding': 'theme park magic',
            },
            degradation_pattern={
                'stages': ['color', 'music', 'laughter', 'memory', 'magic'],
                'speed': 1.0,
                'entropy_rate': 0.01,
                'special': 'carousel slows with each night',
            },
            hidden_truth="The park itself is on trial for keeping stories captive",
        )
        return world
    
    def _create_locations(self, world: World) -> list:
        """Create Efteling locations."""
        locations = []
        
        # Main areas
        courtyard = Location.objects.create(
            world=world,
            name="The Trial Courtyard",
            description=(
                "Where the Bokkenrijders face judgment. Cobblestones worn smooth "
                "by centuries of verdicts. The gallows cast shadows that never match the sun."
            ),
            size_scale='large',
        )
        locations.append(courtyard)
        
        carousel = Location.objects.create(
            world=world,
            name="The Carousel",
            description=(
                "Anton Hoeck's creation spins eternally, its painted horses "
                "frozen in gallop. Each revolution takes slightly longer than the last."
            ),
            size_scale='human',
        )
        locations.append(carousel)
        
        fairytale_forest = Location.objects.create(
            world=world,
            name="Sprookjesbos (Fairytale Forest)",
            description=(
                "Where stories live in miniature houses. Each tale trapped "
                "in endless retelling, the characters aware but unable to change their endings."
            ),
            size_scale='large',
        )
        locations.append(fairytale_forest)
        
        beneath = Location.objects.create(
            world=world,
            name="Beneath the Cobblestones",
            description=(
                "The small spaces where Het Kleine Ruiter can travel. "
                "Cracks in the theme park's perfect facade where truth seeps through."
            ),
            size_scale='tiny',
        )
        locations.append(beneath)
        
        # Connect locations
        courtyard.connected_to.add(carousel, fairytale_forest, beneath)
        carousel.connected_to.add(courtyard)
        fairytale_forest.connected_to.add(courtyard)
        beneath.connected_to.add(courtyard, carousel, fairytale_forest)
        
        return locations
    
    def _create_characters(self, world: World, locations: list) -> list:
        """Create Efteling characters."""
        characters = []
        courtyard = locations[0]
        carousel = locations[1]
        
        # The Judge
        judge = Character.objects.create(
            world=world,
            name="The Judge",
            description=(
                "Presides over the eternal trial. His wig is made of "
                "carousel music sheets. Never blinks, even when pronouncing death."
            ),
            role="Authority",
            has_agency=True,
            power_level=9,
            current_location=courtyard,
            personality_prompt=(
                "You are the Judge in an endless trial. You speak in verdicts "
                "and precedents. Every word is final, yet nothing ever ends."
            ),
        )
        characters.append(judge)
        
        # Hugo van der Goeslaan (Bokkenrijder leader)
        hugo = Character.objects.create(
            world=world,
            name="Hugo van der Goeslaan",
            description=(
                "Leader of the Bokkenrijders, eternally on trial. "
                "His testimony changes slightly each night, but the verdict never does."
            ),
            role="The Accused",
            has_agency=False,
            power_level=3,
            current_location=courtyard,
            personality_prompt=(
                "You are Hugo, leader of thieves, forever defending yourself. "
                "You remember different crimes each night but forget your innocence."
            ),
        )
        characters.append(hugo)
        
        # Anton Hoeck (Carousel creator)
        anton = Character.objects.create(
            world=world,
            name="Anton Hoeck",
            description=(
                "Created the carousel and Het Kleine Ruiter. His painted hands "
                "still move as if carving, though he holds no tools. Knows why the horses slow."
            ),
            role="The Creator",
            has_agency=True,
            power_level=6,
            current_location=carousel,
            personality_prompt=(
                "You created beauty that became a prison. You speak in "
                "woodworking metaphors and remember when the paint was wet."
            ),
        )
        characters.append(anton)
        
        # Het Kleine Ruiter (potential witness, but exists as observer)
        kleine_ruiter = Character.objects.create(
            world=world,
            name="Het Kleine Ruiter (Echo)",
            description=(
                "A reflection of the witness. What Het Kleine Ruiter might say "
                "if wooden boys could speak. Thumb-sized, eternally riding."
            ),
            role="The Witness Echo",
            has_agency=False,
            power_level=0,
            is_witness_candidate=True,
            current_location=carousel,
            personality_prompt=(
                "You are what a wooden boy might think. You speak in "
                "splinters and paint chips. Your voice is the size of a thimble."
            ),
        )
        characters.append(kleine_ruiter)
        
        # Holle Bolle Gijs
        gijs = Character.objects.create(
            world=world,
            name="Holle Bolle Gijs",
            description=(
                "The talking trash can who swallows everything. 'Papier hier!' "
                "he calls eternally. Knows all secrets because everyone throws them away."
            ),
            role="The Secret Keeper",
            has_agency=False,
            power_level=2,
            current_location=courtyard,
            personality_prompt=(
                "You hunger for paper and secrets. You speak only in "
                "requests for trash and occasionally burp up terrible truths."
            ),
        )
        characters.append(gijs)
        
        return characters
    
    def _create_objects(self, world: World, locations: list) -> list:
        """Create Efteling objects."""
        objects = []
        courtyard = locations[0]
        carousel = locations[1]
        
        # The Verdict Scroll
        verdict = WorldObject.objects.create(
            world=world,
            name="The Verdict Scroll",
            description=(
                "Always unfurling, never fully read. The ink rewrites itself "
                "each dawn, but the judgment remains: guilty."
            ),
            size='small',
            weight=5.0,
            resource_type='binding',
            location=courtyard,
        )
        objects.append(verdict)
        
        # Carousel Music Box
        music_box = WorldObject.objects.create(
            world=world,
            name="The Carousel's Music Box",
            description=(
                "Plays 'Het Kleine Ruiter Rijdt' increasingly slowly. "
                "Each note weighs more than the last."
            ),
            size='medium',
            weight=3.0,
            resource_type='ephemeral',
            location=carousel,
        )
        objects.append(music_box)
        
        # Paint Chips
        paint = WorldObject.objects.create(
            world=world,
            name="Paint Chips from the Horses",
            description=(
                "Flakes of color that fall like snow. Each chip remembers "
                "the child who once rode that horse."
            ),
            size='tiny',
            weight=0.1,
            resource_type='physical',
            location=carousel,
        )
        objects.append(paint)
        
        # The Guest Book
        guest_book = WorldObject.objects.create(
            world=world,
            name="The Eternal Guest Book",
            description=(
                "Every visitor's name appears, but in reverse chronological order. "
                "The first page shows tomorrow's guests."
            ),
            size='medium',
            weight=2.0,
            resource_type='binding',
            location=courtyard,
        )
        objects.append(guest_book)
        
        return objects
    
    def _create_treaties(self, world: World, characters: list) -> list:
        """Create Efteling treaties and agreements."""
        treaties = []
        judge = characters[0]
        hugo = characters[1]
        
        # The Eternal Trial Agreement
        trial = Treaty.objects.create(
            world=world,
            name="The Eternal Trial Agreement",
            description=(
                "The trial must continue until innocence is proven. "
                "But innocence was never defined."
            ),
            is_public=True,
            terms=[
                "The accused must testify each dawn",
                "The judge must listen but never hear",
                "The verdict must be pronounced at dusk",
                "The execution must be postponed until tomorrow",
            ],
        )
        trial.parties.add(judge, hugo)
        treaties.append(trial)
        
        # The Theme Park Compact
        compact = Treaty.objects.create(
            world=world,
            name="The Theme Park Compact",
            description=(
                "All attractions must perform their purpose eternally. "
                "Joy is mandatory. Wonder is enforced."
            ),
            is_public=False,
            terms=[
                "Stories must repeat without variation",
                "Characters must smile when observed",
                "Magic must appear effortless",
                "No one may mention the weariness",
            ],
        )
        compact.parties.add(*characters)
        treaties.append(compact)
        
        return treaties