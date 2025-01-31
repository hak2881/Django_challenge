from django.db.models import CASCADE

from django.db import models
from django.contrib.auth import get_user_model
from django.urls.base import reverse
from utils.models import TimeStampModel

from PIL import Image
from pathlib import Path
from io import BytesIO

User = get_user_model()

# Create your models here.
class Todo(TimeStampModel):

    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    is_completed = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField('이미지', null=True, blank=True, upload_to='todo/%Y/%m/%d')
    thumbnail = models.ImageField('썸네일', null=True, blank=True, upload_to='todo/%Y/%m/%d/thumbnail')

    def __str__(self):  # 객체를 admin 에서 읽기쉬운 문자열로 표현
        return self.title

    def get_absolute_url(self):
        return reverse('todo:info', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        if not self.image:
            return super().save(*args, **kwargs)
        image = Image.open(self.image)
        image.thumbnail((300,300))

        image_path = Path(self.image.name)

        thumbnail_name = image_path.stem
        thumbnail_extension = image_path.suffix.lower()
        thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}'

        if thumbnail_extension in ['.jpg', 'jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_filename, temp_thumb, save= False)
        temp_thumb.close()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Todo'
        verbose_name_plural = '할일 생성'
        ordering = ['-created_at']

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
