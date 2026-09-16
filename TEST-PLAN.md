# Test plan: DjangoStart

**Verze plánu:** 1.0  
**Datum:** 16. září 2026  
**Cíl testování:** ověřit, že výukový web DjangoStart poskytuje funkční, bezpečný a přístupný tok od veřejného obsahu přes registraci až po chráněné bonusové úkoly a správu obsahu.

Tento plán vychází z průmyslově používaných standardů a metodik testování: z testování řízeného riziky, oddělení úrovní testu, návrhových technik, dohledatelnosti a jasných kritérií vstupu a výstupu.

## 1. Rozsah

| V rozsahu | Mimo rozsah |
|---|---|
| Veřejné články, filtry kategorií, koncepty a detail článku | Platební brána nebo skutečný komerční premium model |
| Registrace, přihlášení, odhlášení a oprávnění autora | E-mailové ověření a externí poskytovatelé identity |
| Bonusová zóna pro přihlášené uživatele | Zátěžový test velkého počtu souběžných uživatelů |
| Django admin a lokální demo účty | Produkční PythonAnywhere konfigurace provozovatele |
| Formulář článku, validace a výukové materiály | Právní certifikace přístupnosti |
| Přístupnost rozhraní a hlasové čtení ve Web Speech API | Test fyzického hardwaru, lokálních hlasů a všech kombinací prohlížečů |

## 2. Test levels a odpovědnosti

| Test level | Zodpovědnost | Nástroj / postup | Výstup |
|---|---|---|---|
| Unit and component | Vývoj | Django `TestCase`, testovací databáze | Výsledek `python manage.py test` |
| Integration | Vývoj | migrace, seed příkazy, Django test client | Ověřené HTTP stavy a vytvořená data |
| System | Vývoj + vyučující | lokální server, ruční scénáře | Checklist výsledků |
| Acceptance | Vyučující | studenti podle zadání bonusových úkolů | Přijaté projekty a zpětná vazba |
| Accessibility | Vyučující + nezávislý tester | klávesnice, čtečka obrazovky, mobilní prohlížeč | Záznam bariér a opravných kroků |

## 3. Riziková analýza

| ID | Riziko | Dopad | Pravděpodobnost | Skóre | Priorita |
|---|---|---:|---:|---:|---|
| R-01 | Nepřihlášený nebo studentský účet získá formulář pro správu článků | 5 | 2 | 10 | Vysoká |
| R-02 | Správce upraví cizí článek | 5 | 2 | 10 | Vysoká |
| R-03 | Neplatná registrace vytvoří nefunkční účet | 4 | 3 | 12 | Kritická |
| R-04 | Demo hesla se dostanou do repozitáře nebo produkce | 5 | 2 | 10 | Vysoká |
| R-05 | Výukové materiály se při seedování zdvojí | 3 | 3 | 9 | Střední |
| R-06 | Žák se nedostane k obsahu klávesnicí nebo čtečkou | 4 | 2 | 8 | Střední |
| R-07 | Audio čtení naruší běžné použití stránky | 2 | 2 | 4 | Nízká |

**Výpočet skóre:** dopad (1–5) × pravděpodobnost (1–5). Hodnota 10–25 znamená vysokou prioritu, 6–9 střední a 1–5 nízkou.

## 4. Návrhové techniky

| Technika | Použití |
|---|---|
| Ekvivalentní třídy | platná / neplatná registrace, anonymní / student / správce |
| Analýza hraničních hodnot | prázdná povinná pole, délka a shoda hesel, prázdné vyhledávání |
| Rozhodovací tabulka | přístup k vytvoření, úpravě a bonusové zóně podle role a vlastnictví |
| Stavový přechod | anonymní návštěvník → registrovaný → přihlášený → odhlášený |
| Testování podle případů použití | vytvoření článku, otevření administrace, vypracování bonusového úkolu |
| Průzkumné testování | ovládání klávesnicí, mobilní rozvržení, čtečka obrazovky a hlasové čtení |

## 5. Test cases a traceability

| ID | Riziko | Scénář | Očekávaný výsledek | Automation | Priorita |
|---|---|---|---|---|---|
| TC-01 | R-01 | Anonymní návštěvník otevře `/post/new/` | Přesměrování na přihlášení | Ano | Vysoká |
| TC-02 | R-01 | Anonymní návštěvník otevře `/bonus/` | Přesměrování na přihlášení | Ano | Vysoká |
| TC-03 | R-01 | Přihlášený uživatel otevře `/bonus/` | Stav `200`, zobrazí se zadání | Ano | Vysoká |
| TC-04 | R-02 | Jiný uživatel otevře URL pro úpravu cizího článku | Stav `404` | Ano | Vysoká |
| TC-05 | R-03 | Nový uživatel zadá platné shodné heslo | Účet vznikne a uživatel je přihlášen | Ano | Kritická |
| TC-06 | R-03 | Nový uživatel zadá rozdílná hesla | Formulář vrátí chybu, účet nevznikne | Ano | Kritická |
| TC-07 | R-04 | Příkaz demo účtů běží v produkčním nastavení | Příkaz skončí `CommandError` | Ano | Vysoká |
| TC-08 | R-04 | Příkaz demo účtů běží v režimu vývoje | Vzniknou 3 studenty + správce, soubor je v `local/` | Ano | Vysoká |
| TC-09 | R-05 | Seed spustíme opakovaně | Obsah a kategorie se nezdvojí | Ano | Střední |
| TC-10 | R-06 | Klávesnice vstoupí na úvodní stránku | První odkaz přeskočí navigaci na hlavní obsah | Ano + ručně | Střední |
| TC-11 | R-06 | Otevření formuláře článku | Pole mají labely, popis a místo pro chybu | Ano + ručně | Střední |
| TC-12 | R-07 | Prohlížeč podporuje / nepodporuje Web Speech API | K dispozici jsou ovladače nebo srozumitelná informace | Automation načtení + ručně | Nízká |
| TC-13 | Funkční | `admin_demo` se přihlásí na `/admin/` | Úspěšný přístup administrátora | Ano | Vysoká |
| TC-14 | R-01 | Studentský účet otevře `/post/new/` | Stav `403`; formulář a odkaz v navigaci nejsou dostupné | Ano | Vysoká |
| TC-15 | R-01 | Správce odešle minimální formulář článku | Článek je uložen s aktuálním správcem | Ano | Vysoká |
| TC-16 | R-01 | Studentský účet otevře vlastní `/post/<pk>/edit/` | Stav `403` | Ano | Vysoká |
| TC-17 | R-02 | Správce otevře URL pro úpravu cizího článku | Stav `404` | Ano | Vysoká |
| TC-18 | Funkční | Správce upraví vlastní článek | Změněný článek je uložen | Ano | Vysoká |

## 6. Testovací data

| Sada | Obsah | Použití |
|---|---|---|
| TD-01 | `author`, `other` | ověření vlastnictví článků |
| TD-02 | publikovaný článek a koncept | seznam a ochrana konceptů |
| TD-03 | kategorie Python a Web | filtrování |
| TD-04 | `ada_demo`, `bruno_demo`, `cyril_demo`, `admin_demo` | lokální demonstrace účtů |
| TD-05 | 11 seed lekcí a 8 kategorií | výukový obsah a idempotence seeding |

Demo hesla vznikají náhodně pouze ve vývojové databázi; nesmějí se zapsat do test plánu, reportu, repozitáře ani veřejného nasazení.

## 7. Vstupní a výstupní kritéria

**Vstupní kritéria**

1. Pracovní větev je aktuální a bez necommitnutých změn nesouvisejících s testem.
2. Je dostupné virtuální prostředí a závislosti z `requirements.txt`.
3. Migrace lze aplikovat na čistou SQLite databázi.
4. Testovací data se vytvářejí izolovaně a produkční data nejsou používána.

**Výstupní kritéria**

1. `python manage.py test` skončí bez selhání.
2. `python manage.py check` nehlásí problém.
3. Všechny automatizovatelné případy s vysokou a kritickou prioritou projdou.
4. Žádné otevřené kritické riziko nezůstane bez plánu nápravy.
5. Ruční přístupnostní a prohlížečové kontroly jsou zaznamenány před veřejným nasazením.

## 8. Prostředí, reporting a ukončení

Automatické testy poběží přes Django TestCase na dočasné databázi. Integrační test běží v izolované lokální pracovní kopii. Výsledky se zapisují do `TEST-REPORT.md`; nalezené vady se evidují s ID, kroky reprodukce, očekávaným a skutečným výsledkem a prioritou.

Testování se ukončí po splnění výstupních kritérií nebo po zaznamenání blokující vady. Formální akceptaci veřejného nasazení dává provozovatel až po produkční konfiguraci, bezpečnostním review registrace a ručním přístupnostním auditu.
