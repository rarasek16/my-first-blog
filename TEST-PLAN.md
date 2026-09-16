# Test plan: DjangoStart

**Plan version:** 1.0
**Date:** 16. září 2026
**Test objective:** ověřit, že výukový web DjangoStart poskytuje funkční, bezpečný a přístupný tok od veřejného obsahu přes registraci až po chráněné bonusové úkoly a správu obsahu.

Tento plán vychází z průmyslově používaných standardů a metodik testování: z testování řízeného riziky, oddělení úrovní testu, návrhových technik, dohledatelnosti a jasných kritérií vstupu a výstupu.

## 1. Scope

| In scope | Out of scope |
|---|---|
| Veřejné články, filtry kategorií, koncepty a detail článku | Platební brána nebo skutečný komerční premium model |
| Registrace, přihlášení, odhlášení a oprávnění autora | E-mailové ověření a externí poskytovatelé identity |
| Bonusová zóna pro přihlášené uživatele | Zátěžový test velkého počtu souběžných uživatelů |
| Django admin a lokální demo účty | Produkční PythonAnywhere konfigurace provozovatele |
| Formulář článku, validace a výukové materiály | Právní certifikace přístupnosti |
| Přístupnost rozhraní a hlasové čtení ve Web Speech API | Test fyzického hardwaru, lokálních hlasů a všech kombinací prohlížečů |

## 2. Test levels and responsibilities

| Test level | Responsibility | Tool / procedure | Deliverable |
|---|---|---|---|
| Unit and component | Vývoj | Django `TestCase`, testovací databáze | Result `python manage.py test` |
| Integration | Vývoj | migrace, seed příkazy, Django test client | Ověřené HTTP stavy a vytvořená data |
| System | Vývoj + vyučující | lokální server, ruční scénáře | Checklist výsledků |
| Acceptance | Vyučující | studenti podle zadání bonusových úkolů | Přijaté projekty a zpětná vazba |
| Accessibility | Vyučující + nezávislý tester | klávesnice, čtečka obrazovky, mobilní prohlížeč | Záznam bariér a opravných kroků |

## 3. Risk analysis

| ID | Risk | Impact | Likelihood | Score | Priority |
|---|---|---:|---:|---:|---|
| R-01 | Nepřihlášený nebo studentský účet získá formulář pro správu článků | 5 | 2 | 10 | High |
| R-02 | Správce upraví cizí článek | 5 | 2 | 10 | High |
| R-03 | Neplatná registrace vytvoří nefunkční účet | 4 | 3 | 12 | Critical |
| R-04 | Demo hesla se dostanou do repozitáře nebo produkce | 5 | 2 | 10 | High |
| R-05 | Výukové materiály se při seedování zdvojí | 3 | 3 | 9 | Medium |
| R-06 | Žák se nedostane k obsahu klávesnicí nebo čtečkou | 4 | 2 | 8 | Medium |
| R-07 | Audio čtení naruší běžné použití stránky | 2 | 2 | 4 | Low |

**Score calculation:** Impact (1–5) × Likelihood (1–5). Hodnota 10–25 znamená High priority, 6–9 Medium a 1–5 Low.

## 4. Test design techniques

| Technique | Usage |
|---|---|
| Equivalence partitioning | platná / neplatná registrace, anonymní / student / správce |
| Boundary value analysis | prázdná povinná pole, délka a shoda hesel, prázdné vyhledávání |
| Decision table testing | přístup k vytvoření, úpravě a bonusové zóně podle role a vlastnictví |
| State transition testing | anonymní návštěvník → registrovaný → přihlášený → odhlášený |
| Use case testing | vytvoření článku, otevření administrace, vypracování bonusového úkolu |
| Exploratory testing | ovládání klávesnicí, mobilní rozvržení, čtečka obrazovky a hlasové čtení |

## 5. Test cases a traceability

| ID | Risk | Scenario | Expected result | Automation | Priority |
|---|---|---|---|---|---|
| TC-01 | R-01 | Anonymní návštěvník otevře `/post/new/` | Přesměrování na přihlášení | Yes | High |
| TC-02 | R-01 | Anonymní návštěvník otevře `/bonus/` | Přesměrování na přihlášení | Yes | High |
| TC-03 | R-01 | Přihlášený uživatel otevře `/bonus/` | Status `200`, zobrazí se zadání | Yes | High |
| TC-04 | R-02 | Jiný uživatel otevře URL pro úpravu cizího článku | Status `404` | Yes | High |
| TC-05 | R-03 | Nový uživatel zadá platné shodné heslo | Účet vznikne a uživatel je přihlášen | Yes | Critical |
| TC-06 | R-03 | Nový uživatel zadá rozdílná hesla | Formulář vrátí chybu, účet nevznikne | Yes | Critical |
| TC-07 | R-04 | Příkaz demo účtů běží v produkčním nastavení | Příkaz skončí `CommandError` | Yes | High |
| TC-08 | R-04 | Příkaz demo účtů běží v režimu vývoje | Vzniknou 3 studenty + správce, soubor je v `local/` | Yes | High |
| TC-09 | R-05 | Seed spustíme opakovaně | Obsah a kategorie se nezdvojí | Yes | Medium |
| TC-10 | R-06 | Klávesnice vstoupí na úvodní stránku | První odkaz přeskočí navigaci na hlavní obsah | Yes + manual | Medium |
| TC-11 | R-06 | Otevření formuláře článku | Pole mají labely, popis a místo pro chybu | Yes + manual | Medium |
| TC-12 | R-07 | Prohlížeč podporuje / nepodporuje Web Speech API | K dispozici jsou ovladače nebo srozumitelná informace | Load automation + manual | Low |
| TC-13 | Functional | `admin_demo` se přihlásí na `/admin/` | Úspěšný přístup administrátora | Yes | High |
| TC-14 | R-01 | Studentský účet otevře `/post/new/` | Status `403`; formulář a odkaz v navigaci nejsou dostupné | Yes | High |
| TC-15 | R-01 | Správce odešle minimální formulář článku | Článek je uložen s aktuálním správcem | Yes | High |
| TC-16 | R-01 | Studentský účet otevře vlastní `/post/<pk>/edit/` | Status `403` | Yes | High |
| TC-17 | R-02 | Správce otevře URL pro úpravu cizího článku | Status `404` | Yes | High |
| TC-18 | Functional | Správce upraví vlastní článek | Změněný článek je uložen | Yes | High |

## 6. Test data

| Dataset | Content | Usage |
|---|---|---|
| TD-01 | `author`, `other` | ověření vlastnictví článků |
| TD-02 | publikovaný článek a koncept | seznam a ochrana konceptů |
| TD-03 | kategorie Python a Web | filtrování |
| TD-04 | `ada_demo`, `bruno_demo`, `cyril_demo`, `admin_demo` | lokální demonstrace účtů |
| TD-05 | 11 seed lekcí a 8 kategorií | výukový obsah a idempotence seeding |

Demo hesla vznikají náhodně pouze ve vývojové databázi; nesmějí se zapsat do test plánu, reportu, repozitáře ani veřejného nasazení.

## 7. Entry and exit criteria

**Entry criteria**

1. Pracovní větev je aktuální a bez necommitnutých změn nesouvisejících s testem.
2. Je dostupné virtuální prostředí a závislosti z `requirements.txt`.
3. Migrace lze aplikovat na čistou SQLite databázi.
4. Test data se vytvářejí izolovaně a produkční data nejsou používána.

**Exit criteria**

1. `python manage.py test` skončí bez selhání.
2. `python manage.py check` nehlásí problém.
3. Všechny automatizovatelné test cases s High a Critical priority skončí PASS.
4. Žádné otevřené kritické riziko nezůstane bez plánu nápravy.
5. Ruční přístupnostní a prohlížečové kontroly jsou zaznamenány před veřejným nasazením.

## 8. Test environment, reporting and closure

Automatické testy poběží přes Django TestCase na dočasné databázi. Integration test běží v izolované lokální pracovní kopii. Výsledky se zapisují do `TEST-REPORT.md`; nalezené defects se evidují s ID, kroky reprodukce, očekávaným a skutečným výsledkem a priority.

Testování se ukončí po splnění výstupních kritérií nebo po zaznamenání blokující vady. Formální akceptaci veřejného nasazení dává provozovatel až po produkční konfiguraci, bezpečnostním review registrace a ručním přístupnostním auditu.
