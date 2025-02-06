
from django.test import TestCase
from django.urls import reverse

from .models import Restaurant
from rest_framework.test import APITestCase
from rest_framework import status
# Create your tests here.


class RestaurantModelTestCase(TestCase):
    def setUp(self):
        self.restaurant_info=Restaurant.objects.create(
            name='이름',
            address='주소',
            contact='못함',
        )


    def test_create_restaurant(self):
        restaurant = Restaurant.objects.get(name='이름')
        self.assertEqual(restaurant.name, '이름')


class RestaurantViewTestCase(APITestCase):
    def setUp(self):
        self.restaurant_info={
            'name':'이름',
            'address':'주소',
            'contact':'못함',
        }

    def test_restaurant_list_view(self):
        response = self.client.get(reverse('restaurants:restaurant-list'))
        Restaurant.objects.create(**self.restaurant_info)

        restaurant_list = Restaurant.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), restaurant_list.count()+3)

    def test_restaurant_post_view(self):
        url = reverse('restaurants:restaurant-list')
        response = self.client.post(url, self.restaurant_info, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.first().name, self.restaurant_info['name'])

    def test_restaurant_detail_view(self):
        restaurant = Restaurant.objects.create(**self.restaurant_info)
        url = reverse('restaurants:restaurant-detail', kwargs={'pk': restaurant.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('name'), self.restaurant_info['name'])

    def test_restaurant_update_view(self):
        restaurant = Restaurant.objects.create(**self.restaurant_info)
        url = reverse('restaurants:restaurant-detail', kwargs={'pk': restaurant.id})
        updated_restaurant_info = {
            "name": "Updated Restaurant",
            "description": "Updated Description",
            "address": "Updated Address",
            "contact": "Updated Contact",
            "open_time": "11:00:00",
            "close_time": "23:00:00",
            "last_order": "22:00:00",
            "regular_holiday": "TUE"
        }

        response = self.client.put(url, updated_restaurant_info, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(response.data.get('name'), updated_restaurant_info['name'])
        self.assertEqual(response.data.get('address'), updated_restaurant_info['address'])
        self.assertEqual(response.data.get('contact'), updated_restaurant_info['contact'])
        self.assertEqual(response.data.get('open_time'), updated_restaurant_info['open_time'])
        self.assertEqual(response.data.get('close_time'), updated_restaurant_info['close_time'])
        self.assertEqual(response.data.get('last_order'), updated_restaurant_info['last_order'])
        self.assertEqual(response.data.get('regular_holiday'), updated_restaurant_info['regular_holiday'])

    def test_restaurant_delete_view(self):
        restaurant = Restaurant.objects.create(**self.restaurant_info)
        url = reverse('restaurants:restaurant-detail', kwargs={'pk': restaurant.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Restaurant.objects.count(), 0)