from django.forms import ModelForm, TextInput, forms
from .models import StarredCity

class CityForm(ModelForm):
    class Meta:
        model = StarredCity 
        fields = ['city_name']
        widgets = {'city_name' : TextInput(attrs={'style': 'width: 260px', 'class' : 'input', 'placeholder' : '"Bend"  "Bend, OR"  "Bend, Oregon"'})}

