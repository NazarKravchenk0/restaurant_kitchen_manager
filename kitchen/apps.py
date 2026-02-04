from django.apps import AppConfig


class KitchenConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kitchen"

    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError

        User = get_user_model()

        try:
            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="admin",
                    password="admin12345",
                )
                print("✅ Test superuser created: admin / admin12345")
        except OperationalError:
            pass
