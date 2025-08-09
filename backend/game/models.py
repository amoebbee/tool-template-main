"""
Game models for The Endless Nights Engine.
Where witnesses carry the weight of knowledge through degrading worlds.
"""

from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime


class GameSession(models.Model):
    """A witness's journey through an endless night."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Player and world
    player = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anonymous_id = models.CharField(max_length=100, blank=True)  # For anonymous play
    world = models.ForeignKey('worlds.World', on_delete=models.CASCADE)
    
    # Witness configuration
    witness_name = models.CharField(max_length=200)
    witness_size = models.CharField(max_length=50, default='thumb')
    witness_mount = models.CharField(max_length=100, blank=True)  # What they ride/use
    
    # Current state
    current_location = models.ForeignKey('worlds.Location', on_delete=models.SET_NULL, null=True)
    night_count = models.IntegerField(default=1)
    total_weight = models.FloatField(default=0.0)
    movement_speed = models.FloatField(default=1.0)
    
    # Degradation tracking
    world_entropy = models.FloatField(default=0.0)  # 0=pristine, 1=ruins
    text_degradation = models.FloatField(default=0.0)
    color_loss = models.FloatField(default=0.0)
    
    # Session metadata
    started_at = models.DateTimeField(auto_now_add=True)
    last_action_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Map state (JSON for flexibility)
    map_tears = models.JSONField(default=list)  # Locations of tears
    map_burns = models.JSONField(default=list)  # Locations of burns
    map_blood = models.JSONField(default=list)  # Locations of blood
    
    class Meta:
        ordering = ['-last_action_at']
    
    def advance_night(self):
        """The night continues, everything degrades."""
        self.night_count += 1
        self.world_entropy = min(1.0, self.world_entropy + 0.01)
        self.text_degradation = min(1.0, self.text_degradation + 0.02)
        self.color_loss = min(1.0, self.color_loss + 0.015)
        self.save()
    
    def add_weight(self, amount):
        """Knowledge has physical weight."""
        self.total_weight += amount
        self.movement_speed = 1.0 / (1 + (self.total_weight * 0.1))
        self.save()
    
    def __str__(self):
        return f"{self.witness_name} in {self.world.name} (Night {self.night_count})"


class Knowledge(models.Model):
    """A piece of information with weight."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='knowledge')
    
    # Knowledge properties
    knowledge_type = models.CharField(
        max_length=50,
        choices=[
            ('whisper', 'Whisper (Ephemeral)'),
            ('mark', 'Mark (Physical)'),
            ('oath', 'Oath (Binding)'),
        ]
    )
    content = models.TextField()
    source = models.CharField(max_length=200, blank=True)  # Who/what provided it
    
    # Weight and burden
    base_weight = models.FloatField(default=1.0)
    truth_multiplier = models.FloatField(default=1.0)  # Terrible truths weigh more
    personal_multiplier = models.FloatField(default=1.0)  # Personal connections add weight
    total_weight = models.FloatField(default=1.0)
    
    # State
    is_truth = models.BooleanField(default=True)
    is_terrible = models.BooleanField(default=False)
    involves_self = models.BooleanField(default=False)
    has_been_shared = models.BooleanField(default=False)
    
    # Location and time
    discovered_at = models.ForeignKey('worlds.Location', on_delete=models.SET_NULL, null=True)
    discovered_time = models.DateTimeField(auto_now_add=True)
    night_discovered = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['-discovered_time']
    
    def calculate_weight(self):
        """Calculate the true weight of this knowledge."""
        weight = self.base_weight
        
        if self.is_terrible:
            weight *= 2.0
        
        if self.involves_self:
            weight *= 2.0
        
        if not self.is_truth:
            weight *= 0.5  # Lies are lighter but still burden
        
        self.total_weight = weight
        self.save()
        return weight
    
    def __str__(self):
        return f"{self.knowledge_type}: {self.content[:50]}... (weight: {self.total_weight:.1f})"


class Conversation(models.Model):
    """A dialogue with a character in the degrading world."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='conversations')
    character = models.ForeignKey('worlds.Character', on_delete=models.CASCADE)
    location = models.ForeignKey('worlds.Location', on_delete=models.SET_NULL, null=True)
    
    # Conversation state
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    night_occurred = models.IntegerField()
    
    # Degradation affects conversation
    text_clarity = models.FloatField(default=1.0)  # How clear the text appears
    response_coherence = models.FloatField(default=1.0)  # How coherent responses are
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Conversation with {self.character.name} (Night {self.night_occurred})"


class Message(models.Model):
    """A single message in a conversation."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    
    # Message content
    speaker = models.CharField(
        max_length=50,
        choices=[
            ('witness', 'Witness'),
            ('character', 'Character'),
            ('narrator', 'Narrator'),
        ]
    )
    original_content = models.TextField()  # Original, undegraded
    degraded_content = models.TextField()  # What actually appears
    
    # Degradation level when sent
    degradation_level = models.FloatField(default=0.0)
    
    # Knowledge gained
    knowledge_gained = models.ForeignKey(Knowledge, on_delete=models.SET_NULL, null=True, blank=True)
    
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['sent_at']
    
    def degrade_text(self, level):
        """Apply degradation to the message text."""
        import re
        import random
        
        text = self.original_content
        
        if level < 0.1:
            self.degraded_content = text
        elif level < 0.3:
            # Remove adjectives
            self.degraded_content = re.sub(r'\b(very|quite|rather|really|extremely)\b', '', text)
        elif level < 0.5:
            # Start losing vowels
            self.degraded_content = ''.join(
                c if random.random() > level or c not in 'aeiou' else '·' 
                for c in text
            )
        elif level < 0.7:
            # Fragment into pieces
            words = text.split()
            self.degraded_content = ' '.join(w[:len(w)//2] + '...' for w in words)
        else:
            # Only shadows remain
            self.degraded_content = '█' * (len(text) // 3)
        
        self.degradation_level = level
        self.save()
    
    def __str__(self):
        return f"{self.speaker}: {self.original_content[:50]}..."


class Discovery(models.Model):
    """A significant discovery that changes the world."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='discoveries')
    
    # Discovery details
    discovery_type = models.CharField(
        max_length=50,
        choices=[
            ('truth', 'Hidden Truth'),
            ('death', 'Character Death'),
            ('betrayal', 'Betrayal'),
            ('treaty_broken', 'Treaty Broken'),
            ('location_lost', 'Location Lost'),
        ]
    )
    description = models.TextField()
    
    # Impact
    world_impact = models.TextField()  # How it changed the world
    map_impact = models.CharField(
        max_length=50,
        choices=[
            ('tear', 'Tore the Map'),
            ('burn', 'Burned the Map'),
            ('blood', 'Bloodied the Map'),
            ('none', 'No Map Impact'),
        ],
        default='none'
    )
    impact_location = models.JSONField(default=dict)  # Coordinates on map
    
    # When
    discovered_at = models.DateTimeField(auto_now_add=True)
    night_discovered = models.IntegerField()
    
    class Meta:
        ordering = ['-discovered_at']
    
    def __str__(self):
        return f"{self.discovery_type}: {self.description[:50]}..."