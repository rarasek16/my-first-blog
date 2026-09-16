# Technical stand-up report: DjangoStart

**Date:** 16. září 2026
**Tested commit:** `251b6d9`
**Branch:** `copilot/basic-task-for-high-school-students`
**Runtime environment:** Windows, Python 3.12.6, Django 5.1.1, SQLite
**Scope:** výukový blog, registrace a přihlášení, role administrátora, bonusová zóna, přístupnost, lokální demo data.

## Stand-up status

| Area | Status | Evidence |
|---|---|---|
| Learning content | DONE | 11 lekcí v 8 kategoriích, z toho 8 lekcí s cílem, ukázkou kódu, výkladem a úkolem |
| Standard user | DONE | Registrace, přihlášení, bonusová zóna a testovací materiály; správa článků je nepřístupná |
| Content administrator | DONE | Pouze `is_staff=True` může vytvořit a upravit vlastní článek; cizí článek vrací `404` |
| Administration | DONE | Lokální účet `admin_demo` úspěšně otevře `/admin/` |
| Bonus content | DONE | `/bonus/` vyžaduje přihlášení; anonymní návštěvník dostává `302`, přihlášený uživatel `200` |
| Accessibility | TECHNICAL BASELINE COMPLETE | Přeskočení navigace, fokus, sémantika, responzivita, formulářové chyby, omezení animací a `/pristupnost/` |
| Local demo | DONE | Migrace, seed obsahu a čtyři lokální účty vytvořeny příkazy Djanga |
| Production deployment | PARTIALLY READY | Existuje produkční nastavení, ale zbývá vyřešit otevřená rizika níže |

## Automated tests

Poslední úplné spuštění:

```text
python manage.py test
Ran 29 tests in 1.582s
OK
```

| Test area | Verification | Result |
|---|---|---|
| `Post` model | `publish()` nastaví datum publikace | PASS |
| Post form | Povinná data projdou validací | PASS |
| Learning-content seed | Vytvoří 11 lekcí a 8 kategorií; opakované spuštění data neduplikuje | PASS |
| Seed refresh | `seed_django_lessons --refresh` obnoví výuková pole vzorových lekcí | PASS |
| Public list | Zobrazuje pouze publikované články | PASS |
| Category filter | Filtrování článků podle kategorie | PASS |
| Post detail | Neveřejný koncept vrací `404` | PASS |
| Template accessibility | Odkaz pro přeskočení navigace, ARIA popisy formuláře a prohlášení o přístupnosti | PASS |
| Post creation | Nepřihlášený návštěvník je přesměrován; student dostane `403`; správce je nastaven jako autor | PASS |
| Post editing | Student dostane `403`; správce může upravit vlastní článek, ale cizí článek vrací `404` | PASS |
| Registration | Nový uživatel vznikne, je přihlášen a vrácen na úvod | PASS |
| Bonus zone | Anonymní návštěvník je přesměrován, přihlášený má přístup | PASS |
| Role-based navigation | Student nevidí formulář článku; správce odkaz vidí | PASS |
| Demo accounts | Příkaz odmítne produkční nastavení; vývojový příkaz vytvoří administrátora a lokální soubor s údaji | PASS |

## Integration a manual validation

| Check | Command / procedure | Result |
|---|---|---|
| Configuration check | `python manage.py check` | PASS |
| Database migrations | `python manage.py migrate --noinput` | PASS |
| Learning content | `python manage.py seed_django_lessons` | PASS |
| Demo accounts | `python manage.py create_demo_accounts` | PASS |
| Administrator login | Test client s údaji z lokálního souboru otevřel `/admin/` | PASS |
| Bonus zone | Lokální server a HTTP kontrola `/bonus/` | PASS |
| Static assets | `findstatic blog/css/site.css` a HTTP kontrola JavaScriptu | PASS |
| Audio reader | Check načtení `speechSynthesis` skriptu | PASS with browser-dependent voice availability |
| Source formatting | `git diff --check` | PASS |
| Demo credential protection | Check `git status --short` před commitem | PASS |

## Severity scale

| Score | Severity | Expected action |
|---|---|---|
| 5/5 - Critical | Umožňuje závažné zneužití nebo blokuje provoz | Fix before deployment |
| 4/5 - High | Významné bezpečnostní, právní nebo funkční riziko | Fix before public production |
| 3/5 - Medium | Omezuje kvalitu, kompatibilitu nebo spolehlivost | Schedule for the next iteration |
| 2/5 - Low | Dopad je omezený a existuje rozumný postup obejití | Address according to priority |
| 1/5 - Informational | Doporučení ke zlepšení bez aktuálního dopadu | Track |

## Open risks and recommendations

| # | Severity | Area | Finding | Recommended action |
|---|---:|---|---|---|
| 1 | High | Public registration | Registrace nemá ověření e-mailu, rate limiting ani ochranu proti automatizovanému zakládání účtů. | Před veřejným provozem přidat ověření e-mailu, omezení pokusů a vhodnou ochranu proti botům. |
| 2 | Medium | Dependency versioning | `requirements.txt` uvádí `Django~=4.2.11`, ale ověřené prostředí běží na Django 5.1.1. | Rozhodnout cílovou verzi, upravit `requirements.txt` a otestovat nasazení se stejnou verzí. |
| 3 | Medium | Production configuration | Produkční nastavení existuje, ale je nutné v PythonAnywhere skutečně nastavit `DJANGO_SETTINGS_MODULE=mysite.settings_prod`, `DJANGO_SECRET_KEY` a `DJANGO_ALLOWED_HOSTS`. | Nastavit proměnné prostředí, vypnout `DEBUG`, spustit `check --deploy` a provést nasazovací kontrolu. |
| 4 | Medium | Formal accessibility | Automatické testy ověřují technické prvky, ne skutečné použití čtečkou obrazovky, klávesnicí nebo s uživateli. | Doplnit kontaktní údaj do prohlášení a provést nezávislý audit WCAG 2.2 AA/EN 301 549. |
| 5 | Low | Audio reader | Web Speech API a české hlasy nejsou dostupné ve všech prohlížečích a zařízeních. | Zachovat textový obsah jako primární zdroj; otestovat Chrome, Edge, Firefox a mobilní prohlížeče s reálnou čtečkou. |
| 6 | Low | SQLite | SQLite je vhodná pro výuku a malý provoz, ale při souběžných zápisech škáluje omezeně. | Pro větší počet aktivních uživatelů naplánovat přechod na PostgreSQL nebo MySQL. |
| 7 | Informational | Demo credentials | Demo účty se po opakovaném příkazu zaheslují novými náhodnými hesly. | Při opakovaném spuštění vždy použít aktuální `local/demo-accounts.txt`; soubor nesdílet ani nenasazovat. |

## Next steps

1. Na PythonAnywhere sjednotit verzi Djanga se souborem závislostí a dokončit produkční konfiguraci.
2. Před veřejnou registrací implementovat ověření e-mailu a ochranu proti zneužití.
3. Provést ruční přístupnostní test s klávesnicí, čtečkou obrazovky a alespoň jedním mobilním zařízením.
4. V Moodlu vytvořit pro každý modul kvíz a odevzdávárnu, zatímco DjangoStart zůstane referenčním výukovým webem.
