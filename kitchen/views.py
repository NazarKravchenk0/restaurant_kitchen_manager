from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from kitchen.forms import (
    CookCreationForm,
    CookUpdateForm,
    DishForm,
    DishTypeForm,
    IngredientForm,
    SearchForm,
)
from kitchen.models import Dish, DishType, Ingredient


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "kitchen/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_cooks"] = get_user_model().objects.count()
        context["num_dish_types"] = DishType.objects.count()
        context["num_dishes"] = Dish.objects.count()
        context["num_ingredients"] = Ingredient.objects.count()

        context["latest_dishes"] = Dish.objects.select_related("dish_type").prefetch_related("cooks").order_by(
            "-created_at"
        )[:5]
        return context


# ======== Cook ========
class CookListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 10
    template_name = "kitchen/cook_list.html"
    context_object_name = "cook_list"

    def get_queryset(self):
        queryset = super().get_queryset().annotate(num_dishes=Count("dishes"))
        form = SearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data.get("q"):
            q = form.cleaned_data["q"]
            queryset = queryset.filter(
                Q(username__icontains=q)
                | Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET)
        return context


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    template_name = "kitchen/cook_detail.html"
    context_object_name = "cook"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("dishes")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = CookCreationForm
    template_name = "kitchen/form.html"
    success_url = reverse_lazy("kitchen:cook-list")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = CookUpdateForm
    template_name = "kitchen/form.html"
    success_url = reverse_lazy("kitchen:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:cook-list")


# ======== DishType ========
class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    paginate_by = 10
    template_name = "kitchen/dish_type_list.html"

    def get_queryset(self):
        queryset = super().get_queryset().annotate(num_dishes=Count("dishes"))
        form = SearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data.get("q"):
            queryset = queryset.filter(name__icontains=form.cleaned_data["q"])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET)
        return context


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    form_class = DishTypeForm
    template_name = "kitchen/form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    form_class = DishTypeForm
    template_name = "kitchen/form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


# ======== Ingredient ========
class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    paginate_by = 10
    template_name = "kitchen/ingredient_list.html"

    def get_queryset(self):
        queryset = super().get_queryset().annotate(num_dishes=Count("dishes"))
        form = SearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data.get("q"):
            queryset = queryset.filter(name__icontains=form.cleaned_data["q"])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET)
        return context


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "kitchen/form.html"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "kitchen/form.html"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:ingredient-list")


# ======== Dish ========
class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 10
    template_name = "kitchen/dish_list.html"

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("dish_type")
            .prefetch_related("cooks", "ingredients")
        )
        form = SearchForm(self.request.GET)
        if form.is_valid() and form.cleaned_data.get("q"):
            q = form.cleaned_data["q"]
            queryset = queryset.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET)
        return context


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "kitchen/dish_detail.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("dish_type")
            .prefetch_related("cooks", "ingredients")
        )


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/form.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/form.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-list")
