# Generated by Django 4.0.1 on 2022-01-16 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mission',
            old_name='nae',
            new_name='name',
        ),
    ]