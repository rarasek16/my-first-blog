import secrets
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


DEMO_USERS = (
    ("ada_demo", "Ada", "Student", False),
    ("bruno_demo", "Bruno", "Student", False),
    ("cyril_demo", "Cyril", "Student", False),
    ("admin_demo", "Admin", "DjangoStart", True),
)


class Command(BaseCommand):
    help = "Create or reset local-only demo accounts and write their credentials outside Git."

    def add_arguments(self, parser):
        parser.add_argument(
            "--credentials-file",
            type=Path,
            default=settings.BASE_DIR / "local" / "demo-accounts.txt",
            help="Local file for generated credentials (default: local/demo-accounts.txt).",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Demo accounts may only be created when DEBUG is enabled.")

        credentials_file = options["credentials_file"].resolve()
        local_directory = (settings.BASE_DIR / "local").resolve()
        if not credentials_file.is_relative_to(local_directory):
            raise CommandError("Credentials must be stored inside the ignored local directory.")

        user_model = get_user_model()
        credentials = []
        for username, first_name, last_name, is_admin in DEMO_USERS:
            password = secrets.token_urlsafe(12)
            user, _ = user_model.objects.get_or_create(
                username=username,
                defaults={"first_name": first_name, "last_name": last_name},
            )
            user.set_password(password)
            user.is_active = True
            user.is_staff = is_admin
            user.is_superuser = is_admin
            user.save()
            credentials.append((username, password))

        credentials_file.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "LOCAL DEVELOPMENT ONLY - do not commit or publish this file.",
            "Passwords are regenerated whenever create_demo_accounts is run.",
            "",
            "username | password",
            "-------------------",
            *(f"{username} | {password}" for username, password in credentials),
            "",
        ]
        credentials_file.write_text("\n".join(lines), encoding="utf-8")
        self.stdout.write(self.style.SUCCESS(f"Created 4 demo accounts. Credentials: {credentials_file}"))
