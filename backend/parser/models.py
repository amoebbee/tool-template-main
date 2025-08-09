"""
Parser models for transforming text into witness-able worlds.
"""

from django.db import models
import uuid


class ParseSession(models.Model):
    """A session for parsing source material into a world."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Source information
    source_file = models.FileField(upload_to='parse_sources/', null=True, blank=True)
    source_text = models.TextField(blank=True)
    source_url = models.URLField(blank=True)
    source_type = models.CharField(
        max_length=50,
        choices=[
            ('pdf', 'PDF Document'),
            ('txt', 'Plain Text'),
            ('html', 'HTML/Web Page'),
            ('docx', 'Word Document'),
            ('epub', 'EPUB Book'),
            ('manual', 'Manual Input'),
        ]
    )
    
    # Parsing configuration
    world_name = models.CharField(max_length=200)
    witness_type = models.CharField(
        max_length=50,
        choices=[
            ('auto', 'Auto-detect witness'),
            ('smallest', 'Find smallest character'),
            ('observer', 'Find pure observer'),
            ('child', 'Find child character'),
            ('animal', 'Find animal observer'),
            ('object', 'Create object witness'),
        ],
        default='auto'
    )
    
    # Parsing stages
    extraction_complete = models.BooleanField(default=False)
    entities_identified = models.BooleanField(default=False)
    witness_selected = models.BooleanField(default=False)
    resources_defined = models.BooleanField(default=False)
    world_created = models.BooleanField(default=False)
    
    # Extracted data
    extracted_text = models.TextField(blank=True)
    entities = models.JSONField(default=dict)
    witness_config = models.JSONField(default=dict)
    resource_mapping = models.JSONField(default=dict)
    
    # Results
    world = models.ForeignKey('worlds.World', on_delete=models.SET_NULL, null=True, blank=True)
    error_log = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        status = "complete" if self.world_created else "in progress"
        return f"Parse: {self.world_name} ({status})"


class ExtractedEntity(models.Model):
    """An entity extracted from source material."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ParseSession, on_delete=models.CASCADE, related_name='extracted_entities')
    
    # Entity information
    entity_type = models.CharField(
        max_length=50,
        choices=[
            ('character', 'Character'),
            ('location', 'Location'),
            ('object', 'Object'),
            ('event', 'Event'),
            ('concept', 'Concept'),
            ('treaty', 'Treaty/Agreement'),
        ]
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Extracted properties
    properties = models.JSONField(default=dict)
    mentions = models.JSONField(default=list)  # Where in text it appears
    relationships = models.JSONField(default=list)  # Connections to other entities
    
    # Analysis
    power_level = models.IntegerField(null=True, blank=True)  # For characters
    size_scale = models.CharField(max_length=50, blank=True)  # For locations/objects
    importance_score = models.FloatField(default=0.5)  # 0-1 scale
    
    # Witness candidacy
    is_witness_candidate = models.BooleanField(default=False)
    witness_score = models.FloatField(default=0.0)  # How good a witness
    
    class Meta:
        ordering = ['entity_type', 'name']
    
    def __str__(self):
        return f"{self.entity_type}: {self.name}"


class ParseTemplate(models.Model):
    """Templates for parsing specific types of sources."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Template configuration
    source_type = models.CharField(max_length=50)
    extraction_rules = models.JSONField(default=dict)
    entity_patterns = models.JSONField(default=dict)
    witness_criteria = models.JSONField(default=dict)
    resource_mapping = models.JSONField(default=dict)
    
    # Usage
    times_used = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"Template: {self.name}"