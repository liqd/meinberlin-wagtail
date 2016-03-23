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
RIKIEZKASSE = 'adhocracy_meinberlin.resources.kiezkassen.IProcess'
RIPROPOSAL = 'adhocracy_core.resources.proposal.IProposalVersion'
RISTADTFORUM = 'adhocracy_meinberlin.resources.stadtforum.IProcess'
SIDESCRIPTION = 'adhocracy_core.sheets.description.IDescription'
SINAME = 'adhocracy_core.sheets.name.IName'
SIPOOL = 'adhocracy_core.sheets.pool.IPool'
SITITLE = 'adhocracy_core.sheets.title.ITitle'
SIWORKFLOW = 'adhocracy_core.sheets.workflow.IWorkflowAssignment'

IMAGES = {
    RICOLLABORATIVE: (2, ''),
    RIKIEZKASSE: (3, 'Foto K - Fotolia.com'),
    RIBURGERHAUSHALT: (4, ''),
    RIPROPOSAL: (5, ''),
    RIBPLAN: (6, 'SenStadtUm'),
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
    short_description = process['data'][SIDESCRIPTION]['short_description']
    city = ''
    embed_url = process['path']
    description = process['data'][SIDESCRIPTION]['description']

    if process['content_type'] == RIPROPOSAL:
        question = process['data'][SITITLE]['title']
        slug = slugify(question)[:50]
        short_description = question
        title = 'Stadtforum'
        ws = 'workflow_state'
        # FIXME: also check proposal item workflow state
        archived = parent_process['data'][SIWORKFLOW][ws] == 'result'
    else:
        slug = process['data'][SINAME]['name']
        title = process['data'][SITITLE]['title']
        archived = process['data'][SIWORKFLOW]['workflow_state'] == 'result'

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
        process_type=process['content_type'])


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
        external_url=external_url)


def iter_stadtforum_polls(process):
    request = requests.get(process['path'], params={
        'content_type': RIPROPOSAL,
        'depth': 2,
        'tag': 'LAST',
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
                    adhocracy_process = create_process(poll, process)
                    add_process(process['path'], adhocracy_process)

            elif process['content_type'] == RIBPLAN:
                workflow_sheet = process['data'][SIWORKFLOW]
                if workflow_sheet['workflow_state'] == 'participate':
                    external_process = create_external_process(process)
                    add_process(process['path'], external_process)

            else:
                adhocracy_process = create_process(process)
                add_process(process['path'], adhocracy_process)
