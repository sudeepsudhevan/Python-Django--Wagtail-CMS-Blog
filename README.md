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
## Create a Custom File Handling
### 1. Create App
```
python manage.py startapp documents
```
### 2. Edit models.py
`documents/models.py`
```py
from django.db import models
from wagtail.documents.models import AbstractDocument, Document

class CustomDocument(AbstractDocument):
    description = models.CharField(blank=True, max_length=255)
    admin_form_fields = Document.admin_form_fields + (
        "description",
    )
```
### 3. Edit base.py
`blog/settings/base.py`
```py
INSTALLED_APPS = [
    "home",
    "search",
    "images",
    "documents", # Add documents

    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",

....
....
....



WAGTAILIMAGES_IMAGE_MODEL = "images.CustomImage"

WAGTAILIMAGES_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "webp", "svg"]
WAGTAILDOCS_DOCUMENT_MODEL = "documents.CustomDocument"
```
### 4. Edit `home/models.py` for using documents in home page
`home/models.py`
```py
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
from wagtail.documents import get_document_model


class HomePage(Page):
    ....
    ....
    ....
        null=True,
    )

    custom_documents = models.ForeignKey(
        get_document_model(),
        #"wagtaildocs.Document", can be used as string instead
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("subtitle", read_only=True), # use read_only=True to make the field read-only
        FieldPanel("body"),
        FieldPanel("image"),
        FieldPanel("custom_documents"),
    ]
```
### 5. Edit home_page html template
`home/templates/home/home_page.html`
```html
{% extends "base.html" %}

{% block content %}

    {% if page.custom_documents %}

        <h1>This is the download url</h1>
        {{ page.custom_documents.url }}

        <a href="{{ page.custom_documents.url }}" download>Download</a>
        {{ page.custom_documents.title }}
```
## Create a Custom Page
### 1. Create App
```
python manage.py startapp blogpages
```
### 2. Edit models.py
`blogpages/models.py`
```py
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
class BlogIndex(Page):
    # A listing page for blog entries(child pages)
    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
    ]
class BlogDetail(Page):
    # A blog entry page
    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
    ]
```
### 3. Edit base.py
`blog/settings/base.py`
```py
INSTALLED_APPS = [
    "home",
    "search",
    "images",
    "documents",
    "blogpages",

    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",

....
....
....
```
### 4. Add a Blog Index html page
`blogpages/templates/blogpages/blog_index.html`
```html
{% extends "base.html" %}
{% load wagtailcore_tags %}
{% block content %}
<h1>{{ page.title }}</h1>
<h3>{{ page.subtitle }}</h3>
<h4>Body is below:</h4>
{{ page.body|richtext }}
{% endblock %}
```
## Limiting Blog page Creation
[Commit #9](https://github.com/sudeepsudhevan/Python-Django--Wagtail-CMS-Blog/commit/b404b381b32a8f472fe03030b9709bee6eb2987d)
```
class BlogIndex(Page):
    # A listing page for blog entries(child pages)

    # max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['blogpages.BlogDetail']
```

## Understand wagtail page context
`blogpages/models.py`
[Commit #10](https://github.com/sudeepsudhevan/Python-Django--Wagtail-CMS-Blog/commit/9ee52865e7da7af188ad4ea5e9e7523a8254217b)
```py
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model

class BlogIndex(Page):
    # A listing page for blog entries(child pages)

    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['blogpages.BlogDetail']

@@ -19,6 +20,11 @@ class BlogIndex(Page):
        FieldPanel('body'),
    ]

    def get_context(self, request):        # Context function
        context = super().get_context(request)
        context['blogpages'] = BlogDetail.objects.live().public()
        return context
```
### Add Custom page validation
`blogpages/models.py`
```py
from django.core.exceptions import ValidationError
class BlogDetail(Page):
    # A blog entry page

        .....
        .....
        .....
        FieldPanel('body'),
        FieldPanel('image'),
    ]

    # Use this function
    def clean(self):
        super().clean()
        errors = {}
        if 'blog' in self.title.lower():
            errors['title'] = 'Title should not contain the word "blog"'
        
        if 'blog' in self.subtitle.lower():
            errors['subtitle'] = 'Subtitle should not contain the word "blog"'
        if 'blog' in self.slug.lower():
            errors['slug'] = 'Slug should not contain the word "blog"'
        if errors:
            raise ValidationError(errors)
        
        return None
```
### Internal and External Links in a WagTail page
`home/models.py`
```py
from django.db import models
from django.core.exceptions import ValidationError

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
@@ -33,9 +34,44 @@ class HomePage(Page):
        null=True,
    )

    # For Internal Links (provided by Wagtail)
    cta_url = models.ForeignKey(
        'wagtailcore.Page',     # use 'blogpages.BlogDetail' to link to a specific page
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )
    # For External Links (provided by Django)
    cta_external_url = models.URLField(blank=True, null=True)
    content_panels = Page.content_panels + [
        FieldPanel("subtitle", read_only=True), # use read_only=True to make the field read-only
        FieldPanel("cta_url"),
        FieldPanel("cta_external_url"), 
        FieldPanel("body"),
        FieldPanel("image"),
        FieldPanel("custom_documents"),
    ]


    @property
    def get_cta_url(self):
        if self.cta_url:
            return self.cta_url.url
        elif self.cta_external_url: 
            return self.cta_external_url
        else:
            return None


    def clean(self):
        super().clean()
        if self.cta_url and self.cta_external_url:
            raise ValidationError(
                {
                    "cta_url":"You can only one CTA link",
                    "cta_external_url":"You can only one CTA link",
                }
            )
```
`home/templates/home/home_page.html`
```html
{% block content %}

{% if page.cta_url or page.cta_external_url %}
    {% if page.cta_url %}
        <a href="{{ page.cta_url.url }}">{{ page.cta_url.title }}</a>
    {% else %}
        <a href="{{ page.cta_external_url }}">Some external link</a>
    {% endif %}
{% endif %}
{% if page.get_cta_url %}
    {{ page.get_cta_url }}
{% endif %}
{% comment %}
    {% if page.custom_documents %}

        <h1>This is the download url</h1>
@@ -13,5 +28,6 @@ <h1>This is the download url</h1>

        {{ page.custom_documents.description }}
    {% endif %}
{% endcomment %}

{% endblock content %}
```
