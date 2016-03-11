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
    header = models.CharField(max_length=255, blank=True)
    description = RichTextField(blank=True)
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+')
    info1_title = models.CharField(max_length=255, blank=True)
    info1_text = models.CharField(max_length=2047, blank=True)
    info2_title = models.CharField(max_length=255, blank=True)
    info2_text = models.CharField(max_length=2047, blank=True)
    info3_title = models.CharField(max_length=255, blank=True)
    info3_text = models.CharField(max_length=2047, blank=True)
    netiquette_linktext = models.CharField(max_length=255, blank=True)
    privacy_linktext = models.CharField(max_length=255, blank=True)
    processes_linktext = models.CharField(max_length=255, blank=True)
    current_processes_title = models.CharField(max_length=255, blank=True)
    view_all = models.CharField(max_length=255, blank=True)
    past_processes_title = models.CharField(max_length=255, blank=True)

    @property
    def processes(self):
        return Process.objects.filter(archived=False).all()[:8]

    @property
    def archived(self):
        return Process.objects.filter(archived=True).all()[:4]

    content_panels = [
        FieldPanel('title'),
        FieldPanel('header'),
        FieldPanel('description'),
        ImageChooserPanel('cover_image'),
        FieldPanel('info1_title'),
        FieldPanel('info1_text'),
        FieldPanel('info2_title'),
        FieldPanel('info2_text'),
        FieldPanel('info3_title'),
        FieldPanel('info3_text'),
        FieldPanel('netiquette_linktext'),
        FieldPanel('privacy_linktext'),
        FieldPanel('processes_linktext'),
        FieldPanel('current_processes_title'),
        FieldPanel('view_all'),
        FieldPanel('past_processes_title'),
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
