from django.contrib import admin
from .models import StarredCity
# from .models import CityWeatherData

admin.site.site_header = "Django Weather Admin"
admin.site.site_title = "Django Weather Admin Area"
admin.site.index_title = "Welcome to the Weather Admin Area"

# class CityWeatherInline(admin.TabularInline):
#     model = CityWeatherData
#     extra = 1

class StarredCityAdmin(admin.ModelAdmin):
    fieldsets = [('City', {'fields': ['city_name']}),]

admin.site.register(StarredCity, StarredCityAdmin)
# admin.site.register(StarredCity)
# admin.site.register(CityWeatherData)