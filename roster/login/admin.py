from django.contrib import admin

from login.models import User, Staff, Manager, Admin

admin.site.register(User)
admin.site.register(Staff)
admin.site.register(Manager)
admin.site.register(Admin)

