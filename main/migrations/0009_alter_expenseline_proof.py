# Generated by Django 4.0 on 2022-01-16 21:33

from django.db import migrations, models
import main.dataValidator


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_expenseline_proof'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenseline',
            name='proof',
            field=models.FileField(upload_to='proofs', validators=[main.dataValidator.validate_file_type]),
        ),
    ]
