from django.contrib import admin
from myapp.models import CustomUser,CustomerProfile,AgencyProfile,OwnerProfile,Region,City,Property,Review,SaveProperty,Inquiry

admin.site.register(CustomUser)
admin.site.register(CustomerProfile)
admin.site.register(AgencyProfile)
admin.site.register(OwnerProfile)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(Property)
admin.site.register(Review)
admin.site.register(SaveProperty)
admin.site.register(Inquiry)