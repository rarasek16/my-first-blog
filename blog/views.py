from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import PostForm, RegistrationForm
from .models import Category, Post


COURSE_MODULES = (
    {
        "number": "01",
        "title": "Start a nástroje",
        "outcome": "Připravím Python, virtuální prostředí, Git a první Django projekt.",
    },
    {
        "number": "02",
        "title": "Webová architektura",
        "outcome": "Vysvětlím cestu požadavku od URL přes view až po šablonu.",
    },
    {
        "number": "03",
        "title": "Data a databáze",
        "outcome": "Navrhnu model, vytvořím migraci a pracuji s daty v adminu.",
    },
    {
        "number": "04",
        "title": "Formuláře a účty",
        "outcome": "Vytvořím validovaný formulář a rozliším přihlášení od oprávnění.",
    },
    {
        "number": "05",
        "title": "Kvalita a bezpečnost",
        "outcome": "Napíšu testy a umím vysvětlit ochranu CSRF i práci s chybami.",
    },
    {
        "number": "06",
        "title": "Volba nástroje a nasazení",
        "outcome": "Porovnám Django s Flaskem a bezpečně zveřejním hotový projekt.",
    },
)

BONUS_TASKS = (
    {
        "number": "01",
        "title": "Katalog knih pro třídu",
        "level": "Databáze a administrace",
        "description": "Vytvoř model Book s názvem, autorem, rokem vydání a dostupností. Zaregistruj jej v adminu a zobraz knihy na veřejné stránce.",
        "success": "Katalog zobrazuje data z databáze, umí filtrovat dostupné knihy a každá kniha má detailní stránku.",
        "joke": "Kniha bez migrace je jako knihovna bez katalogu: možná tam je, ale nikdo ji nenajde.",
    },
    {
        "number": "02",
        "title": "Bezpečná školní nástěnka",
        "level": "Formuláře a oprávnění",
        "description": "Přidej oznámení, které může vytvořit přihlášený uživatel. Autor smí upravit nebo smazat jen vlastní oznámení.",
        "success": "Formulář validuje data, používá CSRF token a test ověří, že cizí oznámení nelze upravit.",
        "joke": "Neoprávněná úprava cizího příspěvku není spolupráce. Je to 403 s dramatickou hudbou.",
    },
    {
        "number": "03",
        "title": "Hledání bez chaosu",
        "level": "QuerySety a uživatelské rozhraní",
        "description": "Doplň vyhledávání podle názvu a kategorii. Prázdný hledaný výraz nesmí rozbít stránku ani zobrazit chybu databáze.",
        "success": "Výsledky odpovídají zadání, URL jde sdílet a prázdný stav nabízí uživateli srozumitelný další krok.",
        "joke": "SELECT * je občas rychlý začátek. Stejně jako věta „určitě to funguje“ před spuštěním testů.",
    },
    {
        "number": "04",
        "title": "Nasazení s klidnou hlavou",
        "level": "Testování a produkce",
        "description": "Připrav projekt k nasazení: přidej README, spusť testy, nastav proměnné prostředí a zkontroluj chybové stránky.",
        "success": "Repozitář obsahuje návod, testy procházejí, tajné údaje nejsou v Gitu a nasazená aplikace má správné ALLOWED_HOSTS.",
        "joke": "DEBUG=True v produkci je jako nechat učebnu otevřenou po zvonění: někdo tam vždy najde něco, co neměl.",
    },
)

TESTING_STAGES = (
    ("01", "Plánuj", "Vymez cíl, rozsah, rizika, prostředí a kritéria hotového testování."),
    ("02", "Navrhuj", "Převeď požadavky na testovací scénáře, data a očekávané výsledky."),
    ("03", "Prováděj", "Spusť automatické i ruční testy, porovnej skutečný a očekávaný výsledek."),
    ("04", "Reportuj", "Zapiš stav, vady, závažnost, důkazy a doporučení pro další krok."),
)

TEST_SCENARIOS = (
    {
        "id": "TS-01",
        "risk": "4/5",
        "title": "Přístup do bonusové zóny",
        "precondition": "Návštěvník není přihlášen.",
        "steps": "Otevři /bonus/ v anonymním okně prohlížeče.",
        "expected": "Aplikace přesměruje návštěvníka na přihlášení a po přihlášení vrátí do bonusové zóny.",
    },
    {
        "id": "TS-02",
        "risk": "5/5",
        "title": "Registrace s rozdílnými hesly",
        "precondition": "Uživatelské jméno ještě v databázi neexistuje.",
        "steps": "Vyplň registraci a do obou polí zadej různá hesla.",
        "expected": "Formulář zobrazí chybu a nový účet nevznikne.",
    },
    {
        "id": "TS-03",
        "risk": "4/5",
        "title": "Ochrana cizího článku",
        "precondition": "Existují dva přihlášení uživatelé a článek autora A.",
        "steps": "Jako uživatel B otevři URL pro úpravu článku autora A.",
        "expected": "Aplikace vrátí 404; uživatel B nemůže data zobrazit ani změnit.",
    },
    {
        "id": "TS-04",
        "risk": "3/5",
        "title": "Publikování a koncept",
        "precondition": "Existuje publikovaný článek i koncept bez data publikování.",
        "steps": "Otevři úvodní seznam a detail konceptu.",
        "expected": "Seznam obsahuje jen publikovaný článek; detail konceptu vrátí 404.",
    },
)

REPORT_RISKS = (
    ("4/5", "Veřejná registrace", "Před veřejným provozem doplnit ověření e-mailu a omezení pokusů."),
    ("3/5", "Verze Djanga", "Sjednotit verzi v requirements.txt s ověřeným produkčním prostředím."),
    ("3/5", "Produkční konfigurace", "Nastavit proměnné prostředí a spustit check --deploy."),
    ("3/5", "Formální přístupnost", "Doplnit kontakt a provést nezávislý audit s asistivními technologiemi."),
    ("2/5", "Hlasové čtení", "Ověřit český hlas ve vybraných prohlížečích a zařízeních."),
)


def navigation_context():
    return {"categories": Category.objects.all()}


def post_list(request, category_slug=None):
    posts = (
        Post.objects.filter(published_date__lte=timezone.now())
        .select_related("author", "category")
        .order_by("-published_date")
    )
    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=selected_category)

    return render(
        request,
        "blog/post_list.html",
        {
            **navigation_context(),
            "posts": posts,
            "selected_category": selected_category,
            "course_modules": COURSE_MODULES,
        },
    )


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, published_date__lte=timezone.now())
    return render(request, "blog/post_detail.html", {**navigation_context(), "post": post})


def accessibility_statement(request):
    return render(request, "blog/accessibility_statement.html", navigation_context())


@login_required
def bonus_tasks(request):
    return render(request, "blog/bonus_tasks.html", {"bonus_tasks": BONUS_TASKS})


@login_required
def testing_lab(request):
    return render(
        request,
        "blog/testing_lab.html",
        {"testing_stages": TESTING_STAGES, "test_scenarios": TEST_SCENARIOS},
    )


@login_required
def testing_reports(request):
    return render(
        request,
        "blog/testing_reports.html",
        {"test_scenarios": TEST_SCENARIOS, "report_risks": REPORT_RISKS},
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("post_list")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("post_list")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.published_date is None:
                post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(
        request,
        "blog/post_edit.html",
        {**navigation_context(), "form": form, "is_edit": False},
    )


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.published_date is None:
                post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(
        request,
        "blog/post_edit.html",
        {**navigation_context(), "form": form, "is_edit": True, "post": post},
    )


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)
