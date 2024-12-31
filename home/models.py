from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
from wagtail.documents import get_document_model


class HomePage(Page):

    #template = "home/home_page.html" # look  for app_name/your_class_name.html
    max_count = 1

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
