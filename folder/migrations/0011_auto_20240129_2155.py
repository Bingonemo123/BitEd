# Generated by Django 4.2.5 on 2024-01-30 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folder', '0010_auto_20240129_2139'),
    ]

    operations = [
        migrations.RenameField('Folder', 'tile_headline', 'name'),
        migrations.RenameField('Folder', 'subtype_of_tile', 'subtype'),
        migrations.RenameField('Folder', 'type_of_tile_char', 'type'),
        migrations.RenameField('WriteRequestData', 'tile_created_from', 
                               'folder_created_from'),
    ]
