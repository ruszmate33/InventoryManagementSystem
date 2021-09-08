from django.contrib.auth import get_user_model
from django.contrib import admin

# Register your models here.
from .models import Recipe, RecipeIngredient

User = get_user_model() # beyond the models.py this is how you get the userModel
admin.site.unregister(User) # we will need to unregister to register again with UserAdmin

admin.site.register(RecipeIngredient)

# class UserInline(admin.TabularInline):
#     model = User
#
# class RecipeAdmin(admin.ModelAdmin):
#     inlines = [UserInline, RecipeIngredientInline]
#     list_display = ['name', 'user']
#     readonly_fields = ['timestamp', 'updated']
#     raw_id_fields = ['user']
# ERRORS:
# <class 'recipes.admin.UserInline'>: (admin.E202) 'auth.User' has no ForeignKey to 'recipes.Recipe'.
# we need to Tab other things, since this is the highest in hierarchy
# user > recipe > recipeIngredient
# User-TabularInline -> Recipe-TabularInline


class RecipeInline(admin.TabularInline):
    model = Recipe
    extra = 0

class UserAdmin(admin.ModelAdmin):
    inlines = [RecipeInline]
    list_display = ['username']

admin.site.register(User, UserAdmin)

    
class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0
    readonly_fields = ['quantity_as_float']
    # fields = ['name', 'quantity', 'unit', 'directions']

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['name', 'user']
    readonly_fields = ['timestamp', 'updated']
    raw_id_fields = ['user']


admin.site.register(Recipe, RecipeAdmin)

