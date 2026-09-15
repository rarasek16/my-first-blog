from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import Category, Post


LESSONS = [
    {
        "category": "zaklady",
        "title": "Jak Django promění URL adresu v hotovou stránku",
        "days_ago": 6,
        "text": """Když do prohlížeče zadáš adresu stránky, Django ji nezobrazí samo od sebe. Postupuje po jasné trase: URL adresa -> view -> šablona -> HTML odpověď.

1. Soubor urls.py rozhodne, která funkce nebo třída obslouží danou adresu.
2. View připraví data a zvolí šablonu.
3. Šablona spojí HTML s daty a Django pošle výsledek do prohlížeče.

Zkus si změnit název URL nebo text ve view a stránku obnov. Právě tato rychlá zpětná vazba dělá z Djanga příjemný nástroj pro učení webového vývoje.""",
    },
    {
        "category": "zaklady",
        "title": "Virtuální prostředí: proč projekt nechce sdílet balíčky",
        "days_ago": 5,
        "text": """Každý Python projekt může potřebovat jinou verzi knihovny. Virtuální prostředí je oddělený adresář s vlastní instalací balíčků, takže změna v jednom projektu nerozbije druhý.

Na Windows jej aktivuješ příkazem myvenv\\Scripts\\Activate.ps1. Pak instaluj závislosti pomocí pip install -r requirements.txt. Soubor requirements.txt je seznam verzí, které projekt potřebuje.

Do Gitu virtuální prostředí nepatří. Je velké, závislé na konkrétním počítači a každý vývojář si ho umí vytvořit z requirements.txt znovu.""",
    },
    {
        "category": "databaze",
        "title": "Model, migrace a SQLite: tři části jedné databázové změny",
        "days_ago": 4,
        "text": """Model v models.py je Pythonový popis dat. Třeba Post říká, že příspěvek má autora, název, text a datum publikování. Django z modelu umí vytvořit databázovou tabulku.

Když model změníš, spusť nejdřív python manage.py makemigrations. Django vytvoří migraci - přesný záznam změny databáze. Potom python manage.py migrate změnu skutečně aplikuje.

SQLite je pro školní projekt výborná: databáze je jediný soubor db.sqlite3 a nepotřebuje samostatný server. V produkci se později můžeš přesunout třeba na MySQL nebo PostgreSQL, ale princip modelů a migrací zůstane stejný.""",
    },
    {
        "category": "databaze",
        "title": "Django admin: nejrychlejší cesta k vlastním datům",
        "days_ago": 3,
        "text": """Django admin je hotové administrátorské rozhraní. Po vytvoření superuživatele příkazem python manage.py createsuperuser otevři adresu /admin/ a přihlas se.

Model se v administraci objeví po registraci v admin.py. V tomto projektu může správce vytvářet články i kategorie, vyhledávat podle názvu a filtrovat je podle tématu.

Admin není náhradou veřejného designu. Je to pracovní nástroj pro správu obsahu. Díky němu ale můžeš rychle přidávat výukové články, aniž bys pro každý nový příspěvek měnil zdrojový kód.""",
    },
    {
        "category": "bezpecnost",
        "title": "Přihlášení, CSRF a oprávnění: komu Django dovolí měnit článek",
        "days_ago": 2,
        "text": """Přihlášení zjišťuje, kdo uživatel je. Oprávnění řeší, co tento uživatel smí udělat. Jsou to dvě různé věci a bezpečná aplikace potřebuje obě.

Decorator @login_required nepustí nepřihlášeného návštěvníka na formulář nového článku. Při úpravě článku filtrujeme objekt i podle author=request.user, takže autor nemůže upravovat cizí práci jen změnou čísla v URL.

Formuláře odesílané metodou POST obsahují {% csrf_token %}. Tento token chrání uživatele před podvrženým požadavkem z jiné webové stránky. Nikdy jej z formuláře neodstraňuj jen proto, aby chyba zmizela.""",
    },
    {
        "category": "nasazeni",
        "title": "Od localhostu k PythonAnywhere: kontrolní seznam nasazení",
        "days_ago": 1,
        "text": """Lokální adresa 127.0.0.1 funguje jen na tvém počítači. Aby projekt viděli ostatní, musí běžet na serveru. PythonAnywhere je vhodná platforma pro první Django nasazení.

Před zveřejněním nastav DEBUG = False, vyplň konkrétní doménu do DJANGO_ALLOWED_HOSTS a vlož silný DJANGO_SECRET_KEY do proměnné prostředí. Tajné hodnoty nepatří do repozitáře.

Nakonec spusť migrace, nastav statické soubory a otestuj přihlášení i stránku 404. Nasazení není poslední kliknutí: je to ověření, že aplikace funguje bezpečně i mimo tvůj vlastní počítač.""",
    },
]


class Command(BaseCommand):
    help = "Create original Czech Django lessons for the student blog."

    def handle(self, *args, **options):
        user_model = get_user_model()
        author, author_created = user_model.objects.get_or_create(
            username="django_start",
            defaults={"is_active": False},
        )

        categories = {}
        for slug, name in (
            ("zaklady", "Základy"),
            ("databaze", "Databáze"),
            ("bezpecnost", "Bezpečnost"),
            ("nasazeni", "Nasazení"),
        ):
            categories[slug], _ = Category.objects.get_or_create(name=name, slug=slug)

        now = timezone.now()
        created_count = 0
        for lesson in LESSONS:
            _, created = Post.objects.get_or_create(
                author=author,
                title=lesson["title"],
                defaults={
                    "category": categories[lesson["category"]],
                    "text": lesson["text"],
                    "published_date": now - timedelta(days=lesson["days_ago"]),
                },
            )
            created_count += created

        if author_created:
            self.stdout.write("Created the disabled author account django_start.")
        self.stdout.write(
            self.style.SUCCESS(
                f"Learning content ready: {created_count} new lesson(s), {len(LESSONS) - created_count} already present."
            )
        )
