#  AI‑Powered Blog Platform

A modern Django blog platform enhanced with AI content generation, web research, and a production ready Docker setup. Build, curate, and publish posts faster with automated tools while keeping full editorial control.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-green.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1.svg)](https://www.postgresql.org/)
[![License: CC BY‑NC‑SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

---

## ✨ Features

- 🤖 AI content generation with OpenAI GPT‑4 for drafts, outlines, and full posts.
- 🔍 Web research integration via ValueSERP to enrich content with up‑to‑date context.
- 🗂️ 12 pre‑configured categories auto‑created on first migration.
- 🔐 Authentication: registration, login, password reset, and admin management.
- 📊 Editorial dashboard for creating, editing, and organizing posts.
- 🐳 Dockerized stack (Django + Gunicorn + PostgreSQL + WhiteNoise) for quick deploys.
- 🎨 Production static files pipeline (collectstatic + compression).
- ✅ Healthchecks and startup script with automated migrations.

---

## 🚀 Quick Start

### Option A — Docker (recommended)

git clone https://github.com/Davidxap/ai_powered_blog_platform.git
cd ai_powered_blog_platform

cp .env.docker.example .env

Edit .env with your SECRET_KEY, DB_PASSWORD, and API keys
docker-compose up -d

Create admin account (if not auto-created via env vars)
docker-compose exec -it web python manage.py createsuperuser

Open:
Main: http://localhost:8001/
Admin: http://localhost:8001/admin/


### Option B — Local development

git clone https://github.com/Davidxap/ai_powered_blog_platform.git
cd ai_powered_blog_platform

python -m venv venv
source venv/Scripts/activate # Windows

source venv/bin/activate # Linux/Mac
pip install -r requirements.txt

cp .env.example .env

Edit .env (DEBUG=True, DB_HOST=localhost or use SQLite)
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createsuperuser
python manage.py runserver

Open: http://localhost:8000/admin/

---

## ⚙️ Configuration

Two environment templates are included:

- `.env.example` (local): `DEBUG=True`, `DB_HOST=localhost`, port `8000`.
- `.env.docker.example` (docker): `DEBUG=False`, `DB_HOST=db`, port `8001`, optional auto‑superuser.

Key variables:

SECRET_KEY=your-secret
DEBUG=True|False
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CSRF_TRUSTED_ORIGINS=http://localhost:8000|8001
DB_NAME=blog_ai_db
DB_USER=postgres|Docker_postgres
DB_PASSWORD=your_password
DB_HOST=localhost|db
DB_PORT=5432
OPENAI_API_KEY=sk-xxxx
VALUESERP_API_KEY=xxxx



### Key differences
```
| Setting  | Local | Docker |
|---------|-------|--------|
| Port | 8000 | 8001 |
| DEBUG | True | False |
| DB_HOST | localhost | db |
| Database | SQLite/PostgreSQL | PostgreSQL |
```
---

## 📁 Project Structure

```
ai_powered_blog_platform/
├─ blog/                  # Blog models, views, migrations
├─ accounts/              # Auth and user flows
├─ dashboard/             # Editorial dashboard
├─ ai_generator/          # AI generation flows
├─ simple_blog_ai/        # Django project settings
├─ templates/             # HTML templates
├─ staticfiles/           # Collected static assets
├─ docker-compose.yml     # Docker services
├─ entrypoint.sh          # Startup (migrate, collectstatic, etc.)
├─ requirements.txt       # Python dependencies
├─ .env.example           # Local env template
└─ .env.docker.example    # Docker env template

```
---

## 🐳 Docker Commands
```
docker-compose up -d # Start services
docker-compose down # Stop services
docker-compose down -v # Stop and remove volumes
docker-compose logs -f web # Tail web logs
docker-compose exec web bash # Shell into container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec -it web python manage.py createsuperuser
```

---

## 🧪 Development
```
Run tests
python manage.py test

Create/apply migrations
python manage.py makemigrations
python manage.py migrate

Collect static files
python manage.py collectstatic --no-input
```



---

## 🗂️ Categories

The following categories are created automatically:  
Technology, Artificial Intelligence, Programming, Web Development, Data Science, Tutorial, News, Review, Opinion, Business, Productivity, Lifestyle.

---

## 🔑 API Keys

- OpenAI: https://platform.openai.com/api-keys → set `OPENAI_API_KEY`
- ValueSERP: https://www.valueserp.com/ → set `VALUESERP_API_KEY`

---

## 🔐 Security Checklist (production)
```
- Set `DEBUG=False`
- Use a strong `SECRET_KEY`
- Configure `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`
- Enable HTTPS and set `SECURE_*` cookie flags
- Use strong database credentials
- Rotate API keys periodically
```
---

## 📦 Deployment Notes

- Gunicorn serves Django
- WhiteNoise serves static files
- PostgreSQL 15 with healthcheck
- Startup script runs migrations, optional superuser creation, and collectstatic

---

## 📄 License

This project is licensed under the **Creative Commons Attribution‑NonCommercial‑ShareAlike 4.0 International** license (CC BY‑NC‑SA 4.0).  
You may use, modify, and share for non‑commercial purposes with attribution and the same license.  
Commercial use requires explicit permission. See [LICENSE](./LICENSE) for details.

---

## 👤 Author

- David — https://github.com/Davidxap  
- Project — https://github.com/Davidxap/ai_powered_blog_platform