from wagtail.images.formats import Format,register_image_format

register_image_format(
    Format(
        'thumbnail',
        'richtext-image thumbnail-150',
        'fill-150x150',
        'width-150',
    )
)