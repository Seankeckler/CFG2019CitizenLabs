# Generated by Django 2.0.7 on 2018-07-13 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('elections', '0010_auto_20180713_1704')]

    operations = [
        migrations.AlterField(
            model_name='ballotwebsite',
            name='source',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='ballotwebsite',
            name='valid',
            field=models.NullBooleanField(),
        ),
    ]
