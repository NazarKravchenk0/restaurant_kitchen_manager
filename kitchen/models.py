from django.contrib.auth.models import AbstractUser
from django.db import models


class Cook(AbstractUser):
    """Custom user representing a cook in the restaurant."""

    years_of_experience = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        full_name = f"{self.first_name} {self.last_name}".strip()
        if full_name:
            return f"{self.username} ({full_name})"
        return self.username


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE, related_name="dishes")
    cooks = models.ManyToManyField(Cook, related_name="dishes", blank=True)
    ingredients = models.ManyToManyField(Ingredient, related_name="dishes", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
