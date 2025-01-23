from django.db.models import CASCADE

from django.db import models
from django.contrib.auth import get_user_model
from django.urls.base import reverse
from utils.models import TimeStampModel

User = get_user_model()

# Create your models here.
class Todo(TimeStampModel):

    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    is_completed = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):  # 객체를 admin 에서 읽기쉬운 문자열로 표현
        return self.title

    def get_absolute_url(self):
        return reverse('todo:info', kwargs={'pk':self.pk})

    class Meta:
        verbose_name = 'Todo'
        verbose_name_plural = '할일 생성'

class Comment(TimeStampModel):
    todo = models.ForeignKey(Todo, on_delete=CASCADE, related_name='comments')
    content = models.TextField('댓글', max_length=200)
    author = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f'{self.todo.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ['-created_at']
