# Generated by Django 4.1.7 on 2023-03-28 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tiles', '0002_remove_tile_children_tile_children'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tile',
            old_name='children',
            new_name='parent',
        ),
    ]
