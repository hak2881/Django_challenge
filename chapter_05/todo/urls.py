# CBV
from todo import cb_views
from django.urls.conf import path

app_name = 'todo'

urlpatterns = [
    path('', cb_views.TodoListView.as_view(), name='list'),
    path('<int:pk>/', cb_views.TodoDetailView.as_view(), name='info'),
    path('create/', cb_views.TodoCreateView.as_view(), name='create'),
    path('<int:pk>/update/', cb_views.TodoUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', cb_views.TodoDeleteView.as_view(), name='delete'),
]