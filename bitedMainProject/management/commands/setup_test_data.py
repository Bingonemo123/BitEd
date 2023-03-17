import random

from django.db import transaction
from django.core.management.base import BaseCommand

from tiles.models import Tile

from utils.factories import TileFactory, ProfileFactory

NUM_USERS = 50
NUM_TILES = 50

class Command(BaseCommand):
    help= 'Generates test data'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        Tile.objects.all().delete()

        self.stdout.write('Creating New users...')
        user_inst = []
        for _ in range(NUM_USERS):
            profile_user = ProfileFactory()
            user_inst.append(profile_user)

        for _ in range(NUM_TILES):
            author = random.choice(user_inst)
            tile = TileFactory(author=author)

