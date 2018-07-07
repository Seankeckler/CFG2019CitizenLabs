# Generated by Django 2.0.7 on 2018-07-07 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('elections', '0010_auto_20180705_1757')]

    operations = [
        migrations.AlterModelOptions(
            name='district', options={'ordering': ['-population']}
        ),
        migrations.AlterModelOptions(
            name='districtcategory',
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'District Categories',
            },
        ),
        migrations.AlterModelOptions(
            name='election', options={'ordering': ['-date']}
        ),
        migrations.AlterField(
            model_name='poll',
            name='ward_number',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
