from django.contrib import admin
from registration.models import Lbw
from registration.models import Event
from registration.models import Accomodation
from registration.models import Message

class LbwAdmin(admin.ModelAdmin):
  list_display = ('description', 'start_date', 'end_date')

admin.site.register(Lbw, LbwAdmin)

class EventAdmin(admin.ModelAdmin):
  list_display = ('description', 'start_date', 'end_date')
admin.site.register(Event, EventAdmin)

admin.site.register(Message)
admin.site.register(Accomodation)
