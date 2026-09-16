# Test execution report: DjangoStart

**Execution date:** 16. září 2026
**Build / branch:** `copilot/basic-task-for-high-school-students`
**Test level:** component, integration and limited system validation
**Reference:** `TEST-PLAN.md`

## Summary

| Metric | Result |
|---|---:|
| Automated tests run | 29 |
| Passed tests | 29 |
| Failed tests | 0 |
| Blocked tests | 0 |
| `python manage.py check` | PASS |
| `git diff --check` | PASS |
| Recommendation for local teaching | APPROVED |
| Recommendation for public production | CONDITIONAL APPROVAL after mitigation of open risks |

## Results by priority

| Priority | Test cases | Status | Notes |
|---|---|---|---|
| Critical | TC-05, TC-06 | PASS | Platná registrace vytvoří účet; rozdílná hesla účet nevytvoří. |
| High | TC-01 až TC-04, TC-07, TC-08, TC-13 až TC-18 | PASS | Chráněné cesty, role student/správce, vlastnictví článků a demo administrátor fungují podle očekávání. |
| Medium | TC-09 až TC-11 | PASS | Seed je idempotentní, navigace a formuláře obsahují kontrolované přístupnostní prvky. |
| Low | TC-12 | PASS with limitation | JavaScript pro Web Speech API je načtený; skutečný hlas musí být ověřen ručně v cílovém prohlížeči. |

## Evidence

| Area | Verification | Result |
|---|---|---|
| Access control | anonymní uživatel je přesměrován; student dostane `403`; správce může spravovat vlastní článek, ale ne cizí | PASS |
| Navigation | student nevidí odkaz na formulář; správce jej vidí | PASS |
| Bonus zone and test materials | přihlášený student má stále status `200` | PASS |
| Regression | 29 automatizovaných testů, `manage.py check` a `git diff --check` | PASS |

## Defects

| ID | Severity | Status | Description |
|---|---:|---|---|
| DEF-01 | 2/5 | FIXED | Původní test byl po přidání nové třídy omylem zařazen do nesprávného test case. Struktura testů byla opravena a regrese prošla. |
| DEF-02 | 1/5 | FIXED | Pomocný integration script nesprávně vybral řádek lokálního souboru demo hesel. Výběr byl nahrazen vyhledáním podle uživatelského jména. |

## Residual risks

| Risk | Score | Status |
|---|---:|---|
| Veřejná registrace bez potvrzení e-mailu a omezení pokusů | 4/5 | OPEN before public production |
| Nesoulad deklarované a ověřené verze Djanga | 3/5 | OPEN |
| Produkční proměnné a konfigurace PythonAnywhere | 3/5 | OPEN |
| Formální audit WCAG a test s asistivními technologiemi | 3/5 | OPEN |
| Dostupnost českého hlasu Web Speech API | 2/5 | MANUAL VERIFICATION required on target devices |

## Recommendation

Recommendation: report je vhodný pro lokální demonstraci a školní výuku. Před zveřejněním aplikace pro neomezený okruh uživatelů je nutné odstranit riziko veřejné registrace, sjednotit verzi Djanga v závislostech, dokončit produkční konfiguraci a provést ruční přístupnostní testování.
