from django.contrib import admin
from .models import Employee, Team, Contrat, Attendance

# Register your models here.
admin.site.register(Employee)
admin.site.register(Team)
admin.site.register(Contrat)
admin.site.register(Attendance)


