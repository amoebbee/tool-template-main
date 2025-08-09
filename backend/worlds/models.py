"""
World models for The Endless Nights Engine.
Every world begins whole and degrades through observation.
"""

from django.db import models
import uuid
import json


class World(models.Model):
    """A world ready to be witnessed and degraded."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Source information
    source_type = models.CharField(
        max_length=50,
        choices=[
            ('onlyworlds', 'OnlyWorlds Import'),
            ('text', 'Parsed Text'),
            ('manual', 'Manual Creation'),
        ]
    )
    source_reference = models.TextField(blank=True)
    
    # World configuration
    witness_config = models.JSONField(default=dict)
    resource_types = models.JSONField(default=dict)
    degradation_pattern = models.JSONField(default=dict)
    hidden_truth = models.TextField(blank=True)
    
    # OnlyWorlds integration
    onlyworlds_api_key = models.CharField(max_length=100, blank=True)
    onlyworlds_pin = models.CharField(max_length=20, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    times_witnessed = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} (witnessed {self.times_witnessed} times)"


class Location(models.Model):
    """A place that exists until forgotten."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='locations')
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Spatial properties
    size_scale = models.CharField(
        max_length=50,
        choices=[
            ('microscopic', 'Microscopic'),
            ('tiny', 'Tiny'),
            ('small', 'Small'),
            ('human', 'Human Scale'),
            ('large', 'Large'),
            ('vast', 'Vast'),
        ],
        default='human'
    )
    
    # Degradation state
    integrity = models.FloatField(default=1.0)  # 1.0 = pristine, 0.0 = ruins
    color_saturation = models.FloatField(default=1.0)  # Fades over time
    clarity = models.FloatField(default=1.0)  # Becomes harder to perceive
    
    # Connections
    connected_to = models.ManyToManyField('self', blank=True)
    
    # Memory markers
    has_been_witnessed = models.BooleanField(default=False)
    last_witnessed = models.DateTimeField(null=True, blank=True)
    witness_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['name']
    
    def degrade(self, amount=0.01):
        """Things fall apart."""
        self.integrity = max(0, self.integrity - amount)
        self.color_saturation = max(0, self.color_saturation - amount * 0.5)
        self.clarity = max(0, self.clarity - amount * 0.3)
        self.save()
    
    def __str__(self):
        return f"{self.name} (integrity: {self.integrity:.2f})"


class Character(models.Model):
    """A being who exists in the world, with or without agency."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='characters')
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    role = models.CharField(max_length=100, blank=True)
    
    # Agency and power
    has_agency = models.BooleanField(default=True)
    power_level = models.IntegerField(default=5)  # 0=powerless, 10=omnipotent
    is_witness_candidate = models.BooleanField(default=False)
    
    # Current state
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    alive = models.BooleanField(default=True)
    memory_intact = models.FloatField(default=1.0)  # Degrades over time
    
    # Knowledge they possess
    known_truths = models.JSONField(default=list)
    spoken_lies = models.JSONField(default=list)
    
    # LLM personality configuration
    personality_prompt = models.TextField(blank=True)
    speech_pattern = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def forget(self, amount=0.05):
        """Memory degrades."""
        self.memory_intact = max(0, self.memory_intact - amount)
        self.save()
    
    def __str__(self):
        status = "alive" if self.alive else "dead"
        return f"{self.name} ({status}, memory: {self.memory_intact:.2f})"


class Object(models.Model):
    """An item that can be witnessed, carried, or lost."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='world_objects')
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Physical properties
    size = models.CharField(
        max_length=50,
        choices=[
            ('tiny', 'Tiny - fits in palm'),
            ('small', 'Small - can be carried'),
            ('medium', 'Medium - requires effort'),
            ('large', 'Large - immovable'),
        ],
        default='small'
    )
    weight = models.FloatField(default=1.0)  # Knowledge weight
    
    # Resource type
    resource_type = models.CharField(
        max_length=50,
        choices=[
            ('ephemeral', 'Ephemeral (whispers, rumors)'),
            ('physical', 'Physical (marks, scars)'),
            ('binding', 'Binding (oaths, contracts)'),
        ],
        default='physical'
    )
    
    # Location and ownership
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    owned_by = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True)
    
    # State
    condition = models.FloatField(default=1.0)  # 1.0 = perfect, 0.0 = destroyed
    hidden = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['name']
    
    def decay(self, amount=0.02):
        """Objects deteriorate."""
        self.condition = max(0, self.condition - amount)
        self.save()
    
    def __str__(self):
        return f"{self.name} ({self.resource_type}, condition: {self.condition:.2f})"


class Treaty(models.Model):
    """An agreement or rule that governs the world."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='treaties')
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Treaty properties
    parties = models.ManyToManyField(Character, related_name='treaties')
    is_public = models.BooleanField(default=True)
    is_broken = models.BooleanField(default=False)
    
    # Terms
    terms = models.JSONField(default=list)
    consequences = models.TextField(blank=True)
    
    # Degradation
    strength = models.FloatField(default=1.0)  # Weakens over time
    
    created_at = models.DateTimeField(auto_now_add=True)
    broken_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Treaties"
    
    def weaken(self, amount=0.03):
        """Agreements lose their power."""
        self.strength = max(0, self.strength - amount)
        if self.strength == 0:
            self.is_broken = True
        self.save()
    
    def __str__(self):
        status = "broken" if self.is_broken else f"strength: {self.strength:.2f}"
        return f"{self.name} ({status})"