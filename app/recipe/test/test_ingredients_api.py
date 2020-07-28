from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTest(TestCase):
    """ Test publicly available ingredients API """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test login required when adding ingredient """
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTest(TestCase):
    """ Test private available ingredients API """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """ Test retrieving Ingredients """
        Ingredient.objects.create(
            name='Meat',
            user=self.user
        )
        Ingredient.objects.create(
            name='Cheese',
            user=self.user
        )

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_ingredients_limited_to_user(self):
        """ Test retrieving Ingredients """
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'testpass'
        )
        ingredient = Ingredient.objects.create(
            name='Meat',
            user=self.user
        )
        Ingredient.objects.create(
            name='Cheese',
            user=user2
        )

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """ Test if successfully created ingredient """
        payload = {'name': 'Meat'}

        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """ Test if successfully created ingredient """
        payload = {'name': ''}

        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
