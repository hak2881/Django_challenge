# Generated by Django 5.1.5 on 2025-01-24 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0007_alter_comment_todo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todo',
            options={'ordering': ['-created_at'], 'verbose_name': 'Todo', 'verbose_name_plural': '할일 생성'},
        ),
    ]
