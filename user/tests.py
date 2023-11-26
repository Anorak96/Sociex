from django.test import TestCase
from .models import User

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username='BigBob', email='bigbob@gmail.com')

    def test_username_label(self):
        user = User.objects.get(pk='BigBob')
        field_label = user._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')

    def test_object_name_is_username(self):
        user = User.objects.get(pk='BigBob')
        expected_object_name = f'{user.username}'
        self.assertEqual(str(user), expected_object_name)

    def test_get_absolute_url(self):
        user = User.objects.get(pk='BigBob')
        # This will also fail if the urlconf is not defined.
        self.assertEqual(user.get_absolute_url(), '/user/BigBob/')
