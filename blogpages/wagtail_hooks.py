from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from taggit.models import Tag
from blogpages.models import Author


@register_snippet
class TagSnippetViewSet(SnippetViewSet):
    model = Tag
    icon = 'tag'
    add_to_admin_menu = True
    menu_label = 'Tags'
    menu_order = 200
    list_display = ['name', 'slug']
    search_fields = ('name',)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

@register_snippet
class AuthorSnippet(SnippetViewSet):
    model = Author
    add_to_admin_menu = False

    panels = [
        FieldPanel('name'),
        FieldPanel('bio'),
    ]

from wagtail import hooks
from django.core.cache import cache

@hooks.register('after_publish_page')
def delete_all_cache(request, page):
    cache.clear()
    # print("page is:", page.title, page.id)



from django.contrib.auth.models import Permission

@hooks.register('register_permissions')
def customer_permissions_numero_uno():
    return Permission.objects.filter(
        content_type__app_label='blogpages', 
        codename='can_edit_author_name'
    )