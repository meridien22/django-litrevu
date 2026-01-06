from django.contrib import admin
from authentication.models import User
from authentication.models import UserFollows

class UserAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "username",
                    "last_login")
    
class UserFollwsAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "user",
                    "followed_user")

admin.site.register(User, UserAdmin)

admin.site.register(UserFollows, UserFollwsAdmin)