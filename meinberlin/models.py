from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import RichTextField


class Process(Page):
    short_description = models.CharField(max_length=255)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    image_copyright = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    archived = models.BooleanField()

    content_panels = [
        FieldPanel('title'),
        FieldPanel('short_description'),
        ImageChooserPanel('image'),
        FieldPanel('image_copyright'),
        FieldPanel('city'),
        FieldPanel('archived'),
    ]

    parent_page_types = []


class ExternalProcess(Process):
    external_url = models.URLField()

    @property
    def external(self):
        return True

    content_panels = Process.content_panels + [
        FieldPanel('external_url'),
    ]

    parent_page_types = ['meinberlin.OverviewPage']


class AdhocracyProcess(Process):
    embed_code = models.TextField()
    description = RichTextField(blank=True)

    @property
    def external(self):
        return False

    content_panels = Process.content_panels + [
        FieldPanel('description'),
        FieldPanel('embed_code'),
    ]

    parent_page_types = ['meinberlin.OverviewPage']


class HomePage(Page):
    description = RichTextField(blank=True)

    @property
    def processes(self):
        return Process.objects.filter(archived=False).all()[:8]

    @property
    def archived(self):
        return Process.objects.filter(archived=True).all()[:4]

    content_panels = [
        FieldPanel('title'),
        FieldPanel('description'),
    ]

    parent_page_types = []


class SimplePage(Page):
    body = RichTextField(blank=True)

    content_panels = [
        FieldPanel('title'),
        FieldPanel('body'),
    ]

    parent_page_types = ['meinberlin.HomePage']


class OverviewPage(Page):
    description = RichTextField(blank=True)

    @property
    def processes(self):
        return Process.objects.filter(archived=False).all()

    content_panels = [
        FieldPanel('title'),
        FieldPanel('description'),
    ]

    parent_page_types = []


class ArchivePage(OverviewPage):
    @property
    def processes(self):
        return Process.objects.filter(archived=True).all()

    parent_page_types = []
