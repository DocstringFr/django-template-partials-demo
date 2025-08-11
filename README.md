# Django Template Partials + HTMX — Démo

Ce projet démontre comment utiliser les Django Template Partials couplés à HTMX pour des mises à jour ultra-rapides de fragments HTML, sans recharger toute la page. L’interface est stylée avec Tailwind CSS (via CDN) et les interactions dynamiques sont gérées par HTMX (via CDN également).

## Aperçu rapide
- **Template Partials**: mise à jour ciblée de fragments HTML nommés (`{% partialdef %}` … `{% endpartialdef %}`).
- **HTMX**: requêtes légères (`hx-get`, `hx-post`, `hx-trigger`, `hx-swap`, `hx-swap-oob`).
- **Composants de démo**:
  - **Badge de statut** (online/offline), rafraîchi toutes les 2s.
  - **Contenu dynamique** (citation + couleur + horodatage).
  - **Compteur de likes** persistant en base SQLite via le modèle `Like`.
  - **Boutique / Panier** en session, avec mise à jour OOB des quantités produit.

## Deux variantes de la page

### 1) Variante « simple » (sans template partials)
- Fichier: `demo/templates/demo/index-simple.html`.
- Cette variante montre le **découpage en sous-templates** via `{% include %}` (ex.: `demo/partials/online-status.html`, `demo/partials/dynamic-content.html`, `demo/partials/like-counter.html`, `demo/partials/cart-icon.html`).
- Elle n’est pas reliée au backend par défaut (aucune route ne la sert). Elle sert de **référence pédagogique** pour visualiser la structure « sans partials ».
- Pour la tester, vous pouvez temporairement modifier la vue `index` pour rendre `demo/index-simple.html`, ou ajouter une nouvelle route dédiée.

### 2) Variante avec Django Template Partials (reliée au backend)
- Fichier: `demo/templates/demo/index.html`.
- Les fragments sont définis inline avec `{% partialdef ... inline %}` (ex.: `online-status`, `dynamic-content`, `like-counter`, `cart-icon`).
- Côté serveur, les vues renvoient directement un **fragment** en utilisant la syntaxe `render(request, "demo/index.html#nom-du-fragment", context)` — idéal pour les mises à jour ciblées via HTMX.

## Composants de test

- **Badge de statut** (`online-status`)
  - Client: `hx-get` vers la route `online-status`, `hx-trigger="every 2s"`, `hx-swap="outerHTML"`.
  - Serveur: `views.online_status` renvoie le fragment `index.html#online-status` avec `is_online`, `status_text`, `status_color`, `status_icon`.

- **Contenu dynamique** (`dynamic-content`)
  - Client: un bouton `hx-get` vers `update-content`, cible `#dynamic-content`, swap `outerHTML`.
  - Serveur: `views.update_content` choisit une citation/couleur au hasard et renvoie `index.html#dynamic-content` avec `quote`, `color`, `timestamp`.

- **Compteur de likes** (`like-counter`)
  - Client: bouton `hx-post` vers `like-counter`, cible `#like-counter`.
  - Serveur: `views.like_counter` incrémente `Like(id=1)` et renvoie `index.html#like-counter` avec `like_count`.

- **Boutique / Panier** (`cart-icon` + grille produits)
  - Client: boutons d’ajout/retrait appellent `add-to-cart`/`remove-from-cart` et ciblent `#cart-icon`.
  - Serveur: panier stocké en **session**; calcul de `cart_count`; renvoi du fragment `index.html#cart-icon`.
  - Démonstration d’**Out-Of-Band (OOB) swap** via `hx-swap-oob="true"` pour mettre à jour la quantité du produit sans retoucher toute la grille.

## Routage
Défini dans `demo/urls.py`:
- `/` → `views.index` (page avec template partials)
- `/like-counter/` → `views.like_counter` (POST via HTMX)
- `/update-content/` → `views.update_content`
- `/online-status/` → `views.online_status`
- `/cart/add/<int:product_id>/` → `views.add_to_cart`
- `/cart/remove/<int:product_id>/` → `views.remove_from_cart`

## Dépendances
Déclarées dans `pyproject.toml`:
- `django>=5.2.5`
- `django-template-partials>=25.1` (app Django: `template_partials`)

Les bibliothèques côté client sont chargées via CDN:
- HTMX: `https://unpkg.com/htmx.org@1.9.10`
- Tailwind CSS: `https://cdn.tailwindcss.com`

## Démarrage
Prérequis: Python ≥ 3.11, SQLite (inclus), accès réseau pour les CDN.

### Option A — Avec uv (recommandé si vous utilisez `pyproject.toml` et `uv.lock`)
```bash
# Dans le dossier du projet
cd /Users/thibh/template-partials
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```
Ouvrez `http://127.0.0.1:8000/`.

### Option B — Avec venv + pip
```bash
cd /Users/thibh/template-partials
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install "django>=5.2.5" "django-template-partials>=25.1"
python manage.py migrate
python manage.py runserver
```

## Structure du projet (extrait)
```
template-partials/
├── demo/
│   ├── templates/demo/
│   │   ├── index.html                # Variante avec template partials (utilisée)
│   │   ├── index-simple.html         # Variante pédagogique sans partials (non routée)
│   │   └── partials/
│   │       ├── online-status.html
│   │       ├── dynamic-content.html
│   │       ├── like-counter.html
│   │       └── cart-icon.html
│   ├── views.py
│   ├── urls.py
│   └── models.py                     # Modèle Like(count)
├── testpartials/
│   └── settings.py                   # App installée: template_partials, demo
├── manage.py
├── pyproject.toml
└── README.md
```

## Notes
- La base de données SQLite (`db.sqlite3`) est utilisée pour le compteur de likes. Les migrations sont fournies.
- Pour tester `index-simple.html`, reliez-la à une vue/URL ou modifiez temporairement le rendu dans `views.index`.
- Les CDN (HTMX, Tailwind) évitent toute configuration node/npm.

## Liens utiles
- Django Template Partials: https://github.com/carltongibson/django-template-partials
- HTMX: https://htmx.org
- Tailwind CSS: https://tailwindcss.com
