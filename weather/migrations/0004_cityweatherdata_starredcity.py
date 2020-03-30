# Generated by Django 3.0.4 on 2020-03-30 01:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('weather', '0003_auto_20200329_1759'),
    ]

    operations = [
        migrations.CreateModel(
            name='StarredCity',
            fields=[
                ('city_id', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('city_name', models.CharField(max_length=100)),
                ('state', models.CharField(default=None, max_length=15)),
                ('is_home', models.BooleanField(default=False)),
                ('temp', models.IntegerField(default=None)),
                ('icon', models.CharField(default=None, max_length=25)),
            ],
            options={
                'verbose_name_plural': 'Starred Cities',
            },
        ),
        migrations.CreateModel(
            name='CityWeatherData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_date', models.DateTimeField(auto_now=True)),
                ('current_temp', models.DecimalField(decimal_places=2, max_digits=50)),
                ('current_humidity', models.DecimalField(decimal_places=2, max_digits=50)),
                ('feels_like', models.DecimalField(decimal_places=2, max_digits=50)),
                ('todays_min_temp', models.DecimalField(decimal_places=2, max_digits=50)),
                ('todays_max_temp', models.DecimalField(decimal_places=2, max_digits=50)),
                ('todays_sunset', models.BigIntegerField()),
                ('todays_sunrise', models.BigIntegerField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.StarredCity')),
            ],
        ),
    ]
