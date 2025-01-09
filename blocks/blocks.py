from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class TextBlock(blocks.TextBlock):

    def __init__(self, **kwargs):
        super().__init__(**kwargs,
            max_length=5,
            min_length=2,
            required=False,
            help_text="This is from my TextBlock (help text)")
    
    class Meta:
        icon = 'strikethrough'
        template = 'blocks/text_block.html'
        group = "Standalone blocks"
       

class InfoBlock(blocks.StaticBlock):
    class Meta:
        # icon = '....'
        group = "Standalone blocks"
        template = 'blocks/info_block.html'
        admin_text = "This is from my InfoBlock"
        label = "General Information"

class FAQBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answer = blocks.RichTextBlock(features=["bold", "italic"])


class FAQListBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(FAQBlock(), **kwargs)

    class Meta:
        min_num = 1
        max_num = 5
        label = "Frequently Asked Questions 2"
        # icon = "...."
        template = "blocks/faq_list_block.html"


class CarouselBlock(blocks.StreamBlock):
    image = ImageChooserBlock()
    quotation = blocks.StructBlock(
        [
            ("text", blocks.TextBlock()),
            ("author", blocks.TextBlock()),
        ]
    )

    class Meta:
        template = "blocks/carousel_block.html"
        

class CallToAction1(blocks.StructBlock):
    text = blocks.RichTextBlock(features=["bold", "italic"], required=True)
    page = blocks.PageChooserBlock()
    button_text = blocks.CharBlock(max_length=100, required=False)

    class Meta:
        label = 'CTA #1'
        template = 'blocks/call_to_action_1.html'


class ImageBlock(ImageChooserBlock):
    class Meta:
        template = 'blocks/image_block.html'
        group = "Standalone blocks"