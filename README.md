# DjangoStart

Český výukový blog pro studenty IT, kteří se učí Django a základy webového vývoje.

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
