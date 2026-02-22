# Real Estate Scraper Backend - Heroku Deployment

Backend FastAPI pour Real Estate Scraper, déployé sur Heroku.

## Structure

```
app/
├── main.py           # Application FastAPI principale
├── database.py       # Configuration de la base de données
├── models.py         # Modèles SQLAlchemy
├── schemas.py        # Schémas Pydantic
└── routes/           # Routes de l'API
requirements.txt      # Dépendances Python
Procfile             # Configuration Heroku
```

## Déploiement sur Heroku

### 1. Prérequis

- Compte Heroku
- Heroku CLI installé
- Git

### 2. Créer l'app Heroku

```bash
heroku create ton-nom-d-app
```

### 3. Ajouter une base de données PostgreSQL

```bash
heroku addons:create heroku-postgresql:hobby-dev --app ton-nom-d-app
```

### 4. Pousser le code

```bash
git push heroku main
```

### 5. Vérifier les logs

```bash
heroku logs --tail --app ton-nom-d-app
```

## Variables d'environnement

Heroku configure automatiquement `DATABASE_URL` après l'ajout de PostgreSQL.

Pour ajouter d'autres variables :

```bash
heroku config:set VAR_NAME=value --app ton-nom-d-app
```

## Endpoints

- `GET /health` - Vérifier que l'API est en ligne
- `GET /api/info` - Informations sur l'API
- Autres endpoints selon les routes définies dans `app/routes/`

## Développement local

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

L'API sera disponible sur `http://localhost:8000`
