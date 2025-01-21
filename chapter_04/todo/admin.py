from django.contrib import admin
from todo.models import Todo

class TodoAdmin(admin.ModelAdmin):
    list_display = ['id','title','description']
    list_display_links = ['title','description']
# Register your models here.
admin.site.register(Todo, TodoAdmin)