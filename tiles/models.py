from django.db import models
from django.contrib.auth import get_user_model
from home_page_tiles.models import HomePageTile
# Create your models here.

BLOCK_MODE_CHOICES  = (
    (1, 'Test'),
    (2, 'Training')
)

BLOCK_SECTOR_CHOICES = (
    (1, 'Private'),
    (2, 'Public')
)

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
    tile_created_from = models.ForeignKey(HomePageTile, null=True, blank=True,  on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
