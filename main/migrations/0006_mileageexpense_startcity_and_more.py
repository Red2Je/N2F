# Generated by Django 4.0 on 2022-02-16 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_advance_validorcommentary_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mileageexpense',
            name='startCity',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='advance',
            name='validorCommentary',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='refundrequest',
            name='validorCommentary',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
