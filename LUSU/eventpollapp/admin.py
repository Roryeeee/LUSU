from django.contrib import admin
from .models import UserGroup, TimeOption, Event, Profile, Vote


admin.site.register(UserGroup)
admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(TimeOption)
admin.site.register(Vote)

