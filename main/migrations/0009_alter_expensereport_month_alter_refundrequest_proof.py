# Generated by Django 4.0.1 on 2022-02-16 18:22

from django.db import migrations, models
import main.dataValidator


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_expensereport_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensereport',
            name='month',
            field=models.CharField(choices=[('Janvier', 'Janvier'), ('Fevrier', 'Fevrier'), ('Mars', 'Mars'), ('Avril', 'Avril'), ('Mai', 'Mai'), ('Juin', 'Juin'), ('Juillet', 'Juillet'), ('Aout', 'Aout'), ('Septembre', 'Septembre'), ('Octobre', 'Octobre'), ('Novembre', 'Novembre'), ('Decembre', 'Decembre')], max_length=20),
        ),
        migrations.AlterField(
            model_name='refundrequest',
            name='proof',
            field=models.FileField(upload_to='proofs', validators=[main.dataValidator.validate_file_type]),
        ),
    ]
