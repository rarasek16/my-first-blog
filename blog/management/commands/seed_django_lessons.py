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

LESSONS.extend(
    [
        {
            "category": "architektura",
            "title": "Šablony a statické soubory: obsah a vzhled odděleně",
            "days_ago": 7,
            "text": """Šablona spojuje HTML s daty z view. Základní šablona obsahuje společnou navigaci a patičku; jednotlivé stránky ji rozšiřují. CSS, obrázky a JavaScript ukládej do static/ uvnitř aplikace.

Oddělení obsahu, vzhledu a logiky dovolí měnit design bez zásahu do databáze a přidávat nové články bez úprav CSS.""",
        },
        {
            "category": "formular",
            "title": "Django formulář: validace dřív, než data uložíš",
            "days_ago": 8,
            "text": """HTML formulář získá data od uživatele, ale nesmíš jim bez kontroly věřit. ModelForm zná povinná pole modelu, vypíše chyby a ověří typy dat.

GET zobrazí prázdný formulář. POST jej zpracuje a is_valid rozhodne, zda se data smějí uložit. Tento vzor použiješ pro komentáře, rezervace i školní odevzdávání.""",
        },
        {
            "category": "testovani",
            "title": "Automatické testy: důkaz, že změna nic nerozbila",
            "days_ago": 9,
            "text": """Test připraví situaci, provede akci a ověří výsledek. Django TestCase používá vlastní testovací databázi, takže nepoškodí skutečná data.

Testuj hlavně pravidla: koncept není veřejný, nepřihlášený návštěvník nevytvoří článek a autor neupraví cizí příspěvek.""",
        },
        {
            "category": "frameworky",
            "title": "Django nebo Flask? Jak vybrat framework pro projekt",
            "days_ago": 10,
            "text": """Django nabízí ORM, administraci, formuláře, přihlášení a jasnou strukturu už v základu. Hodí se pro blog, evidenci, katalog a rezervační systém. Výhodou je rychlý start; nevýhodou více pravidel a souborů.

Flask je malý mikroframework. Hodí se pro prototyp nebo jednoduché API, je stručný a volný. Databázi, formuláře, administraci a strukturu větší aplikace ale vybíráš a skládáš sám.

Pro školní projekt s účty a databází zvol Django. Flask použij pro velmi malé API nebo jako srovnání, jaké služby Django řeší za tebe.""",
        },
        {
            "category": "nasazeni",
            "title": "Závěrečný projekt: od nápadu k odevzdání",
            "days_ago": 11,
            "text": """Vyber problém s jasným uživatelem a alespoň dvěma entitami: katalog knih a autorů, školní nástěnku, rezervace místností nebo evidenci úkolů.

Před kódem nakresli model a napiš tři uživatelské scénáře. Hotový projekt musí mít databázi, formulář, oprávnění, základní test, README a nasazenou ukázku.""",
        },
    ]
)

MATERIALS = {
    "Jak Django promění URL adresu v hotovou stránku": {
        "learning_goal": "Popíšu cestu požadavku a vytvořím URL, view a šablonu.",
        "code_example": """# blog/urls.py
path("ahoj/", views.ahoj, name="ahoj")

# blog/views.py
def ahoj(request):
    return render(request, "blog/ahoj.html", {"jmeno": "třído"})""",
        "code_explanation": "path spojí URL s view. View předá šabloně slovník dat; šablona je vypíše pomocí {{ jmeno }}.",
        "practice_task": "Přidej adresu /kontakt/ se jménem školy a odkazem zpět na úvod.",
    },
    "Model, migrace a SQLite: tři části jedné databázové změny": {
        "learning_goal": "Přidám pole do modelu a bezpečně provedu migraci.",
        "code_example": """class Book(models.Model):
    title = models.CharField(max_length=200)
    published_year = models.PositiveIntegerField()

python manage.py makemigrations
python manage.py migrate""",
        "code_explanation": "Model popisuje data. makemigrations zapíše změnu do historie a migrate ji aplikuje do databáze.",
        "practice_task": "Navrhni model knihy nebo školní události se třemi poli a vytvoř migraci.",
    },
    "Přihlášení, CSRF a oprávnění: komu Django dovolí měnit článek": {
        "learning_goal": "Ochráním vytvoření záznamu přihlášením a úpravu vlastnictvím objektu.",
        "code_example": """@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    return render(request, "blog/post_edit.html", {"post": post})

<form method="post">{% csrf_token %}</form>""",
        "code_explanation": "login_required vyžaduje přihlášení. Filtr author=request.user zabrání úpravě cizího objektu. CSRF token chrání POST formulář.",
        "practice_task": "Přihlas dva uživatele a ověř, že druhý nemůže upravit článek prvního.",
    },
    "Šablony a statické soubory: obsah a vzhled odděleně": {
        "learning_goal": "Použiji dědičnost šablon a korektně načtu CSS.",
        "code_example": """{% extends "blog/base.html" %}
{% load static %}
{% block content %}
<link rel="stylesheet" href="{% static 'blog/css/site.css' %}">
<h1>{{ title }}</h1>
{% endblock %}""",
        "code_explanation": "extends převezme společný vzhled, block vyplní měnící se část a static vytvoří správnou URL i po nasazení.",
        "practice_task": "Vytvoř base.html a dvě stránky, které ji rozšiřují. Barvu navigace změň pouze v CSS.",
    },
    "Django formulář: validace dřív, než data uložíš": {
        "learning_goal": "Zpracují GET a POST pomocí ModelForm a zobrazím chyby validace.",
        "code_example": """if request.method == "POST":
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("post_detail", pk=post.pk)
else:
    form = PostForm()""",
        "code_explanation": "GET vytvoří prázdný formulář. POST jej naplní. commit=False dovolí nastavit autora mimo vstup návštěvníka.",
        "practice_task": "Přidej povinné pole a pošli prázdný formulář. Zkontroluj, zda šablona zobrazí chybu.",
    },
    "Automatické testy: důkaz, že změna nic nerozbila": {
        "learning_goal": "Napíšu test URL a bezpečnostního pravidla pomocí Django TestCase.",
        "code_example": """def test_post_create_requires_login(self):
    response = self.client.get(reverse("post_new"))

    self.assertEqual(response.status_code, 302)
    self.assertIn(reverse("login"), response.url)""",
        "code_explanation": "Testovací klient simuluje návštěvníka. Stav 302 ověřuje přesměrování na přihlášení.",
        "practice_task": "Napiš test pro chybnou URL nebo pravidlo svého závěrečného projektu.",
    },
    "Django nebo Flask? Jak vybrat framework pro projekt": {
        "learning_goal": "Porovnám Django a Flask podle rozsahu projektu a potřebných komponent.",
        "code_example": """# Flask: velmi malý začátek
from flask import Flask
app = Flask(__name__)

@app.get("/")
def home():
    return "Ahoj z Flasku"

# Django: URL je samostatně v urls.py
path("", views.post_list, name="post_list")""",
        "code_explanation": "Flask definuje trasu dekorátorem a je stručný. Django odděluje URL a view, ale obsahuje navíc modely, admin, formuláře a účty.",
        "practice_task": "Pro blog, JSON API a rezervační systém zvol Django nebo Flask a volbu obhaj dvěma důvody.",
    },
    "Závěrečný projekt: od nápadu k odevzdání": {
        "learning_goal": "Dokončím vlastní Django aplikaci s databází, formulářem, testem a nasazením.",
        "code_example": """# Uživatelský scénář
# Jako přihlášený žák chci přidat knihu,
# abych ji mohl doporučit spolužákům.

# Entity: Book, Recommendation
# Pravidlo: upravovat doporučení smí jen jeho autor.""",
        "code_explanation": "Scénář určí uživatele a přínos. Entity se stanou modely a pravidlo ověříš ve view i testu.",
        "practice_task": "Odevzdej repozitář, nasazenou aplikaci, README a prezentaci jednoho modelu, formuláře a testu.",
    },
}


class Command(BaseCommand):
    help = "Create original Czech Django lessons for the student blog."

    def add_arguments(self, parser):
        parser.add_argument(
            "--refresh",
            action="store_true",
            help="Update existing sample lessons created for the django_start account.",
        )

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
            ("architektura", "Architektura webu"),
            ("formular", "Formuláře a účty"),
            ("testovani", "Testování"),
            ("frameworky", "Frameworky"),
        ):
            categories[slug], _ = Category.objects.get_or_create(name=name, slug=slug)

        now = timezone.now()
        created_count = 0
        updated_count = 0
        for lesson in LESSONS:
            defaults = {
                "category": categories[lesson["category"]],
                "text": lesson["text"],
                "published_date": now - timedelta(days=lesson["days_ago"]),
                **MATERIALS.get(lesson["title"], {}),
            }
            post, created = Post.objects.get_or_create(
                author=author,
                title=lesson["title"],
                defaults=defaults,
            )
            created_count += created
            if options["refresh"] and not created:
                for field, value in defaults.items():
                    setattr(post, field, value)
                post.save(update_fields=defaults.keys())
                updated_count += 1

        if author_created:
            self.stdout.write("Created the disabled author account django_start.")
        self.stdout.write(
            self.style.SUCCESS(
                f"Learning content ready: {created_count} new, {updated_count} updated, "
                f"{len(LESSONS) - created_count - updated_count} already present."
            )
        )
