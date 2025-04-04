from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, Project, Task

# UserProfile Admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'whatsapp_number')
    search_fields = ('user__username', 'whatsapp_number')

# Task Inline for Project Admin
class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    fields = ('task_name', 'assigned_to', 'status', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date')

# Project Admin
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_by', 'created_at', 'current_task_display')
    search_fields = ('title', 'created_by__username')
    list_filter = ('status', 'created_at')
    inlines = [TaskInline]
    
    def current_task_display(self, obj):
        task = obj.current_task()
        return format_html('<strong>{}</strong>', task) if task else "لا توجد مهام حالية"
    current_task_display.short_description = "المهمة الحالية"

# Task Admin
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'project', 'assigned_to', 'status', 'start_date', 'end_date')
    search_fields = ('task_name', 'project__title', 'assigned_to__username')
    list_filter = ('status', 'start_date', 'end_date')
    ordering = ('-start_date',)

# Register Models
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)

# Admin Site Customization
admin.site.site_header = "لوحة تحكم المشاريع"
admin.site.site_title = "إدارة المشاريع"
admin.site.index_title = "مرحبًا بك في لوحة الإدارة"
