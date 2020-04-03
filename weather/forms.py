from django.forms import ModelForm, TextInput, forms
from .models import StarredCity

class CityForm(ModelForm):
    class Meta:
        model = StarredCity 
        fields = ['city_name']
        widgets = {'city_name' : TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'})}

