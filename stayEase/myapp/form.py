from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    CustomUser,
    CustomerProfile,
    AgencyProfile,
    OwnerProfile,
    Region,
    City,
    Property,
    Review,
    Inquiry
)

# --------------------
# 1. Customer Profile Form
# --------------------
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = [
            'customer_full_name',
            'phone',
            'email',
            'date_of_birth',
            'profile_photo',
            'address'
        ]
        widgets = {
            'customer_full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# --------------------
# 2. Agency Profile Form
# --------------------
class AgencyProfileForm(forms.ModelForm):
    class Meta:
        model = AgencyProfile
        fields = [
            'agency_name',
            'phone',
            'email',
            'contact_person',
            'license_number',
            'license_status',
            'address',
            'website',
            'agency_logo'
        ]
        widgets = {
            'agency_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone':forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'license_status': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'agency_logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# --------------------
# 3. Owner Profile Form
# --------------------
class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = OwnerProfile
        fields = [
            'owner_name',
            'address',
            'owner_photo'
        ]
        widgets = {
            'owner_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'owner_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# --------------------
# 4. Region & City Forms
# --------------------
class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['region', 'name']
        widgets = {
            'region': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

# --------------------
# 5. Property Form
# --------------------
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'name',
            'property_type',
            'description',
            'beds',
            'baths',
            'has_wifi',
            'has_pool',
            'has_kitchen',
            'area_sqft',
            'rent_type',
            'rent_amount',
            'security_deposit',
            'primary_image',
            'image_caption',
            'region',
            'city',
            'address',
            'latitude',
            'longitude',
            'status',
            'is_featured'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'beds': forms.NumberInput(attrs={'class': 'form-control'}),
            'baths': forms.NumberInput(attrs={'class': 'form-control'}),
            'has_wifi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_pool': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_kitchen': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'area_sqft': forms.NumberInput(attrs={'class': 'form-control'}),
            'rent_type': forms.Select(attrs={'class': 'form-control'}),
            'rent_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'security_deposit': forms.NumberInput(attrs={'class': 'form-control'}),
            'primary_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_caption': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# --------------------
# 6. Review Form
# --------------------
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# --------------------
# 7. User Registration Form
# --------------------
class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='CUSTOMER'
    )
    

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

# --------------------
# 8. Inquiry Form
# --------------------
class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your inquiry here...'}),
        }
