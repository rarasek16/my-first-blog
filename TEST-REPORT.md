# Test execution report: DjangoStart

**Datum exekuce:** 16. září 2026
**Build / větev:** `copilot/basic-task-for-high-school-students`  
**Test level:** component, integration and limited system validation
**Reference:** `TEST-PLAN.md`

## Souhrn

| Metrika | Výsledek |
|---|---:|
| Spuštěné automatické testy | 29 |
| Prošlé testy | 29 |
| Selhané testy | 0 |
| Blokované testy | 0 |
| Kontrola `python manage.py check` | Bez problémů |
| Kontrola `git diff --check` | Bez problémů |
| Doporučení pro lokální výuku | Schválit |
| Doporučení pro veřejný produkční provoz | Podmíněně schválit po vyřešení otevřených rizik |

## Výsledky podle priorit

| Priorita | Případy | Stav | Poznámka |
|---|---|---|---|
| Kritická | TC-05, TC-06 | PASS | Platná registrace vytvoří účet; rozdílná hesla účet nevytvoří. |
| Vysoká | TC-01 až TC-04, TC-07, TC-08, TC-13 až TC-18 | PASS | Chráněné cesty, role student/správce, vlastnictví článků a demo administrátor fungují podle očekávání. |
| Střední | TC-09 až TC-11 | PASS | Seed je idempotentní, navigace a formuláře obsahují kontrolované přístupnostní prvky. |
| Nízká | TC-12 | PASS s omezením | JavaScript pro Web Speech API je načtený; skutečný hlas musí být ověřen ručně v cílovém prohlížeči. |

## Doložené výsledky

| Oblast | Ověření | Výsledek |
|---|---|---|
| Přístupová práva článků | anonymní uživatel je přesměrován; student dostane `403`; správce může spravovat vlastní článek, ale ne cizí | PASS |
| Navigace | student nevidí odkaz na formulář; správce jej vidí | PASS |
| Bonusová zóna a testovací materiály | přihlášený student má stále stav `200` | PASS |
| Regrese | 29 automatizovaných testů, `manage.py check` a `git diff --check` | PASS |

## Vady během exekuce

| ID | Závažnost | Stav | Popis |
|---|---:|---|---|
| DEF-01 | 2/5 | Opraveno | Původní test byl po přidání nové třídy omylem zařazen do nesprávného test case. Struktura testů byla opravena a regrese prošla. |
| DEF-02 | 1/5 | Opraveno | Pomocný integrační skript nesprávně vybral řádek lokálního souboru demo hesel. Výběr byl nahrazen vyhledáním podle uživatelského jména. |

## Reziduální rizika

| Riziko | Skóre | Stav |
|---|---:|---|
| Veřejná registrace bez potvrzení e-mailu a omezení pokusů | 4/5 | Otevřené před veřejným provozem |
| Nesoulad deklarované a ověřené verze Djanga | 3/5 | Otevřené |
| Produkční proměnné a konfigurace PythonAnywhere | 3/5 | Otevřené |
| Formální audit WCAG a test s asistivními technologiemi | 3/5 | Otevřené |
| Dostupnost českého hlasu Web Speech API | 2/5 | Ručně ověřit na cílových zařízeních |

## Doporučení

Výsledek je vhodný pro lokální demonstraci a školní výuku. Před zveřejněním aplikace pro neomezený okruh uživatelů je nutné odstranit riziko veřejné registrace, sjednotit verzi Djanga v závislostech, dokončit produkční konfiguraci a provést ruční přístupnostní testování.
