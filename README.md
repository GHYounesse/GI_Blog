# Django Blog App

A full-featured blog application built with Django and Bootstrap. Supports user authentication, post management, categories, likes, bookmarks, comments, and a trending feed.

---

## Features

### Posts
- Create, read, update, delete posts (authors only)
- Category filtering
- Trending page — posts ranked by like count
- Pagination (5 posts per page)

### Users
- Register, login, logout
- Profile page with avatar upload
- View all posts by a specific author

### Interactions
- Like / unlike posts (toggle)
- Bookmark posts to a Read Later list
- Comment on posts, edit and delete your own comments

### Discovery
- Full-text search across post titles and content
- Browse by category
- Trending feed

### Other
- Contact / message form
- About page

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django |
| Database | PostgreSQL |
| Frontend | Bootstrap 5 |
| Image handling | Pillow |
| Auth | Django built-in auth |

---

## Project Structure

```
├── blog/
│   ├── models.py        # Post, Comment, Categorie, Message
│   ├── views.py         # All blog views (CBVs + function views)
│   ├── forms.py         # PostForm, CategorieForm, CommentForm
│   ├── urls.py
│   └── templates/blog/
│       ├── index.html
│       ├── trending.html
│       ├── cat_list.html
│       ├── search.html
│       ├── read_posts.html
│       └── ...
├── users/
│   ├── models.py        # Profile (extends User)
│   ├── views.py         # register, profile
│   ├── forms.py         # UserRegisterForm, UserUpdateForm, ProfileUpdateForm
│   └── templates/users/
│       ├── register.html
│       └── profile.html
├── manage.py
└── requirements.txt     # See Dependencies section below
```

---

## Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/GHYounesse/GI_Blog.git
```

### 2. Create and activate a virtual environment

```bash
python -m venv env
source env/bin/activate        # Mac/Linux
env\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

In `settings.py`, update the `DATABASES` block:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Configure media files

In `settings.py`:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 6. Apply migrations and create a superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7.Create .env file

```bash
cp .env.example .env
```
And update the values

### 8. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

---

## Key URLs

| URL | Description |
|-----|-------------|
| `/` | Home — all posts with search |
| `/trending/` | Posts sorted by likes |
| `/post/<id>/` | Single post with comments |
| `/post/new/` | Create post (auth required) |
| `/category/<cat>/` | Posts filtered by category |
| `/search/` | Search results |
| `/read/<username>/` | User's read-later list |
| `/register/` | User registration |
| `/profile/` | Edit profile and avatar |
| `/contact/` | Contact form |

---

