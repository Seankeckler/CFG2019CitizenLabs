# Generated by Django 2.0.7 on 2018-07-07 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('elections', '0011_auto_20180707_1805')]

    operations = [
        migrations.AddField(
            model_name='election',
            name='active',
            field=models.BooleanField(default=False),
        )
    ]
