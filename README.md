# DjangoStart

Český výukový blog pro studenty IT, kteří se učí Django a základy webového vývoje. Kurz vede od přípravy nástrojů přes architekturu webu, databáze, formuláře a účty až k testování, srovnání frameworků a nasazení.

Každá výuková lekce obsahuje měřitelný cíl, výklad, ukázku kódu s vysvětlením a praktický úkol. Je tedy použitelná pro společný výklad, samostatnou práci i hodnocení. Kurz je rozdělený do šesti navazujících modulů: nástroje, architektura, databáze, formuláře a účty, kvalita a bezpečnost, volba frameworku a nasazení.

Každá výuková lekce obsahuje konkrétní cíl, výklad, ukázku kódu s vysvětlením a praktický úkol. Studenti tak mohou postupovat samostatně, zatímco vyučující může podle lekcí vést výklad, demonstraci a následnou samostatnou práci.

## Spuštění projektu

Po aktivaci virtuálního prostředí nainstaluj závislosti a aplikuj databázové migrace:

```powershell
pip install -r requirements.txt
python manage.py migrate
```

Výukový obsah přidáš příkazem:

```powershell
python manage.py seed_django_lessons
```

Příkaz je idempotentní: můžeš jej spustit opakovaně, aniž by se výukové články zdvojily nebo přepsaly. Potom aplikaci spusť:

```powershell
python manage.py runserver
```

Pro správu článků založ administrátora příkazem `python manage.py createsuperuser` a otevři `/admin/`.

## PDF reporty

Souhrnný dokument s technickým stand-up reportem, ISTQB test planem a execution reportem vytvoříš příkazem:

```powershell
python tools/generate_reports_pdf.py
```

Výstup vznikne v `reports/DjangoStart-technicke-a-testovaci-reporty.pdf`. Generátor vkládá systémový font Arial s podporou české diakritiky a načítá aktuální obsah z `TECHNICAL-REPORT.md`, `TEST-PLAN.md` a `TEST-REPORT.md`; při spuštění proto vyžaduje soubory `C:\Windows\Fonts\arial.ttf` a `arialbd.ttf`.

Pokud má výchozí PDF otevřený prohlížeč, použij jinou výstupní cestu:

```powershell
python tools/generate_reports_pdf.py --output reports/DjangoStart-technicke-a-testovaci-reporty-opraveno.pdf
```

## Oznámení konzultačních hodin

PDF pro vložení do všech Moodle kurzů vytvoříš příkazem:

```powershell
python tools/generate_consultation_hours_pdf.py
```

Výstup je v `documents/Konzultacni-hodiny.pdf`. Obsahuje pravidelné konzultační hodiny Ing. Radka Kozakoviče, Ph.D.: každé pondělí 12:35–13:20 a možnost individuální konzultace po předchozí domluvě.

## Lokální demo účty

Pouze při lokálním vývoji (`DEBUG=True`) vytvoříš tři studentské demo účty a jeden administrátorský účet příkazem:

```powershell
python manage.py create_demo_accounts
```

Vygenerovaná jména a náhodná hesla jsou uložena v `local/demo-accounts.txt`. Adresář `local/` je ignorovaný Gitem, takže přihlašovací údaje nejsou součástí repozitáře a nesmí se nasazovat ani zveřejňovat.

Účet `admin_demo` má přístup na `/admin/` a jako správce může vytvářet i upravovat vlastní články přes formulář `/post/new/`. Studentské demo účty mají přístup pouze k bonusové zóně a studijním materiálům; formulář článků ani správu článků nemají k dispozici.

Pokud chceš obnovit všechny vzorové lekce autora `django_start` na aktuální obsah kurzu, spusť:

```powershell
python manage.py seed_django_lessons --refresh
```

Tento přepínač úmyslně aktualizuje jen vzorové lekce; běžné články studentů nemění.

## Doporučená metodika

1. Na začátku modulu formulujte společně jeho cíl a aktivujte předchozí znalosti krátkou otázkou nebo miniúlohou.
2. Při výkladu spusťte ukázku kódu v připraveném projektu a nechte studenty předpovědět výsledek ještě před spuštěním.
3. Praktický úkol nechte řešit samostatně nebo ve dvojici; hodnotí se funkčnost, čitelnost a vysvětlení rozhodnutí.
4. Na konci modulu studenti odevzdají odkaz na vlastní repozitář a stručně popíšou, co fungovalo, jakou chybu potkali a jak ji opravili.

Závěrečný projekt může být blog, katalog knih, školní nástěnka, rezervační formulář nebo jednoduchá evidence. Student by měl umět navrhnout modely, vytvořit URL, view a šablony, pracovat s formulářem a přihlášením, napsat základní testy a projekt nasadit.

## Přístupnost

Rozhraní je technicky navržené podle WCAG 2.2 AA a EN 301 549: nabízí ovládání klávesnicí, odkaz pro přeskočení navigace, viditelný fokus, responzivní rozvržení, textové formulářové chyby a omezení animací podle nastavení uživatele. Veřejné prohlášení je na adrese `/pristupnost/`.

Před zveřejněním je potřeba doplnit konkrétní kontaktní údaj správce kurzu a provést nezávislý odborný audit, zejména s uživateli asistivních technologií. Teprve ten může potvrdit právní shodu pro konkrétního provozovatele a jurisdikci.

## Doporučené využití ve výuce

1. U každého modulu nejdřív ověř porozumění cíli lekce.
2. Společně projděte výklad a spusťte ukázku ve vlastním projektu.
3. Studenti vypracují praktický úkol samostatně nebo ve dvojici.
4. Výsledky odevzdají jako odkaz na GitHub repozitář a krátký popis řešení.

Závěrečným projektem může být blog, katalog knih, školní nástěnka, rezervační formulář nebo jednoduchá evidence. Žák by měl umět navrhnout modely, vytvořit URL, view a šablony, pracovat s formulářem a přihlášením, napsat základní testy a projekt nasadit.
