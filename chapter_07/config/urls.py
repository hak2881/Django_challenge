"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from todo.views import todo_list, todo_update, todo_delete
from todo.views import todo_info, todo_create
from member import views
from todo import cb_views

urlpatterns = [
    path('admin/', admin.site.urls),

    #FBV
    # path('', todo_list, name = 'todo_list'),
    # path('<int:pk>/', todo_info, name='todo_info'),
    # path('create/', todo_create, name='todo_create'),
    # path('<int:pk>/', todo_update, name='todo_update'),
    # path('<int:pk>/delete/', todo_delete, name='todo_delete'),

    path('', include('todo.urls')),

    path('signup/', views.signup, name= 'signup'),
    path('accounts/', include("django.contrib.auth.urls")), # 이걸해줘야

    path('login/', views.login, name = 'login'),

    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)