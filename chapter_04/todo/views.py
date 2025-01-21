from django.http import Http404
from django.shortcuts import render
from .models import Todo
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect
from django.urls import reverse
from todo.form import TodoForm
from django.views.decorators.http import require_http_methods


# Create your views here.


@login_required()
def todo_list(request):

    todo_titles = Todo.objects.filter(author = request.user)
    # if not todo_titles:
    #     return render(reverse('login'))

    q = request.GET.get('q')
    print(q)
    if q:
        todo_titles = todo_titles.filter(title__icontains=q)

    context = {
    'todo_titles' : todo_titles,
    'q': q,
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

@login_required()
def todo_create(request):
    form =  TodoForm(request.POST or None)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.author = request.user
        todo = form.save()
        return redirect(reverse('todo_list'))
    context = {
        'form':form,
    }
    return render(request, 'todo_create.html',context)

@login_required()
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk, author=request.user)

    form = TodoForm(request.POST or None, instance=todo)
    if form.is_valid():
        todo.save()
        return redirect(reverse('todo_list'))

    context = {
        'form':form,
    }
    return render(request, 'todo_update.html',context)
@login_required()
@require_http_methods(['POST'])
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, author=request.user)
    todo.delete()
    return redirect(reverse('todo_list'))