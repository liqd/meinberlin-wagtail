# -*- coding: utf-8 -*-
from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel
from wagtail.wagtailadmin.edit_handlers import ObjectList
from wagtail.wagtailadmin.edit_handlers import TabbedInterface
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


def original_status_string(self):
    # see wagtailcore.models.Page.status_string
    if not self.live:
        if self.expired:
            return "expired"
        elif self.approved_schedule:
            return "scheduled"
        else:
            return "draft"
    else:
        if self.has_unpublished_changes:
            return "live + draft"
        else:
            return "live"


def get_processes(archived):
    return Process.objects\
        .filter(archived=archived)\
        .filter(live=True)\
        .all()


class Process(Page):
    short_description = models.CharField(max_length=255, verbose_name="Kurzbeschreibung")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Bild"
    )
    image_copyright = models.CharField(max_length=255, blank=True, verbose_name="Urheberrecht")
    city = models.CharField(max_length=255, verbose_name="Stadt")
    archived = models.BooleanField(verbose_name="vergangen")

    # HACK: show archived in status string (visible in admin UI)
    def status_string(self):
        s = original_status_string(self)
        try:
            if self.process.archived:
                s += ' (vergangen)'
        except Exception:
            pass
        return s
    Page.status_string = property(status_string)

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
    external_url = models.URLField(unique=True, verbose_name="externe URL")

    @property
    def external(self):
        return True

    content_panels = Process.content_panels + [
        FieldPanel('external_url'),
    ]

    parent_page_types = ['meinberlin.OverviewPage']


class AdhocracyProcess(Process):
    ALEXANDERPLATZ = 'adhocracy_meinberlin.resources.alexanderplatz.IProcess'
    BPLAN = 'adhocracy_meinberlin.resources.bplan.IProcess'
    BUERGERHAUSHALT = 'adhocracy_meinberlin.resources.burgerhaushalt.IProcess'
    DIALOG = 'adhocracy_core.resources.proposal.IProposalVersion'
    KIEZKASSE = 'adhocracy_meinberlin.resources.kiezkassen.IProcess'
    COLLABORATIVE = 'adhocracy_meinberlin.resources.collaborative_text.IProcess'

    PROCESS_CHOICES = (
        (ALEXANDERPLATZ, 'Alexanderplatz'),
        (BPLAN, 'Bebauungsplan'),
        (BUERGERHAUSHALT, 'Bürgerhaushalt'),
        (DIALOG, 'Dialog'),
        (KIEZKASSE, 'Kiezkasse'),
        (COLLABORATIVE, 'Kollaborative Textarbeit'),
    )

    embed_url = models.URLField(unique=True, verbose_name="Embed-URL")
    description = RichTextField(blank=True, verbose_name="Beschreibung")
    process_type = models.CharField(
        max_length=255,
        verbose_name="Verfahrenstyp",
        choices=PROCESS_CHOICES,
        default=KIEZKASSE)

    @property
    def external(self):
        return False

    @property
    def embed_options(self):
        if self.process_type == self.DIALOG:
            return {
                'data-widget': 'meinberlin-stadtforum-proposal-detail',
                'data-path': self.embed_url,
                'data-autoresize': 'true',
                'data-locale': 'de',
                'data-autourl': 'false',
                'data-noheader': 'true',
            }
        else:
            relative_url = self.embed_url[self.embed_url.find('api/') + 4:]

            return {
                'data-widget': 'mein.berlin.de',
                'data-initial-url': '/r/' + relative_url,
                'data-autoresize': 'false',
                'data-locale': 'de',
                'data-autourl': 'true',
                'style': 'height: 800px',
            }

    content_panels = Process.content_panels + [
        FieldPanel('description'),
        FieldPanel('embed_url'),
        FieldPanel('process_type')
    ]

    parent_page_types = ['meinberlin.OverviewPage']


class HomePage(Page):
    header = models.CharField(max_length=255, blank=True, verbose_name="Kopfzeile")
    description = RichTextField(blank=True, verbose_name="Beschreibung")
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Titelbild")
    info1_title = models.CharField(max_length=255, blank=True, verbose_name="Infobox 1 Titel")
    info1_text = models.CharField(max_length=2047, blank=True, verbose_name="Infobox 1 Text")
    info2_title = models.CharField(max_length=255, blank=True, verbose_name="Infobox 2 Titel")
    info2_text = models.CharField(max_length=2047, blank=True, verbose_name="Infobox 2 Text")
    info3_title = models.CharField(max_length=255, blank=True, verbose_name="Infobox 3 Titel")
    info3_text = models.CharField(max_length=2047, blank=True, verbose_name="Infobox 3 Text")
    netiquette_linktext = models.CharField(max_length=255, blank=True)
    privacy_linktext = models.CharField(max_length=255, blank=True, verbose_name="Datenschutz Linktext")
    processes_linktext = models.CharField(max_length=255, blank=True, verbose_name="Verfahrensübersicht Linktext")
    current_processes_title = models.CharField(max_length=255, blank=True, verbose_name="Aktuelle Verfahren Titel")
    view_all = models.CharField(max_length=255, blank=True, verbose_name="alle anzeigen")
    past_processes_title = models.CharField(max_length=255, blank=True, verbose_name="Vergangene Verfahren Titel")

    @property
    def processes(self):
        return get_processes(False)[:8]

    @property
    def archived(self):
        return get_processes(True)[:4]

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
    body = RichTextField(blank=True, verbose_name="Inhalt")

    content_panels = [
        FieldPanel('title'),
        FieldPanel('body'),
    ]

    parent_page_types = ['meinberlin.HomePage', 'meinberlin.SimplePage']


class OverviewPage(Page):
    description = RichTextField(blank=True, verbose_name="Beschreibung")

    @property
    def processes(self):
        return get_processes(False)

    content_panels = [
        FieldPanel('title'),
        FieldPanel('description'),
    ]

    parent_page_types = []


class ArchivePage(OverviewPage):
    @property
    def processes(self):
        return get_processes(True)

    parent_page_types = []


class AdhocracyPage(Page):
    widget = models.CharField(max_length=255)

    content_panels = [
        FieldPanel('title'),
        FieldPanel('widget'),
    ]

    parent_page_types = ['meinberlin.HomePage']
