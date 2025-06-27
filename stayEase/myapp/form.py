from django import forms
from myapp.models import Property,Region,City
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = (
            'name',
            'type',
            'beds',
            'bath',
            'wi_fi',
            'pool',
            'kitchen',
            'main_photo',
            'bed_photo',
            'bath_photo',
            'pool_photo',
            'rent_type',
            'rent_amount',
            'region',
            'city',
            'address',
            'posted_by',
            'is_active',
            'status',
            'description',
            'review_star',
            'review_comment',
            
        )
        
        
class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = [
            'name',
        ]
        widgets = {
            'name': forms.TextInput(
                attrs = {'class':'form-control'}
            )
        }
        

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = [
            'region',
            'name'
        ]
        widgets = {
            'name': forms.TextInput(
                attrs = {'class':'form-control'}
            ),
             'region': forms.Select(
                attrs = {'class':'form-control'}
            )
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2'
        ]
        
        widgets = {
            'username': forms.TextInput(
                attrs={'class':'form-control'}
            )
        }