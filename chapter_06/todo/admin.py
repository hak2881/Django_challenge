from django.contrib import admin
from todo.models import Todo, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['content', 'author']

admin.site.register(Comment)

class TodoAdmin(admin.ModelAdmin):
    inlines = [  # 블로그 안에서 만들수 있께 해줌
        CommentInline
    ]


# Register your models here.
admin.site.register(Todo, TodoAdmin)