# Generated by Django 3.0.4 on 2020-03-30 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0004_cityweatherdata_starredcity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='starredcity',
            name='city_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
