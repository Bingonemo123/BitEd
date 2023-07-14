# Generated by Django 4.2.2 on 2023-06-17 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writing', '0003_alter_useranswer_answer_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='answer_state',
            field=models.IntegerField(choices=[(1, 'Seen'), (2, 'Selected'), (8, 'Submitted'), (16, 'Correct'), (32, 'Timeout')], default=0),
        ),
    ]