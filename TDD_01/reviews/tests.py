from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Review
# Create your tests here.

from .models import Restaurant
# Create your tests here.

User = get_user_model()

class RestaurantModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            nickname='test',
            email='test@test.com'
        )
        self.restaurant=Restaurant.objects.create(
            name='이름',
            address='주소',
            contact='못함',
        )
        Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            title='리뷰제목',
            comment='맛있다',
        )


    def test_create_review(self):
        restaurant = Review.objects.get(title='리뷰제목')
        self.assertEqual(restaurant.title, '리뷰제목')


