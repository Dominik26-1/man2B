from django.contrib import admin


# Register your models here.
class BasicAdmin(admin.ModelAdmin):
    exclude = ["avg_rating"]
