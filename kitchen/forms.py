from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from kitchen.models import Dish, DishType, Ingredient


def _bootstrapify_form_fields(form: forms.BaseForm) -> None:
    """Apply Bootstrap 5 classes to widgets in a form."""
    for name, field in form.fields.items():
        widget = field.widget
        # keep checkbox select multiple as list group style
        if isinstance(widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
            continue
        if isinstance(widget, forms.Select):
            classes = widget.attrs.get("class", "")
            widget.attrs["class"] = (classes + " form-select").strip()
        else:
            classes = widget.attrs.get("class", "")
            widget.attrs["class"] = (classes + " form-control").strip()


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "years_of_experience",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _bootstrapify_form_fields(self)


class CookUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "years_of_experience")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _bootstrapify_form_fields(self)


class DishTypeForm(forms.ModelForm):
    class Meta:
        model = DishType
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _bootstrapify_form_fields(self)


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _bootstrapify_form_fields(self)


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ("name", "dish_type", "description", "price", "cooks", "ingredients")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "cooks": forms.CheckboxSelectMultiple,
            "ingredients": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _bootstrapify_form_fields(self)


class SearchForm(forms.Form):
    q = forms.CharField(required=False, label="Search")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _bootstrapify_form_fields(self)
        self.fields["q"].widget.attrs.update({"placeholder": "Search..."})
