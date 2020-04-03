# Generated by Django 3.0.4 on 2020-04-02 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0007_auto_20200329_2310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='starredcity',
            name='id',
        ),
        migrations.AddField(
            model_name='starredcity',
            name='city_id',
            field=models.CharField(default=1, max_length=150, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='starredcity',
            name='is_home',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='CityWeatherData',
        ),
    ]
