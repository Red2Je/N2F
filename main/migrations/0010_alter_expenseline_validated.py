# Generated by Django 4.0 on 2022-01-20 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_expenseline_proof'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenseline',
            name='validated',
            field=models.BooleanField(default=False),
        ),
    ]