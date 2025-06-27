from django.contrib import admin
from myapp.models import CustomerProfile,OwnerProfile,AgencyProfile,Region,City,Property

admin.site.register(CustomerProfile)
admin.site.register(OwnerProfile)
admin.site.register(AgencyProfile)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(Property)


