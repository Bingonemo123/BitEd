from django.db import models
from django.contrib.auth.models import User
from questions.models import Question

# Create your models here.
"""Hierarchy
Individual  Question
x Tags -->      Collection of Question by tag [Goto: Configuration - Write Random Block based on this tag]
xx Blocks -->   Random Collection of Questions limited by number [bl]-block limit
                Can be Grouped by tag [Goto: Configuration - Write specific Block ]
                Example 'Hardest Question on USMLE STEP 2'
xxx Official Test --> Group of Blocks or tags in Subject; Official Test is like Tag;
xxxx Subject --> Goto



""" 
TYPES_OF_TILES = (
    ('T', 'Tag'),
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
# Tiles can be for:
# 1. Individual Question --> 
# 2. For Custom Blocks -->
# 3. For Official Test -->
# 4. For Subjects -->
# 5. For Organization/ University/ -->


class HomePageTile(models.Model):
    # static data
    tile_headline = models.CharField(max_length=128) 
    pointer_url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    subtype_of_tile = models.IntegerField(blank=True, null=True)
    img_url = models.URLField(null=True, blank=True)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    type_of_tile_char = models.CharField(max_length=1, choices=TYPES_OF_TILES)
    
    # calculated data
    json_data_tags = models.JSONField(default=dict)
    expected_reward = models.FloatField(null=True, blank=True)
    total_questions = models.IntegerField(blank=True, null=True)
    total_pass = models.IntegerField(default=0)
    total_writes = models.IntegerField(default=0)

    # Relations
    children = models.ManyToManyField('self')
    questions = models.ManyToManyField(Question)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.tile_headline


