from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model

from django.core.exceptions import ValidationError
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.fields import StreamField
from wagtail.blocks import (
    TextBlock,
    StructBlock,
    StreamBlock,
    PageChooserBlock,
    RichTextBlock,
    CharBlock,
    StaticBlock,
    ListBlock,
)
from wagtail.images.blocks import ImageChooserBlock

from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "blogpages.BlogDetail", related_name="tagged_items", on_delete=models.CASCADE
    )


class BlogIndex(Page):
    # A listing page for blog entries(child pages)

    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = ["blogpages.BlogDetail"]

    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["blogpages"] = BlogDetail.objects.live().public()
        return context

from blocks import blocks as custom_blocks

class BlogDetail(Page):
    # A blog entry page

    parent_page_types = ["blogpages.BlogIndex"]
    subpage_types = []

    subtitle = models.CharField(max_length=100, blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    body = StreamField(
        [
            ('info',custom_blocks.InfoBlock()),
            ("faq", custom_blocks.FAQListBlock()),
            ("image", custom_blocks.ImageBlock()),
            ("Doc", DocumentChooserBlock()),
            ("page", PageChooserBlock(required=False, page_type="home.HomePage")),
            ("author", SnippetChooserBlock("blogpages.Author")),
            ('text', custom_blocks.TextBlock()),
            ('carousel', custom_blocks.CarouselBlock()),
            ("call_to_action_1",custom_blocks.CallToAction1()),
        ],
        block_counts={
            # 'text': {'min_num': 1},
            "image": {"max_num": 1},
        },
        use_json_field=True,
        blank=True,
        null=True,
    )

    image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        # FieldPanel('subtitle'),
        # FieldPanel('tags'),
        # FieldPanel('image'),
        FieldPanel("body"),
    ]

    def clean(self):
        super().clean()

        errors = {}

        if "blog" in self.title.lower():
            errors["title"] = 'Title should not contain the word "blog"'

        if "blog" in self.subtitle.lower():
            errors["subtitle"] = 'Subtitle should not contain the word "blog"'

        if "blog" in self.slug.lower():
            errors["slug"] = 'Slug should not contain the word "blog"'

        if errors:
            raise ValidationError(errors)

        return None
