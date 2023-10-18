from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
# class AccountAdmin(UserAdmin):
#     list_display = ('email','first_name','last_name','user_name','last_login','date_joined','is_active')
#     list_display_links = ('email','first_name','last_name')
#     readonly_fields = ('last_login','date_joined')
#     ordering = ('-date_joined',)

#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()

admin.site.register(Account)
admin.site.register(UserAddress)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Feedback)
# admin.site.register(Referalid)

class ReferalidAdmin(admin.ModelAdmin):
    list_display = ('currentuser','referalid')
admin.site.register(Referalid,ReferalidAdmin)


    
    