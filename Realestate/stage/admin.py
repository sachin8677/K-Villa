from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BuyerProfile, SellerProfile, Property, Transaction

admin.site.register(User, UserAdmin)
admin.site.register(BuyerProfile)
admin.site.register(SellerProfile)
admin.site.register(Property)
admin.site.register(Transaction)