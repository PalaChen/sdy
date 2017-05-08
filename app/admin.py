from django.contrib import admin
from reposition import models


class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Users)
