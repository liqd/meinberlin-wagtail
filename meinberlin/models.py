from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel
from wagtail.wagtailadmin.edit_handlers import ObjectList
from wagtail.wagtailadmin.edit_handlers import TabbedInterface
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class Process(Page):
    short_description = models.CharField(max_length=255)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    image_copyright = models.CharField(max_length=255, blank=True)
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

    parent_page_types = ['meinberlin.OverviewPage']


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
    embed_url = models.CharField(max_length=255, blank=True)
    description = RichTextField(blank=True)
    process_type = models.CharField(max_length=255, blank=True)

    @property
    def external(self):
        return False

    @property
    def relative_embed_url(self):
        return self.embed_url[self.embed_url.find('api/') + 4:]

    @property
    def embed_widget(self):
        return 'mein.berlin.de'

    @property
    def teaser_text(self):
        if self.process_type == 'adhocracy_meinberlin.resources.burgerhaushalt.IProcess':
            return "Machen Sie Vorschläge, um Politik und Verwaltung dabei zu unterstützen, die knappen Finanzen des Bezirks bedarfsgerecht einzusetzen."
        elif self.process_type == 'adhocracy_meinberlin.resources.kiezkassen.IProcess':
            return "Hier können Sie Ihre Ideen und Vorschläge für die Kiezkasse abgeben."
        elif self.process_type == 'adhocracy_meinberlin.resources.stadtforum.IProcess':
            return "Berlin braucht neuen Wohnraum – schnell, viel und gut. Wie würden Sie gesamtstädtische, gesellschaftliche und individuelle Ansprüche an das Wohnen zusammenbringen? Diskutieren Sie mit!"
        else:
            return ""

    content_panels = Process.content_panels + [
        FieldPanel('description'),
        FieldPanel('embed_url'),
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
    ]

    info_panels = [
        MultiFieldPanel([
            FieldPanel('info1_title'),
            FieldPanel('info1_text'),
        ], heading="Info 1"),
        MultiFieldPanel([
            FieldPanel('info2_title'),
            FieldPanel('info2_text'),
            FieldPanel('netiquette_linktext'),
            FieldPanel('privacy_linktext'),
        ], heading="Info 2"),
        MultiFieldPanel([
            FieldPanel('info3_title'),
            FieldPanel('info3_text'),
            FieldPanel('processes_linktext'),
        ], heading="Info 3"),
    ]

    system_panels = [
        FieldPanel('current_processes_title'),
        FieldPanel('past_processes_title'),
        FieldPanel('view_all'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(info_panels, heading='Info'),
        ObjectList(system_panels, heading='System'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings'),
    ])

    parent_page_types = []


class SimplePage(Page):
    body = RichTextField(blank=True)

    content_panels = [
        FieldPanel('title'),
        FieldPanel('body'),
    ]

    parent_page_types = ['meinberlin.HomePage', 'meinberlin.SimplePage']


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
