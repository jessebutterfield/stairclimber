from django.contrib import admin
from countstairs.models import UserPreferences, CustomStairCount, DailyStairs

# Register your models here.
admin.site.register(UserPreferences)
admin.site.register(CustomStairCount)
admin.site.register(DailyStairs)