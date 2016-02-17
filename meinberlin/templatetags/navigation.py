from django import template
from wagtail.wagtailcore.models import Page

register = template.Library()


@register.simple_tag
def get_top_nav():
    return Page.objects.live().in_menu().all()
