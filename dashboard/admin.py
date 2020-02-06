from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(Organisation)
# admin.site.register(Camera)
# admin.site.register(UserDetails)
# admin.site.register(Analytics)
# admin.site.register(StaffVerification)

class AdminStaffVerification(admin.ModelAdmin):
    list_display = ('token' , 'email' , 'visited')

class AdminOrganisation(admin.ModelAdmin):
    list_display = ('id' , 'name' , 'address' , 'api_key')

class AdminUserDetails(admin.ModelAdmin):
    list_display = ('user' , 'org_id','phone','pic','privilege')

class AdminAnalytics(admin.ModelAdmin):
    list_display = ('user' , 'timestamp' , 'camera_id')

class AdminCamera(admin.ModelAdmin):
    list_display = ('name' , 'org_id')

class AdminCandidatePic(admin.ModelAdmin):
    list_display = ( 'user','images',)


admin.site.register(StaffVerification , AdminStaffVerification)
admin.site.register(Organisation , AdminOrganisation)
admin.site.register(Camera , AdminCamera)
admin.site.register(Analytics , AdminAnalytics)
admin.site.register(UserDetails , AdminUserDetails)
admin.site.register(CandidatePics , AdminCandidatePic)
