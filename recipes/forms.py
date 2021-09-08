from django import forms

from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']

    # def clean(self):
    #     data = self.cleaned_data
    #     name = data.get("name")
    #     qs = Recipe.objects.filter(title__icontains=name)
    #     if qs.exists():
    #         self.add_error("name", f"\"{name}\" is already in use.")
    #     return data