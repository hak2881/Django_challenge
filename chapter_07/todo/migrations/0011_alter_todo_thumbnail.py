# Generated by Django 5.1.5 on 2025-01-24 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0010_todo_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='todo/%Y/%m/%d/thumbnail', verbose_name='썸네일'),
        ),
    ]
