from django.contrib import admin

from .models import City, Tag, Job
# Register your models here.

def make_published(modeladmin, request, queryset):
    queryset.update(moderated=True)

class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "city", "moderated")
    filter_horizontal = ("tags",)
    actions = [make_published]

admin.site.register(City)
admin.site.register(Tag)
admin.site.register(Job, JobAdmin)