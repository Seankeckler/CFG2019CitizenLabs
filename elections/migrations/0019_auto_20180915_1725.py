# Generated by Django 2.0.8 on 2018-09-15 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('elections', '0018_auto_20180807_2318')]

    operations = [
        migrations.RenameField(
            model_name='ballotwebsite', old_name='fetched', new_name='last_fetch'
        ),
        migrations.RemoveField(model_name='ballotwebsite', name='created'),
        migrations.RemoveField(model_name='ballotwebsite', name='modified'),
        migrations.AddField(
            model_name='ballotwebsite',
            name='last_fetch_with_ballot',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='ballotwebsite',
            name='last_fetch_with_precent',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='ballotwebsite',
            name='refetch_weight',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='ballotwebsite',
            name='table_count',
            field=models.IntegerField(default=-1),
        ),
    ]
