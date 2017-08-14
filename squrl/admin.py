from django.contrib import admin

from .models import Squrls

# Register the Urls model with UrlsAdmin options to make it accessible in admin app

class SqurlsAdmin(admin.ModelAdmin):
    list_display = ('squrl','target', 'creation_date', 'access_date', 'visits')
    ordering = ('-access_date',)

admin.site.register(Squrls, SqurlsAdmin)
