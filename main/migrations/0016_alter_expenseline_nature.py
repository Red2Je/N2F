# Generated by Django 4.0 on 2022-02-06 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_expenseline_nature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenseline',
            name='nature',
            field=models.CharField(choices=[('Essence', 'Carburant'), ('Hébergement', 'Hebergement'), ('Repas', 'Repas'), ('Transport', 'Transport'), ('Voyage', 'Voyage'), ('Autre', 'Autre'), ('Achat', 'Achat'), ('Demande d &rsquo avance', 'Demande d &rsquo avance')], max_length=25),
        ),
    ]
