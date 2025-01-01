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

## Create a Custom Image
### 1. Create App
```
python manage.py startapp images
```
### 2. Edit models.py
`images/models.py`

```py
from django.db import models
from wagtail.images.models import Image,AbstractImage, AbstractRendition
class CustomImage(AbstractImage):
    caption = models.CharField(max_length=255, blank=True)
    admin_form_fields = Image.admin_form_fields + ("caption",)
class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name="renditions")
    class Meta:
        unique_together = [("image", "filter_spec", "focal_point_key")]
```

### 3. Edit base.py
`blog/settings/base.py`
```py
INSTALLED_APPS = [
    "home",
    "search",
    "images", 
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",

.....
.....
.....

WAGTAILIMAGES_IMAGE_MODEL = "images.CustomImage"

WAGTAILIMAGES_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "webp", "svg"]
```
### 4. Edit `home/models.py` for using image in home page
`home/models.py`
```py
from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model


class HomePage(Page):
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    body = RichTextField(blank=True)

    image = models.ForeignKey(
        get_image_model(),
        #was: "wagtailimages.Image" # use get_image_model() to get the image model,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True, # allow the field to be blank in the admin
        null=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("subtitle", read_only=True), # use read_only=True to make the field read-only
        FieldPanel("body"),
        FieldPanel("image"),
    ]
```
### 5. Edit home_page html template
`home/templates/home/home_page.html`
```html
{% extends "base.html" %}
{% load wagtailcore_tags wagtailimages_tags %}

{% block content %}
    <h1>{{ page.title }}</h1>
@@ -9,4 +9,19 @@ <h3>{{ page.subtitle }}</h3>
        {{ page.body|richtext }}
    {% endif %}

    <hr>
    <hr>
    <hr>
    <hr>
    Image Stuff below: <br>
   
    {% image page.image fill-150x150-c100 format-jpeg %}
    {% image page.image width-400 %}
    {% image page.image width-400 format-avif-lossless %}
    {% image page.image width-400 format-webp-lossless %}
    
    {% image page.image fill-90x200 as custom_img %}
    <img src="{{ custom_img.url }}" width="90" height="200">
{% endblock content %}
```
