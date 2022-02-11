# Generated by Django 4.0.1 on 2022-02-11 19:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_expensereport_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mission',
            old_name='date',
            new_name='endDate',
        ),
        migrations.RemoveField(
            model_name='collaborator',
            name='isValidator',
        ),
        migrations.RemoveField(
            model_name='mission',
            name='amountAdvance',
        ),
        migrations.AddField(
            model_name='mission',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mService', to='main.service'),
        ),
        migrations.AddField(
            model_name='mission',
            name='startDate',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='MissionCollab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amountAdvance', models.FloatField(default=0)),
                ('idCollab', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mcCollab', to='main.collaborator')),
                ('idMission', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mcMission', to='main.mission')),
            ],
            options={
                'unique_together': {('idMission', 'idCollab')},
            },
        ),
    ]
