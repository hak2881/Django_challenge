from django.http import Http404
from django.shortcuts import render
from .models import Todo

# Create your views here.



def todo_list(request):

    todo_titles = [title for title in Todo.objects.all()]

    context = {
    'todo_titles' : todo_titles
    }

    return render(request,'todo_list.html',context)

def todo_info(request, pk):

    todo = Todo.objects.get(pk=pk)

    context = { 'data' :
        {
        'title':todo.title,
        'description':todo.description,
        'created_at':todo.created_at,
        'tart_date':todo.start_date,
        'end_date':todo.end_date,
        'modified_at':todo.modified_at,
        'is_completed':todo.is_completed,
        }
    }

    return render(request,'todo_info.html', context)