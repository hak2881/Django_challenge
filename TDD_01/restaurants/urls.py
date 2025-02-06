from django.urls import path, include

from restaurants import views
from rest_framework import routers

app_name = 'restaurants'

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'restaurants', views.RestaurantViewSet, basename='restaurant')

urlpatterns = [
    path('', include(router.urls)),
]