# Generated by Django 3.0.4 on 2020-03-30 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0005_auto_20200329_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='starredcity',
            name='city_id',
            field=models.CharField(max_length=150, primary_key=True, serialize=False),
        ),
    ]