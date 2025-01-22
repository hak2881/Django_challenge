from django.db import models
from django.contrib.auth import get_user_model
from django.urls.base import reverse

User = get_user_model()

# Create your models here.
class Todo(models.Model):

    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now= True)
    is_completed = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):  # 객체를 admin 에서 읽기쉬운 문자열로 표현
        return self.title

    def get_absolute_url(self):
        return reverse('todo:info', kwargs={'pk':self.pk})

    class Meta:
        verbose_name = 'Todo'
        verbose_name_plural = '할일 생성'

