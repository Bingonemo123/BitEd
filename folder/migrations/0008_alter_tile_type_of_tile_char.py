# Generated by Django 4.2 on 2023-04-27 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folder', '0007_alter_tile_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tile',
            name='type_of_tile_char',
            field=models.CharField(choices=[('T', 'Topic'), ('B', 'Block'), ('O', 'Official Test'), ('S', 'Subject'), ('U', 'Organization'), ('K', 'Book'), ('C', 'Chapter'), ('P', 'Page'), ('C', 'Course'), ('R', 'Research Paper'), ('Q', 'Question')], max_length=1),
        ),
    ]
