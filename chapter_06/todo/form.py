from django import forms
from todo.models import Todo, Comment

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo

        fields = ('title', 'description', 'start_date', 'end_date', 'is_completed')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'})
        }
