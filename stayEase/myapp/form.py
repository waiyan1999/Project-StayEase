from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, CustomerProfile, AgencyProfile, OwnerProfile, Property, Review, Region, City,Inquiry

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='CUSTOMER'
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'phone', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'phone')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CustomerProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )
    
    class Meta:
        model = CustomerProfile
        fields = ('customer_name', 'date_of_birth', 'profile_photo', 'address')
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AgencyProfileForm(forms.ModelForm):
    class Meta:
        model = AgencyProfile
        fields = ('agency_name', 'contact_person', 'license_number', 'address', 'website', 'agency_logo')
        widgets = {
            'agency_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'hello'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'agency_logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = OwnerProfile
        fields = ('owner_name', 'address', 'owner_photo')
        widgets = {
            'owner_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'owner_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = (
            'name', 'property_type', 'description', 'beds', 'baths', 
            'has_wifi', 'has_pool', 'has_kitchen', 'area_sqft', 
            'rent_type', 'rent_amount', 'security_deposit',
            'region', 'city', 'address', 'latitude', 'longitude',
            'status', 'is_featured','primary_image','image_caption'
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'beds': forms.NumberInput(attrs={'class': 'form-control'}),
            'baths': forms.NumberInput(attrs={'class': 'form-control'}),
            'area_sqft': forms.NumberInput(attrs={'class': 'form-control'}),
            'rent_type': forms.Select(attrs={'class': 'form-control'}),
            'rent_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'security_deposit': forms.NumberInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'primary_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_caption': forms.TextInput(attrs={'class': 'form-control'})
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Set empty label for selects
    #     self.fields['region'].empty_label = "Select Region"
    #     self.fields['city'].empty_label = "Select City"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
            }),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('region', 'name')
        widgets = {
            'region': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['region'].empty_label = "Select Region"
        

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['agency_owner', 'message']
        widgets = {
            
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'agency_owner': forms.Select(attrs={'class': 'form-control'}),
        }
        

