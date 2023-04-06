from django.db import models
from django.contrib.auth import get_user_model
from questions.models import Question
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# Create your models here.
TYPES_OF_TILES = (
    ('T', 'Tile/Tag'),
    ('B', 'Block'),
    ('O', 'Official Test'),
    ('S', 'Subject'),
    ('U', 'Organization'), 
    ('K', 'Book'), 
    ('C', 'Chapter'), 
    ('P', 'Page'), 
    ('C', 'Course'), 
    ('R', 'Research Paper'), 
    ('Q', 'Question')

)

BLOCK_MODE_CHOICES  = (
    (1, 'Test'),
    (2, 'Training')
)

BLOCK_SECTOR_CHOICES = (
    (1, 'Private'),
    (2, 'Public')
)

def headline_unique(value):
    if Tile.objects.filter(tile_headline=value).exists():
        raise ValidationError(
            _(f'{value} already Exists'),
            params={'value': value},
        )

class Tile(models.Model):
    # static data
    tile_headline = models.CharField(max_length=128, unique=True) 
    pointer_url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    subtype_of_tile = models.IntegerField(blank=True, null=True)
    img_url = models.URLField(null=True, blank=True)
    author = models.ForeignKey(get_user_model(), 
                               null=True, blank=True,
                                 on_delete=models.SET_NULL)
    type_of_tile_char = models.CharField(max_length=1, choices=TYPES_OF_TILES)
    
    # calculated data
    expected_reward = models.FloatField(null=True, blank=True)
    total_questions = models.IntegerField(blank=True, null=True)
    total_pass = models.IntegerField(default=0)
    total_writes = models.IntegerField(default=0)

    # Relations
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.tile_headline

class WriteRequestData(models.Model):
    requested_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    expected_reward = models.FloatField(null=True, default=1)
    block_mode = models.IntegerField(choices=BLOCK_MODE_CHOICES)
    block_sector =  models.IntegerField(choices=BLOCK_SECTOR_CHOICES)
    timed = models.BooleanField(default=False)
    block_total_questions = models.IntegerField()
    finished = models.BooleanField(default=False)
    finished_at = models.DateTimeField(null=True, blank=True)
    total_correct = models.IntegerField(null=True, blank=True)
    tile_created_from = models.ForeignKey(Tile, null=True, blank=True,  on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


"""Hierarchy
Individual  Question
x Tiles -->      Collection of Question by tiles [Goto: Configuration - Write Random Block based on this tiles]
xx Blocks -->   Random Collection of Questions limited by number [bl]-block limit
                Can be Grouped by tiles [Goto: Configuration - Write specific Block ]
                Example 'Hardest Question on USMLE STEP 2'
xxx Official Test --> Group of Blocks or tiles in Subject; Official Test is like Tiles;
xxxx Subject --> Goto
""" 

# Tiles can be for:
# 1. Individual Question --> 
# 2. For Custom Blocks -->
# 3. For Official Test -->
# 4. For Subjects -->
# 5. For Organization/ University/ -->
