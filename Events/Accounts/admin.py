from django.contrib import admin
from EventAPP.models import Events, Participants
# Register your models here.


class EventAdm(admin.ModelAdmin):
    list_display=['event_name','venue','description']

class ParticipantAdm(admin.ModelAdmin):
    list_display=['event_name','is_registered']

admin.site.register(Events, EventAdm)
admin.site.register(Participants, ParticipantAdm)