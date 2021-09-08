import pint
from django.conf import settings
from django.db import models

from .utils import number_str_to_float
from .validators import validate_unit_of_measure


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
    updated = models.BooleanField(default=True)

    def get_absolute_url(self):
        return f"/pantry/recipes/"

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=50)
    quantity_as_float = models.FloatField(blank=True, null=True) # we override the save() to set it automatically and validate there (not like with "unit" where we use validator)
    unit = models.CharField(max_length=50, validators=[validate_unit_of_measure]) # 'pounds', 'lbs', 'oz', 'gram'
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated =  models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return self.recipe.get_absolute_url()

    def convert_to_system(self, system="mks"):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg[self.unit]
        return measurement # or measurement.to_base_units()

    def to_ounces(self):
        m = self.convert_to_system()
        return round(m.to('ounces'), 2)

    def as_mks(self):
        # meter, pounds, second 
        measurement = self.convert_to_system(system='mks')
        return round(measurement.to_base_units(), 2)

    def as_imperial(self):
        # miles, pounds, seconds
        measurement = self.convert_to_system(system='imperial')
        return round(measurement.to_base_units(), 2)

    def save(self, *args, **kwargs):
        qty = self.quantity
        qty_as_float, qty_as_float_success = number_str_to_float(qty)
        if qty_as_float_success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float = None
        super().save(*args, **kwargs)

    # class RecipeImage():
    #     recipe = models.ForeignKey(Recipe)

