## Getting Started with Wagtail
### 1. Create Virtual Environment
```
python -m venv .venv
```
```
.venv\Scripts\activate
```
### 2. Install wagtail
```
pip install wagtail
```
### 3. Generate your site
```
wagtail start mysite mysite
```
Here is the generated project structure:
```
mysite/
├── .dockerignore
├── Dockerfile
├── home/
├── manage.py*
├── mysite/
├── requirements.txt
└── search/
```
### 4. Install project dependencies
```
cd mysite
```
```
pip install -r requirements.txt
```

### 5. Create the database
```
python manage.py migrate
```
### 6. Create an admin user
```
python manage.py createsuperuser
```
### 7. Start the server
```
python manage.py runserver
```
