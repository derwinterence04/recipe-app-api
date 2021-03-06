from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@test.com', password='testpass'):
    """" Create sample user """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating new user with an email is successful"""
        email = 'test@test.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Test email if normalized """
        email = "test@TEST.COM"
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test createing user with no email raises error """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating new superuser with an email is successful"""
        email = 'test@test.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """ Test tag string representation """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """ Test ingredient string representation """
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Pork'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """ Test ingredient string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Beef and Mushroom',
            time_in_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_filename_uuid(self, mock_uuid):
        """ Test image is saved in correct location """
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid

        file_path = models.recipe_image_path(None, 'tempimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
