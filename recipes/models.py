from django.conf import settings
from django.db import models


"""
-Global
    - Ingredients
    - Recipes
- User
    - Ingredients
    - Recipes
        - Ingredients
        - Directions for Ingredients
"""

User = settings.AUTH_USER_MODEL

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated =  models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated =  models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    # class RecipeImage():
    #     recipe = models.ForeignKey(Recipe)

