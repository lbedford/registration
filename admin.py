from django.contrib import admin
from registration.models import Lbw
from registration.models import Activity
from registration.models import Accomodation
from registration.models import Message
from registration.models import UserRegistration

class LbwAdmin(admin.ModelAdmin):
  list_display = ('description', 'start_date', 'end_date')
admin.site.register(Lbw, LbwAdmin)

class ActivityAdmin(admin.ModelAdmin):
  list_display = ('description', 'start_date', 'end_date')
admin.site.register(Activity, ActivityAdmin)

admin.site.register(Message)
admin.site.register(Accomodation)

class UserRegistrationAdmin(admin.ModelAdmin):
  list_display = ('lbw', 'user', 'children')
admin.site.register(UserRegistration, UserRegistrationAdmin)
