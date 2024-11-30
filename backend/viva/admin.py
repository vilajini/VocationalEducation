from django.contrib import admin

# Register your models here.
from .models import Users, Questions, VivaSessions, Responses, Feedback

admin.site.register(Users)
admin.site.register(Questions)
admin.site.register(VivaSessions)
admin.site.register(Responses)
admin.site.register(Feedback)