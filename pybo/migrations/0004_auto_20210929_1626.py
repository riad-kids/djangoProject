# Generated by Django 3.2.7 on 2021-09-29 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0003_answer_auth'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='auth',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='auth',
            new_name='author',
        ),
    ]
