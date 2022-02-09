from django.contrib import admin
from .models import Account,UserProfile
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountAdmin(UserAdmin):
	list_display=('email','first_name','last_name','username','last_login','date_joined','is_active')
	list_display_links=('email','first_name','last_name')
	readonly_fields=('last_login','date_joined')
	ordering=('-date_joined',)
	fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','username')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

	filter_horizontal=()
	list_filter=()
	field_list=()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'pin_code')

admin.site.register(Account,AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)