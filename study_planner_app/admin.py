from django.contrib import admin
from .models import Subject, Tag, StudyTask

# Register your models here.
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ['name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(StudyTask)
class StudyTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'subject', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'subject', 'tags')
    search_fields = ('title', 'description')