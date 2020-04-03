from django.db import models

# Create your models here.

class StarredCity(models.Model):
    city_id = models.CharField(max_length=150, primary_key=True)
    city_name = models.CharField(max_length=100)
    is_home = models.BooleanField(default=False)

    def __str__(self):
        return StarredCity.city_name

    class Meta:
        verbose_name_plural = 'Starred Cities'

# class CityWeatherData(models.Model):
#     city = models.ForeignKey(StarredCity, on_delete=models.CASCADE)
#     current_date = models.DateTimeField(auto_now=True)
#     current_temp = models.DecimalField(max_digits=50, decimal_places=2)
#     current_humidity = models.DecimalField(max_digits=50, decimal_places=2)
#     feels_like = models.DecimalField(max_digits=50, decimal_places=2)
#     todays_min_temp = models.DecimalField(max_digits=50, decimal_places=2)
#     todays_max_temp = models.DecimalField(max_digits=50, decimal_places=2)
#     todays_sunset = models.BigIntegerField()
#     todays_sunrise = models.BigIntegerField()

#     def __str__(self):
#         return self