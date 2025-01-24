from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as django_login
# Create your views here.

def signup(request):

    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse('todo:list'))

    context = {
        'form' : form,
    }
    return render(request, 'signup.html', context)





def login(request):
    form = AuthenticationForm(request, request.POST or None)

    if request.method == "POST":
        print("POST data:", request.POST)  # 전달된 데이터 확인

    if form.is_valid():
        print("Form is valid")
        django_login(request, form.get_user())
        return redirect(reverse('todo:list'))
    else:
        print("Form errors:", form.errors)  # form 에러 출력

    context = {
        'form' : form,
    }

    return render(request, 'login.html', context)


