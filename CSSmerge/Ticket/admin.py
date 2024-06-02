from django.contrib import admin
from .models import Ticket

class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status")
    search_fields = (("id", "title", "status"))
    readonly_fields = ['user']

    def save_model(self, request, obj, form, change):
        # Set the user field to the currently logged-in user only when creating a new ticket
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Ticket, TicketAdmin)
