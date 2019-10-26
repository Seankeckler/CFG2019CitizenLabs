# Generated by Django 2.2.6 on 2019-10-26 20:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('elections', '0036_remove_ballotwebsite_source')]

    operations = [
        migrations.AlterModelOptions(name='precinct', options={}),
        migrations.RemoveField(model_name='precinct', name='mi_sos_id'),
        migrations.AlterField(
            model_name='ballot',
            name='website',
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='ballot',
                to='elections.BallotWebsite',
            ),
        ),
    ]
