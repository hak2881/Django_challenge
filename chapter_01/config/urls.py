# -*- coding: utf-8 -*-
from django.contrib import admin
from django.http import Http404
from django.shortcuts import render
from django.urls import path
from fake_db import user_db


_db = user_db


def user_list(request):
    # '이름'과 'id'가 제대로 있는지 확인하고, 없는 경우 오류를 처리
    names = [{"name": db.get("name", "이름 없음"), "id": db.get("id")} for db in _db]
    return render(request, 'user_list.html', {'data': names})



def user_info(request, user_id):
    # user_id가 범위 내에 있는지 확인
    if user_id < 1 or user_id > len(_db):
        raise Http404('User not found')

    # user_id - 1로 인덱스 조정
    info = _db[user_id - 1]
    return render(request, 'user_info.html', {'data': info})


urlpatterns = [
    path('users/', user_list, name='user_list'),
    path('users/<int:user_id>/', user_info, name='user_info'),
    path('admin/', admin.site.urls),
]
