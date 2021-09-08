from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Recipe, RecipeIngredient

User = get_user_model()

class UserTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('my_user', password='asdfqwert1234')

    def test_user_pw(self):
        checked = self.user_a.check_password('asdfqwert1234')


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('my_user', password='asdfqwert1234')
        self.recipe_a = Recipe.objects.create(
            user=self.user_a, 
            name='Grilled chicken')
        self.recipe_b = Recipe.objects.create(
            user=self.user_a, 
            name='Grilled chicken tacos')
        self.recipe_ingredient_a = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name='chicken',
            quantity='1',
            unit='kg')

    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 1) # setUp()s are isolated from each other: RecipeTestCase vs UserTestCase

    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all() # {highestModel}.{child}_set.all() -> qs
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_forward_count(self):
        user = self.user_a
        qs = Recipe.objects.filter(user=user)
        self.assertEqual(qs.count(), 2)

    def test_recipe_recipeIngredient_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.recipeingredient_set.all() # for some reason in {highestModel}.{child}_set.all(), the {child} is ALL-LOWERCASE
        self.assertEqual(qs.count(), 1)

    def test_recipe_recipeIngredient_forward_count(self):
        recipe = self.recipe_a
        qs = RecipeIngredient.objects.filter(recipe=recipe)
        self.assertEqual(qs.count(), 1)

    def test_user_two_level_relation(self):
        user = self.user_a
        qs = RecipeIngredient.objects.filter(recipe__user=user) # RecipeIngredient -> Recipe -> User
        self.assertEqual(qs.count(), 1)

    # def test_user_three_level_relation(self):
    #     # eg in models:     class RecipeIngredientImage(models.Model):
    #     #                       RecipeIngredient = models.ForeignKey(RecipeIngredient, on_delete=model.CASCADE)
    #     user = self.user_a
    #     qs = RecipeIngredientImage.objects.filter(recipeingredient__recipe__user=user) # RecipeIngredientImage -> RecipeIngredient -> Recipe -> User
    #     self.assertEqual(qs.count(), 1)

    def test_user_two_level_relation_reverse(self):
        # this rarely makes sense, do rather the normal forward
        user = self.user_a
        recipeIngredient_ids = list(user.recipe_set.all().values_list('recipeingredient__id', flat=True)) # User -> Recipe -> RecipeIngredient
        qs = RecipeIngredient.objects.filter(id__in=recipeIngredient_ids)
        self.assertEqual(qs.count(), 1)

    # instead of the complicated mess of "_reverse"
    def test_user_two_level_relation_via_recipes(self):
        user = self.user_a
        ids = user.recipe_set.all().values_list("id", flat=True)
        qs = RecipeIngredient.objects.filter(recipe__id__in=ids) # RecipeIngredient -> Recipe -> User
        self.assertEqual(qs.count(), 1)

    def test_unit_measure_validation(self):
        # not with create just construct it
        ingredient = RecipeIngredient(
            name='New',
            quantity=10, 
            recipe=self.recipe_a,
            unit='kg'
        )
        ingredient.full_clean() # similar to form.is_valid()

    def test_unit_measure_validation_error(self):
        invalid_unit = 'nada'
        with self.assertRaises(ValidationError):
            # not with create just construct it
            ingredient = RecipeIngredient(
                name='New',
                quantity=10, 
                recipe=self.recipe_a,
                unit=invalid_unit
            )
            ingredient.full_clean() # similar to form.is_valid()

    
