from django.contrib import admin
from events.models import Event, Registration, Experiment, Group

class EventAdmin(admin.ModelAdmin):
    list_filter = ('status',)

class RegistrationAdmin(admin.ModelAdmin):
    list_filter = ('group',)

admin.site.register(Event, EventAdmin)
admin.site.register(Group)
admin.site.register(Experiment)
admin.site.register(Registration, RegistrationAdmin)
