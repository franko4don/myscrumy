from django.contrib import admin

from .models import ScrumyGoal, GoalStatus, Task

admin.site.register(Task)
# admin.site.register(ScrumyUser)
admin.site.register(ScrumyGoal)
admin.site.register(GoalStatus)
# Register your models here.
