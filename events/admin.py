from django.contrib import admin
from events.models import Event, Registration, Experiment, Group

class EventAdmin(admin.ModelAdmin):
    list_filter = ('status',)

class ExperimentAdmin(admin.ModelAdmin):
    list_filter = ('status',)

class GroupAdmin(admin.ModelAdmin):
    list_filter = ('shift',)

class RegistrationAdmin(admin.ModelAdmin):
    list_filter = ('group',)

admin.site.register(Event, EventAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Registration, RegistrationAdmin)
