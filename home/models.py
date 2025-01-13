from django.db import models
from django.core.exceptions import ValidationError

from wagtail.models import Page, Orderable
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
    FieldRowPanel,
    HelpPanel,
    MultipleChooserPanel,
    TitleFieldPanel,
)
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
from wagtail.documents import get_document_model

from modelcluster.fields import ParentalKey

class HomePageGalleryImage(Orderable):
    page = ParentalKey("home.HomePage", related_name="gallery_images", on_delete=models.CASCADE)
    image = models.ForeignKey(
        get_image_model(),
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="+",
    )
    caption = models.CharField(blank=True, max_length=255)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]

class HomePage(Page):

    # template = "home/home_page.html" # look  for app_name/your_class_name.html
    max_count = 1

    subtitle = models.CharField(max_length=100, blank=True, null=True)
    body = RichTextField(blank=True)

    image = models.ForeignKey(
        get_image_model(),
        # was: "wagtailimages.Image" # use get_image_model() to get the image model,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,  # allow the field to be blank in the admin
        null=True,
    )

    custom_documents = models.ForeignKey(
        get_document_model(),
        # "wagtaildocs.Document", can be used as string instead
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )

    # For Internal Links (provided by Wagtail)
    cta_url = models.ForeignKey(
        "wagtailcore.Page",  # use 'blogpages.BlogDetail' to link to a specific page
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )

    # For External Links (provided by Django)
    cta_external_url = models.URLField(blank=True, null=True)

    content_panels = Page.content_panels + [
        # TitleFieldPanel(
        #     "subtitle",
        #     help_text="The subtitle of the home page",
        #     placeholder="Enter your subtitle",
        # ),
        # MultiFieldPanel(
        #     [
        #         HelpPanel(
        #             content="<strong>Help Panel</strong><p>Help text goes here</p>",
        #             heading="Note: ",
        #         ),
        #         FieldRowPanel(
        #             [
        #                 PageChooserPanel(
        #                     "cta_url",
        #                     "blogpages.BlogDetail",
        #                     help_text="Select a page to link to",
        #                     heading="Blog Page Selection",
        #                     classname="col6",
        #                 ),
        #                 FieldPanel(
        #                     "cta_external_url",
        #                     heading="External Link",
        #                     help_text="Enter an external link",
        #                     classname="col6",
        #                 ),
        #             ],
        #             help_text="Select a page or enter an external link",
        #             heading="Call to Action URL",
        #         ),
        #     ],
        #     heading="Multi Field Panel",
        #     # classname="collapsed",
        #     help_text="Random help text",
        # ),

        # InlinePanel(
        #     "gallery_images",
        #     label="Gallery Images",
        #     min_num=2,
        #     max_num=4,
        #     help_text="Add images to the gallery",
        # )

        MultipleChooserPanel(
            "gallery_images",
            label="Gallery Images",
            min_num=2,
            max_num=4,
            help_text="Add images to the gallery",
            chooser_field_name="image",
        )

        # FieldPanel("subtitle", read_only=True), # use read_only=True to make the field read-only
        # FieldPanel("cta_url"),
        # FieldPanel("cta_external_url"),
        # FieldPanel("body"),
        # FieldPanel("image"),
        # FieldPanel("custom_documents"),
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
                    "cta_url": "You can only one CTA link",
                    "cta_external_url": "You can only one CTA link",
                }
            )
