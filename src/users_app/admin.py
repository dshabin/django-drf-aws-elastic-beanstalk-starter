from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display =  ('user',)
    search_fields = ('user__username',)

    def user(self, obj):
        try:
            return self.user.username
        except:
            return "-"

admin.site.register(Profile,ProfileAdmin)
