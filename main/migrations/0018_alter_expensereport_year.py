# Generated by Django 4.0 on 2022-02-07 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_expenseline_nature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensereport',
            name='year',
            field=models.IntegerField(default=2020),
        ),
    ]
