# Technický stand-up report: DjangoStart

**Datum:** 16. září 2026  
**Testovaný commit:** `251b6d9`
**Větev:** `copilot/basic-task-for-high-school-students`  
**Běhové prostředí:** Windows, Python 3.12.6, Django 5.1.1, SQLite  
**Rozsah:** výukový blog, registrace a přihlášení, role administrátora, bonusová zóna, přístupnost, lokální demo data.

## Stav pro stand-up

| Oblast | Stav | Důkaz |
|---|---|---|
| Výukový obsah | Hotovo | 11 lekcí v 8 kategoriích, z toho 8 lekcí s cílem, ukázkou kódu, výkladem a úkolem |
| Běžný uživatel | Hotovo | Registrace, přihlášení, bonusová zóna a testovací materiály; správa článků je nepřístupná |
| Správce obsahu | Hotovo | Pouze `is_staff=True` může vytvořit a upravit vlastní článek; cizí článek vrací `404` |
| Administrace | Hotovo | Lokální účet `admin_demo` úspěšně otevře `/admin/` |
| Bonusový obsah | Hotovo | `/bonus/` vyžaduje přihlášení; anonymní návštěvník dostává `302`, přihlášený uživatel `200` |
| Přístupnost | Technický základ hotov | Přeskočení navigace, fokus, sémantika, responzivita, formulářové chyby, omezení animací a `/pristupnost/` |
| Lokální demo | Hotovo | Migrace, seed obsahu a čtyři lokální účty vytvořeny příkazy Djanga |
| Nasazení do produkce | Částečně připraveno | Existuje produkční nastavení, ale zbývá vyřešit otevřená rizika níže |

## Provedené automatické testy

Poslední úplné spuštění:

```text
python manage.py test
Ran 29 tests in 1.582s
OK
```

| Testovaná oblast | Co bylo ověřeno | Výsledek |
|---|---|---|
| Model `Post` | `publish()` nastaví datum publikace | Prošlo |
| Formulář článku | Povinná data projdou validací | Prošlo |
| Seed výukového obsahu | Vytvoří 11 lekcí a 8 kategorií; opakované spuštění data neduplikuje | Prošlo |
| Obnova seed obsahu | `seed_django_lessons --refresh` obnoví výuková pole vzorových lekcí | Prošlo |
| Veřejný seznam | Zobrazuje pouze publikované články | Prošlo |
| Kategorie | Filtrování článků podle kategorie | Prošlo |
| Detail článku | Neveřejný koncept vrací `404` | Prošlo |
| Přístupnost šablon | Odkaz pro přeskočení navigace, ARIA popisy formuláře a prohlášení o přístupnosti | Prošlo |
| Vytvoření článku | Nepřihlášený návštěvník je přesměrován; student dostane `403`; správce je nastaven jako autor | Prošlo |
| Úprava článku | Student dostane `403`; správce může upravit vlastní článek, ale cizí článek vrací `404` | Prošlo |
| Registrace | Nový uživatel vznikne, je přihlášen a vrácen na úvod | Prošlo |
| Bonusová zóna | Anonymní návštěvník je přesměrován, přihlášený má přístup | Prošlo |
| Navigace podle role | Student nevidí formulář článku; správce odkaz vidí | Prošlo |
| Demo účty | Příkaz odmítne produkční nastavení; vývojový příkaz vytvoří administrátora a lokální soubor s údaji | Prošlo |

## Provedené integrační a manuální validace

| Kontrola | Příkaz / postup | Výsledek |
|---|---|---|
| Kontrola konfigurace | `python manage.py check` | Bez nalezených problémů |
| Databázové změny | `python manage.py migrate --noinput` | Všechny migrace aplikovány |
| Výuková data | `python manage.py seed_django_lessons` | 11 lekcí, 8 kategorií, 8 ukázek kódu |
| Demo účty | `python manage.py create_demo_accounts` | 3 studenti + `admin_demo`; hesla pouze v `local/demo-accounts.txt` |
| Přihlášení administrátora | Testovací klient s údaji z lokálního souboru otevřel `/admin/` | `admin_login=True`, `admin_page=200` |
| Bonusová zóna | Lokální server a HTTP kontrola `/bonus/` | anonymní `302`, přihlášený `200` |
| Statické soubory | `findstatic blog/css/site.css` a HTTP kontrola JavaScriptu | CSS i `audio-reader.js` nalezeny a servírovány |
| Hlasové čtení | Kontrola načtení `speechSynthesis` skriptu | JavaScript je servírován; skutečný hlas závisí na prohlížeči a nainstalovaném hlasu |
| Formát zdrojů | `git diff --check` | Bez chyb bílých znaků |
| Ochrana demo hesel | Kontrola `git status --short` před commitem | `local/demo-accounts.txt` nebyl sledován Gitem |

## Stupnice závažnosti

| Skóre | Význam | Očekávaná reakce |
|---|---|---|
| 5/5 - kritické | Umožňuje závažné zneužití nebo blokuje provoz | Opravit před nasazením |
| 4/5 - vysoké | Významné bezpečnostní, právní nebo funkční riziko | Opravit před veřejným provozem |
| 3/5 - střední | Omezuje kvalitu, kompatibilitu nebo spolehlivost | Naplánovat do nejbližší iterace |
| 2/5 - nízké | Dopad je omezený a existuje rozumný postup obejití | Řešit podle priority |
| 1/5 - informativní | Doporučení ke zlepšení bez aktuálního dopadu | Evidovat |

## Otevřená rizika a doporučení

| # | Závažnost | Oblast | Zjištění | Doporučené opatření |
|---|---:|---|---|---|
| 1 | 4/5 | Veřejná registrace | Registrace nemá ověření e-mailu, rate limiting ani ochranu proti automatizovanému zakládání účtů. | Před veřejným provozem přidat ověření e-mailu, omezení pokusů a vhodnou ochranu proti botům. |
| 2 | 3/5 | Verzování závislostí | `requirements.txt` uvádí `Django~=4.2.11`, ale ověřené prostředí běží na Django 5.1.1. | Rozhodnout cílovou verzi, upravit `requirements.txt` a otestovat nasazení se stejnou verzí. |
| 3 | 3/5 | Produkční konfigurace | Produkční nastavení existuje, ale je nutné v PythonAnywhere skutečně nastavit `DJANGO_SETTINGS_MODULE=mysite.settings_prod`, `DJANGO_SECRET_KEY` a `DJANGO_ALLOWED_HOSTS`. | Nastavit proměnné prostředí, vypnout `DEBUG`, spustit `check --deploy` a provést nasazovací kontrolu. |
| 4 | 3/5 | Formální přístupnost | Automatické testy ověřují technické prvky, ne skutečné použití čtečkou obrazovky, klávesnicí nebo s uživateli. | Doplnit kontaktní údaj do prohlášení a provést nezávislý audit WCAG 2.2 AA/EN 301 549. |
| 5 | 2/5 | Hlasové čtení | Web Speech API a české hlasy nejsou dostupné ve všech prohlížečích a zařízeních. | Zachovat textový obsah jako primární zdroj; otestovat Chrome, Edge, Firefox a mobilní prohlížeče s reálnou čtečkou. |
| 6 | 2/5 | SQLite | SQLite je vhodná pro výuku a malý provoz, ale při souběžných zápisech škáluje omezeně. | Pro větší počet aktivních uživatelů naplánovat přechod na PostgreSQL nebo MySQL. |
| 7 | 1/5 | Demo údaje | Demo účty se po opakovaném příkazu zaheslují novými náhodnými hesly. | Při opakovaném spuštění vždy použít aktuální `local/demo-accounts.txt`; soubor nesdílet ani nenasazovat. |

## Další doporučený krok

1. Na PythonAnywhere sjednotit verzi Djanga se souborem závislostí a dokončit produkční konfiguraci.
2. Před veřejnou registrací implementovat ověření e-mailu a ochranu proti zneužití.
3. Provést ruční přístupnostní test s klávesnicí, čtečkou obrazovky a alespoň jedním mobilním zařízením.
4. V Moodlu vytvořit pro každý modul kvíz a odevzdávárnu, zatímco DjangoStart zůstane referenčním výukovým webem.
