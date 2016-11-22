import requests

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.template.defaultfilters import slugify

from wagtail.wagtailimages.models import Image

from meinberlin.models import AdhocracyProcess
from meinberlin.models import ExternalProcess
from meinberlin.models import OverviewPage

RIBPLAN = 'adhocracy_meinberlin.resources.bplan.IProcess'
RIBURGERHAUSHALT = 'adhocracy_meinberlin.resources.burgerhaushalt.IProcess'
RICOLLABORATIVE = 'adhocracy_meinberlin.resources.collaborative_text.IProcess'
RIIDEACOLLECTION = 'adhocracy_meinberlin.resources.idea_collection.IProcess'
RIKIEZKASSE = 'adhocracy_meinberlin.resources.kiezkassen.IProcess'
RIPOLL = 'adhocracy_meinberlin.resources.stadtforum.IPoll'
RISTADTFORUM = 'adhocracy_meinberlin.resources.stadtforum.IProcess'
SIDESCRIPTION = 'adhocracy_core.sheets.description.IDescription'
SINAME = 'adhocracy_core.sheets.name.IName'
SIPOOL = 'adhocracy_core.sheets.pool.IPool'
SITAGS = 'adhocracy_core.sheets.tags.ITags'
SITITLE = 'adhocracy_core.sheets.title.ITitle'
SIWORKFLOW = 'adhocracy_core.sheets.workflow.IWorkflowAssignment'

IMAGES = {
    RIBPLAN: (6, 'SenStadtUm'),
    RIBURGERHAUSHALT: (4, ''),
    RICOLLABORATIVE: (2, ''),
    RIIDEACOLLECTION: (4, ''),
    RIKIEZKASSE: (3, 'Foto K - Fotolia.com'),
    RIPOLL: (5, '')
}


def get_image(process):
    image_data = IMAGES.get(process['content_type'])
    if image_data is None:
        return None, ''
    else:
        pk, image_copyright = image_data
        image = Image.objects.get(pk=pk)
        return image, image_copyright


def create_process(process, parent_process=None):
    image, image_copyright = get_image(process)

    if process['content_type'] == RIPOLL:
        q = AdhocracyProcess.objects
        if q.filter(embed_url__startswith=process['path']).exists():
            raise IntegrityError

        item = process
        process = requests.get(item['data'][SITAGS]['LAST']).json()

        question = process['data'][SITITLE]['title']
        slug = slugify(question)[:50]
        title = 'Stadtforum'
        short_description = question

        process_state = parent_process['data'][SIWORKFLOW]['workflow_state']
        item_state = item['data'][SIWORKFLOW]['workflow_state']
        archived = process_state == 'result' or item_state == 'result'
    else:
        slug = process['data'][SINAME]['name']
        title = process['data'][SITITLE]['title']
        short_description = process['data'][SIDESCRIPTION]['short_description']
        archived = process['data'][SIWORKFLOW]['workflow_state'] == 'result'

    city = ''
    embed_url = process['path']
    description = process['data'][SIDESCRIPTION]['description']

    if short_description == '':
        if archived:
            short_description = (
                "Ergebnisse dieses Beteiligungsverfahrens "
                "im Überblick"
                )
        else:
            if process['content_type'] == RIBURGERHAUSHALT:
                short_description = (
                    "Machen Sie Vorschläge, um Politik und "
                    "Verwaltung dabei zu unterstützen, die knappen "
                    "Finanzen des Bezirks bedarfsgerecht einzusetzen."
                    )
            elif process['content_type'] == RIKIEZKASSE:
                short_description = (
                    "Hier können Sie Ihre Ideen und Vorschläge für die "
                    "Kiezkasse abgeben."
                    )
            elif process['content_type'] == RIIDEACOLLECTION:
                short_description = (
                    "Sammeln Sie Ideen, die der Politik und der "
                    "Verwaltung bei der Entscheidungsfindung und "
                    "Gesetzgebung zu unterstützen."
                    )

    return AdhocracyProcess(
        title=title,
        slug=slug,
        short_description=short_description,
        image=image,
        image_copyright=image_copyright,
        city=city,
        archived=archived,
        embed_url=embed_url,
        description=description,
        process_type=process['content_type'],
        live=False)


def create_external_process(process):
    image, image_copyright = get_image(process)
    short_description = process['data'][SIDESCRIPTION]['short_description']
    city = ''
    domain = (
        'http://www.stadtentwicklung.berlin.de/planen/'
        'b-planverfahren/de/oeffauslegung/')
    external_url = domain + process['path'].split('/')[-2].lower()
    slug = process['data'][SINAME]['name']
    title = process['data'][SITITLE]['title']
    archived = False
    return ExternalProcess(
        title=title,
        slug=slug,
        short_description=short_description,
        image=image,
        image_copyright=image_copyright,
        city=city,
        archived=archived,
        external_url=external_url,
        is_adhocracy=True,
        live=False)


def iter_stadtforum_polls(process):
    request = requests.get(process['path'], params={
        'content_type': RIPOLL,
        'elements': 'content',
    }).json()

    return request['data'][SIPOOL]['elements']


def add_process(path, process):
    process_index = OverviewPage.objects.first()
    try:
        process_index.add_child(instance=process)
        print('imported %s' % path)
    except IntegrityError:
        print('skipped %s' % path)


class Command(BaseCommand):
    help = (
        'Imports all new processes from adhocracy that are not BPlan processes'
        ' and imports them to the meinberlin CMS'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'adhocracy_url',
            nargs='?',
            default='https://embed.mein.berlin.de/api')

    def handle(self, adhocracy_url, **options):
        r = requests.get(adhocracy_url, params={
            'content_type': 'adhocracy_core.resources.process.IProcess',
            'depth': 'all',
            'elements': 'content',
        }).json()
        processes = r['data'][SIPOOL]['elements']

        for process in processes:
            if process['content_type'] == RISTADTFORUM:
                for poll in iter_stadtforum_polls(process):
                    try:
                        adhocracy_process = create_process(poll, process)
                        add_process(poll['path'], adhocracy_process)
                    except IntegrityError:
                        print('skipped %s' % poll['path'])

            elif process['content_type'] == RIBPLAN:
                workflow_state = process['data'][SIWORKFLOW]['workflow_state']
                if workflow_state in ['announce', 'participate']:
                    external_process = create_external_process(process)
                    add_process(process['path'], external_process)

            else:
                adhocracy_process = create_process(process)
                add_process(process['path'], adhocracy_process)
