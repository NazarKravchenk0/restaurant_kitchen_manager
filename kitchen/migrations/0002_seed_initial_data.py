from django.db import migrations


def seed_initial_data(apps, schema_editor):
    Cook = apps.get_model("kitchen", "Cook")
    DishType = apps.get_model("kitchen", "DishType")
    Ingredient = apps.get_model("kitchen", "Ingredient")
    Dish = apps.get_model("kitchen", "Dish")

    # --- demo users ---
    admin_username = "admin"
    admin_password = "admin12345"

    if not Cook.objects.filter(username=admin_username).exists():
        admin = Cook(
            username=admin_username,
            first_name="Admin",
            last_name="User",
            years_of_experience=10,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        admin.set_password(admin_password)
        admin.save()

    # --- dish types ---
    soup, _ = DishType.objects.get_or_create(name="Soup")
    main, _ = DishType.objects.get_or_create(name="Main")
    dessert, _ = DishType.objects.get_or_create(name="Dessert")

    # --- ingredients ---
    chicken, _ = Ingredient.objects.get_or_create(name="Chicken")
    potato, _ = Ingredient.objects.get_or_create(name="Potato")
    salt, _ = Ingredient.objects.get_or_create(name="Salt")
    cheese, _ = Ingredient.objects.get_or_create(name="Cheese")
    sugar, _ = Ingredient.objects.get_or_create(name="Sugar")

    admin = Cook.objects.get(username=admin_username)

    # --- dishes (with relations) ---
    dish1, _ = Dish.objects.get_or_create(
        name="Chicken Soup",
        defaults={
            "description": "Classic chicken soup.",
            "price": "7.50",
            "dish_type": soup,
        },
    )
    dish1.cooks.set([admin])
    dish1.ingredients.set([chicken, potato, salt])

    dish2, _ = Dish.objects.get_or_create(
        name="Cheesecake",
        defaults={
            "description": "Creamy dessert.",
            "price": "6.20",
            "dish_type": dessert,
        },
    )
    dish2.cooks.set([admin])
    dish2.ingredients.set([cheese, sugar])


def unseed(apps, schema_editor):
    # Usually we do not delete demo data.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("kitchen", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_initial_data, unseed),
    ]
