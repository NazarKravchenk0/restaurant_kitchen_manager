from django.db import migrations


def seed_initial_data(apps, schema_editor):
    Cook = apps.get_model("kitchen", "Cook")
    DishType = apps.get_model("kitchen", "DishType")
    Ingredient = apps.get_model("kitchen", "Ingredient")
    Dish = apps.get_model("kitchen", "Dish")

    # ---------- Users (login for demo) ----------
    # admin / admin12345
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

    # Optional: simple non-admin user (if you want)
    # user / user12345
    demo_username = "user"
    demo_password = "user12345"
    if not Cook.objects.filter(username=demo_username).exists():
        user = Cook(
            username=demo_username,
            first_name="Demo",
            last_name="Cook",
            years_of_experience=2,
            is_staff=False,
            is_superuser=False,
            is_active=True,
        )
        user.set_password(demo_password)
        user.save()

    # ---------- Dish types ----------
    dish_types = {}
    for name in ["Soup", "Salad", "Main", "Dessert", "Drink"]:
        obj, _ = DishType.objects.get_or_create(name=name)
        dish_types[name] = obj

    # ---------- Ingredients ----------
    ingredients = {}
    for name in [
        "Chicken",
        "Beef",
        "Salmon",
        "Potato",
        "Carrot",
        "Onion",
        "Garlic",
        "Tomato",
        "Lettuce",
        "Cucumber",
        "Cheese",
        "Cream",
        "Flour",
        "Sugar",
        "Butter",
        "Lemon",
        "Salt",
        "Pepper",
    ]:
        obj, _ = Ingredient.objects.get_or_create(name=name)
        ingredients[name] = obj

    # ---------- Dishes + relations ----------
    admin = Cook.objects.get(username=admin_username)
    demo = Cook.objects.get(username=demo_username)

    dishes_data = [
        {
            "name": "Chicken Soup",
            "description": "Classic chicken soup with vegetables.",
            "price": "7.50",
            "dish_type": dish_types["Soup"],
            "cooks": [admin],
            "ingredients": ["Chicken", "Carrot", "Onion", "Garlic", "Salt", "Pepper"],
        },
        {
            "name": "Caesar Salad",
            "description": "Salad with cheese and creamy dressing.",
            "price": "8.90",
            "dish_type": dish_types["Salad"],
            "cooks": [demo],
            "ingredients": ["Lettuce", "Cheese", "Cream", "Salt", "Pepper"],
        },
        {
            "name": "Beef Steak",
            "description": "Grilled beef steak with гарнир.",
            "price": "16.00",
            "dish_type": dish_types["Main"],
            "cooks": [admin, demo],
            "ingredients": ["Beef", "Salt", "Pepper", "Butter"],
        },
        {
            "name": "Cheesecake",
            "description": "Creamy dessert with lemon notes.",
            "price": "6.20",
            "dish_type": dish_types["Dessert"],
            "cooks": [demo],
            "ingredients": ["Cheese", "Cream", "Sugar", "Butter", "Flour", "Lemon"],
        },
        {
            "name": "Lemonade",
            "description": "Fresh lemonade.",
            "price": "3.50",
            "dish_type": dish_types["Drink"],
            "cooks": [admin],
            "ingredients": ["Lemon", "Sugar"],
        },
    ]

    for d in dishes_data:
        dish, created = Dish.objects.get_or_create(
            name=d["name"],
            defaults={
                "description": d["description"],
                "price": d["price"],
                "dish_type": d["dish_type"],
            },
        )
        # if dish existed, ensure it has correct type/fields too (no harm)
        if not created:
            dish.description = d["description"]
            dish.price = d["price"]
            dish.dish_type = d["dish_type"]
            dish.save()

        dish.cooks.set(d["cooks"])
        dish.ingredients.set([ingredients[x] for x in d["ingredients"]])


def unseed_initial_data(apps, schema_editor):
    # Usually we do NOT delete demo data on rollback in portfolio projects.
    # Keep empty to avoid accidental deletes.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("kitchen", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_initial_data, unseed_initial_data),
    ]
