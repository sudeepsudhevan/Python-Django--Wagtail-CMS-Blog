from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model

class BlogIndex(Page):
    # A listing page for blog entries(child pages)

    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['blogpages.BlogDetail']

    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['blogpages'] = BlogDetail.objects.live().public()
        return context


from django.core.exceptions import ValidationError

class BlogDetail(Page):
    # A blog entry page

    parent_page_types = ['blogpages.BlogIndex']
    subpage_types = []

    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(
        blank=True,
        features=['h3','code','bold','italic','link','ol','ul','image']
    )

    image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
        FieldPanel('image'),
    ]

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
