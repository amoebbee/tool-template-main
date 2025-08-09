"""
LLM models for character personalities and world intelligence.
Characters remember, but pretend to forget.
"""

from django.db import models
import uuid


class PersonalityTemplate(models.Model):
    """A template for character personalities."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Base personality
    base_prompt = models.TextField()
    speech_patterns = models.JSONField(default=list)
    vocabulary_level = models.CharField(
        max_length=50,
        choices=[
            ('simple', 'Simple'),
            ('normal', 'Normal'),
            ('eloquent', 'Eloquent'),
            ('archaic', 'Archaic'),
            ('broken', 'Broken'),
        ],
        default='normal'
    )
    
    # Behavioral traits
    truthfulness = models.FloatField(default=0.5)  # 0=always lies, 1=always truth
    memory_quality = models.FloatField(default=0.8)  # How well they remember
    paranoia = models.FloatField(default=0.3)  # How suspicious they are
    despair = models.FloatField(default=0.2)  # How hopeless they are
    
    # Degradation behavior
    memory_decay_rate = models.FloatField(default=0.01)
    speech_decay_rate = models.FloatField(default=0.02)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"Personality: {self.name}"


class CharacterMemory(models.Model):
    """What a character remembers (or pretends to forget)."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    character = models.ForeignKey('worlds.Character', on_delete=models.CASCADE, related_name='memories')
    
    # Memory content
    memory_type = models.CharField(
        max_length=50,
        choices=[
            ('fact', 'Fact'),
            ('conversation', 'Conversation'),
            ('observation', 'Observation'),
            ('feeling', 'Feeling'),
            ('secret', 'Secret'),
        ]
    )
    content = models.TextField()
    
    # Memory state
    clarity = models.FloatField(default=1.0)  # How clear the memory is
    accessibility = models.FloatField(default=1.0)  # How easily recalled
    is_suppressed = models.BooleanField(default=False)  # Actively hiding it
    is_false = models.BooleanField(default=False)  # False memory
    
    # Metadata
    formed_at = models.DateTimeField(auto_now_add=True)
    last_recalled = models.DateTimeField(null=True, blank=True)
    recall_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-formed_at']
    
    def decay(self, amount=0.01):
        """Memories fade."""
        self.clarity = max(0, self.clarity - amount)
        self.accessibility = max(0, self.accessibility - amount * 2)
        self.save()
    
    def __str__(self):
        return f"{self.character.name}'s {self.memory_type}: {self.content[:50]}..."


class ConversationContext(models.Model):
    """Context for generating character responses."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.OneToOneField('game.Conversation', on_delete=models.CASCADE)
    
    # Context elements
    character_state = models.JSONField(default=dict)  # Current mental/emotional state
    world_state = models.JSONField(default=dict)  # Relevant world conditions
    relationship_state = models.JSONField(default=dict)  # Relationship with witness
    
    # Conversation parameters
    degradation_level = models.FloatField(default=0.0)
    coherence_target = models.FloatField(default=1.0)
    truth_tendency = models.FloatField(default=0.5)
    
    # Memory access
    accessible_memories = models.ManyToManyField(CharacterMemory)
    suppressed_topics = models.JSONField(default=list)
    
    # Generated personality
    active_prompt = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def generate_prompt(self):
        """Generate the active prompt for this conversation."""
        character = self.conversation.character
        night = self.conversation.night_occurred
        
        prompt = f"""You are {character.name} in a world that has been through {night} endless nights.
        
Your memories are {character.memory_intact * 100:.0f}% intact.
The world is {self.conversation.session.world_entropy * 100:.0f}% degraded.

{character.personality_prompt}

Speech clarity: {self.coherence_target * 100:.0f}%
Truthfulness: {self.truth_tendency * 100:.0f}%

Remember: You exist in a degrading world. Act accordingly.
Sometimes you forget. Sometimes you pretend to forget.
The difference doesn't matter anymore."""
        
        self.active_prompt = prompt
        self.save()
        return prompt
    
    def __str__(self):
        return f"Context for conversation with {self.conversation.character.name}"


class LLMProvider(models.Model):
    """Configuration for LLM providers."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    provider_type = models.CharField(
        max_length=50,
        choices=[
            ('anthropic', 'Anthropic'),
            ('openai', 'OpenAI'),
            ('local', 'Local Model'),
        ]
    )
    
    # Configuration
    api_key = models.CharField(max_length=200, blank=True)
    endpoint = models.URLField(blank=True)
    model_name = models.CharField(max_length=100)
    
    # Parameters
    temperature = models.FloatField(default=0.7)
    max_tokens = models.IntegerField(default=500)
    
    # Usage
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.provider_type})"