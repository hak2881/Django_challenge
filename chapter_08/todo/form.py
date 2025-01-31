from django import forms
from todo.models import Todo, Comment
from django_summernote.widgets import SummernoteWidget

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo

        fields = ('title', 'description','image' ,'start_date', 'end_date', 'is_completed')
        widgets = {
            'description' : SummernoteWidget()
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'})
        }
