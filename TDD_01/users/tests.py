from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
User = get_user_model()

class UserModelTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            nickname='test',
            email='test@test.com'
        )
        User.objects.create(
            nickname='test2',
            email='test2@test.com',
            is_superuser=True
        )

    def test_user_manager_create_user(self):
        user = User.objects.get(nickname='test')
        self.assertEqual(user.nickname, 'test')

    def test_user_manager_create_superuser(self):
        user = User.objects.get(nickname='test2')
        self.assertEqual(user.is_superuser, True)
