# Test execution report: DjangoStart

**Datum exekuce:** 16. září 2026  
**Build / větev:** `copilot/basic-task-for-high-school-students`  
**Úroveň:** component, integrace a omezená systémová validace  
**Reference:** `TEST-PLAN.md`

## Souhrn

| Metrika | Výsledek |
|---|---:|
| Spuštěné automatické testy | 25 |
| Prošlé testy | 25 |
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
| Vysoká | TC-01 až TC-04, TC-07, TC-08, TC-13, TC-14 | PASS | Chráněné cesty, vlastnictví článku, demo administrátor a vytvoření článku fungují podle očekávání. |
| Střední | TC-09 až TC-11 | PASS | Seed je idempotentní, navigace a formuláře obsahují kontrolované přístupnostní prvky. |
| Nízká | TC-12 | PASS s omezením | JavaScript pro Web Speech API je načtený; skutečný hlas musí být ověřen ručně v cílovém prohlížeči. |

## Doložené výsledky

| Oblast | Ověření | Výsledek |
|---|---|---|
| Registrace | platná i neplatná třída vstupů | PASS |
| Přístupová práva | nepřihlášený, přihlášený a jiný autor | PASS |
| Bonusová zóna | `/bonus/` a `/bonus/testovani/` | PASS |
| ISTQB laboratoř a reporty | scénáře i reporty jsou dostupné jen přihlášenému uživateli | PASS |
| Články | publikovaný příspěvek, koncept, kategorie, vytvoření a úprava | PASS |
| Výuková data | seed, opakovaný seed a volitelná obnova | PASS |
| Demo účty | 3 studenti, 1 administrátor, blokace mimo `DEBUG=True` | PASS |
| Přístupnost | skip link, popisy formuláře, prohlášení o přístupnosti | PASS |

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
