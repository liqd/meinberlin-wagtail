import requests
import json
import dateutil.parser

from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify

from meinberlin.models import *
from wagtail.wagtailimages.models import Image

IMAGES = {
    'adhocracy_meinberlin.resources.collaborative_text.IProcess': (2, ''),
    'adhocracy_meinberlin.resources.kiezkassen.IProcess': (
        3, 'Foto K - Fotolia.com'),
    'adhocracy_meinberlin.resources.burgerhaushalt.IProcess': (4, ''),
    'adhocracy_meinberlin.resources.stadtforum.IProcess': (5, ''),
    'adhocracy_meinberlin.resources.bplan.IProcess': (
        6, 'SenStadtUm'),
}


def check_process_exists(process):
    try:
        wagtailprocess = AdhocracyProcess.objects.get(
            embed_url=process['path'])
        return True
    except AdhocracyProcess.DoesNotExist:
        return False


def get_image(process):
    image_data = IMAGES.get(process['content_type'])
    if image_data is None:
        return None, ''
    else:
        pk, image_copyright = image_data
        image = Image.objects.get(pk=pk)
        # image = None
        return image, image_copyright


def create_process(process, parent_process=None):
    image, image_copyright = get_image(process)
    proposal = 'adhocracy_core.resources.proposal.IProposalVersion'
    assignment = 'adhocracy_core.sheets.workflow.IWorkflowAssignment'
    desc = 'adhocracy_core.sheets.description.IDescription'
    short_description = process['data'][desc]['short_description']
    city = ''
    embed_url = process['path']
    description = process['data'][desc]['description']
    process_type = process['content_type']
    if process['content_type'] == proposal:
        quest = process['data']['adhocracy_core.sheets.title.ITitle']['title']
        slug = slugify(quest)[:50]
        short_description = quest
        title = 'Stadtforum'
        ws = 'workflow_state'
        archived = parent_process['data'][assignment][ws] == 'result'
    else:
        slug = process['data']['adhocracy_core.sheets.name.IName']['name']
        title = process['data']['adhocracy_core.sheets.title.ITitle']['title']
        archived = process['data'][assignment]['workflow_state'] == 'result'
        if archived is False and short_description == "":
            bh = 'adhocracy_meinberlin.resources.burgerhaushalt.IProcess'
            kk = 'adhocracy_meinberlin.resources.kiezkassen.IProcess'
            if process_type == bh:
                short_description = (
                    "Machen Sie Vorschläge, um Politik und "
                    "Verwaltung dabei zu unterstützen, die knappen Finanzen "
                    "des Bezirks bedarfsgerecht einzusetzen."
                    )
            elif process_type == kk:
                short_description = (
                    "Hier können Sie Ihre Ideen und Vorschläge für die "
                    "Kiezkasse abgeben."
                    )
        elif short_description == "":
            short_description = (
                "Ergebnisse dieses Beteiligungsverfahrens "
                "im Überblick"
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
        process_type=process_type)


def create_ext_process(process):
    image, image_copyright = get_image(process)
    desc = 'adhocracy_core.sheets.description.IDescription'
    short_description = process['data'][desc]['short_description']
    city = ''
    domain = (
        'http://www.stadtentwicklung.berlin.de/planen/'
        'b-planverfahren/de/oeffauslegung/')
    external_url = domain + process['path'].split('/')[-2].lower()
    slug = process['data']['adhocracy_core.sheets.name.IName']['name']
    title = process['data']['adhocracy_core.sheets.title.ITitle']['title']
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


class Command(BaseCommand):
    help = (
        'Imports all new processes from adhocracy that are not BPlan processes'
        ' and imports them to the meinberlin CMS'
    )

    def handle(self, *args, **options):
        r = requests.get('https://embed.mein.berlin.de/api', params={
            'content_type': 'adhocracy_core.resources.process.IProcess',
            'depth': 'all',
            'elements': 'content',
        }).json()
        pool = 'adhocracy_core.sheets.pool.IPool'
        exported_processes = r['data'][pool]['elements']

        process_index = OverviewPage.objects.first()

        for exported_process in exported_processes:
            process_type = exported_process['content_type']

            if check_process_exists(exported_process):
                continue

            # if it's a Stadtforum process, import the polls 'as processes'
            stadtf = 'adhocracy_meinberlin.resources.stadtforum.IProcess'
            if process_type == stadtf:
                proposal = 'adhocracy_core.resources.proposal.IProposalVersion'
                q = requests.get(exported_process['path'], params={
                    'content_type': proposal,

class Command(BaseCommand):
    help = u'Imports all processes from adhocracy that are not BPlan processes and imports them to the meinberlin CMS'

    def handle(self, *args, **options):
        url = (
            'https://embed.mein.berlin.de/api?'
            'content_type=adhocracy_core.resources'
            '.process.IProcess&depth=all&elements=content'
        )
        r = requests.get(url).json()
        exported_processes = r.get('data').get('adhocracy_core.sheets.pool.IPool').get('elements')

        live_process_index = OverviewPage.objects.first()
        archive_index = ArchivePage.objects.first()

        wagtailprocesses = Process.objects.all()

        for exported_process in exported_processes:

            # check whether this process already exists in wagtail and hasn't been updated
            process_url = exported_process.get('path')
            process_data = exported_process.get('data')
            process_modification = dateutil.parser.parse(process_data.get('adhocracy_core.sheets.metadata.IMetadata').get('modification_date'))
            no_process_import = False

            matching_wagtailprocesses = AdhocracyProcess.objects.filter(embed_url=process_url)
            matching_wagtailprocess = None
            if matching_wagtailprocesses:
                matching_wagtailprocess = matching_wagtailprocesses.first()

            if matching_wagtailprocess:
                if matching_wagtailprocess.latest_revision_created_at:
                    wagtailprocess_modification =  dateutil.parser.parse(matching_wagtailprocess.latest_revision_created_at)
                    if wagtailprocess_modification > process_modification:
                        no_process_import = True
                    else:
                        matching_wagtailprocess.delete()
                else:
                    no_process_import = True

            if no_process_import:
                continue

            # import process (unless it's a BPlan)
            process_type = exported_process.get('content_type')
            if process_type == 'adhocracy_meinberlin.resources.bplan.IProcess':
                continue

            image=None
            image_copyright=""

            if process_type == 'adhocracy_meinberlin.resources.collaborative_text.IProcess':
                image = Image.objects.get(pk=2)
                image_copyright = ""
            if process_type == 'adhocracy_meinberlin.resources.kiezkassen.IProcess':
                image = Image.objects.get(pk=3)
                image_copyright = "Foto K - Fotolia.com"
            if process_type == 'adhocracy_meinberlin.resources.burgerhaushalt.IProcess':
                image = Image.objects.get(pk=4)
                image_copyright = ""
            if process_type == 'adhocracy_meinberlin.resources.stadtforum.IProcess':
                image = Image.objects.get(pk=5)
                image_copyright = ""

            # if it's a Stadtforum process, import the polls 'as processes'
            if process_type == 'adhocracy_meinberlin.resources.stadtforum.IProcess':
                q = requests.get(process_url, params={
                    'content_type': 'adhocracy_core.resources.proposal.IProposalVersion',
>>>>>>> a8204e7... add import_processes
                    'depth': 2,
                    'tag': 'LAST',
                    'elements': 'content',
                    }).json()
<<<<<<< HEAD
                pool = 'adhocracy_core.sheets.pool.IPool'
                polls = q['data'][pool]['elements']
                for poll in polls:

                    if check_process_exists(poll):
                        continue

                    adhocracy_process = create_process(poll, exported_process)
                    process_index.add_child(instance=adhocracy_process)
                    # print(adhocracy_process)

                continue

            if process_type == 'adhocracy_meinberlin.resources.bplan.IProcess':
                assignment = (
                    'adhocracy_core.sheets.workflow.IWorkflowAssignment')
                ws = 'workflow_state'
                if exported_process['data'][assignment][ws] == 'participate':
                    ext_process = create_ext_process(exported_process)
                    process_index.add_child(instance=ext_process)
            else:
                adh_process = create_process(exported_process)
                process_index.add_child(instance=adh_process)
            # print(adhocracy_process)
=======
                polls = q.get('data').get('adhocracy_core.sheets.pool.IPool').get('elements')
                for poll in polls:

                    # check whether poll already exists in wagtail and hasn't been updated
                    poll_url = poll.get('path')
                    poll_data = poll.get('data')
                    poll_modification = dateutil.parser.parse(poll_data.get('adhocracy_core.sheets.metadata.IMetadata').get('modification_date'))
                    no_poll_import = False

                    matching_wagtailpolls = AdhocracyProcess.objects.filter(embed_url=poll_url)
                    matching_wagtailpoll = None
                    if matching_wagtailpolls:
                        matching_wagtailpoll = matching_wagtailpolls.first()

                    if matching_wagtailpoll:
                        if matching_wagtailpoll.latest_revision_created_at:
                            wagtailpoll_modification =  dateutil.parser.parse(matching_wagtailpoll.latest_revision_created_at)
                            if wagtailpoll_modification > poll_modification:
                                no_poll_import = True
                            else:
                                matching_wagtailpoll.delete()
                        else:
                            no_poll_import = True

                    if no_poll_import:
                        continue

                    # import poll
                    poll_data = poll.get('data')
                    city = poll_data.get('adhocracy_core.sheets.title.ITitle').get('title')
                    slug = slugify(city)[:50]
                    short_description =  process_data.get('adhocracy_core.sheets.description.IDescription').get('short_description')
                    title = 'Dialog'
                    archived = (process_data.get('adhocracy_core.sheets.workflow.IWorkflowAssignment').get('workflow_state') == 'closed')
                    poll_embed_url = poll.get('path')
                    description = process_data.get('adhocracy_core.sheets.description.IDescription').get('description')

                    adhocracyprocess = AdhocracyProcess(title=title, slug=slug, short_description=short_description, image=image, image_copyright=image_copyright, city=city, archived=archived, embed_url=poll_embed_url, description=description, process_type=process_type)
                    if archived == False:
                        live_process_index.add_child(instance=adhocracyprocess)
                    else:
                        archive_index.add_child(instance=adhocracyprocess)
                continue
            slug = process_data.get('adhocracy_core.sheets.name.IName').get('name')
            title = process_data.get('adhocracy_core.sheets.title.ITitle').get('title')
            short_description =  process_data.get('adhocracy_core.sheets.description.IDescription').get('short_description')
            city = ''
            archived = (process_data.get('adhocracy_core.sheets.workflow.IWorkflowAssignment').get('workflow_state') == 'closed')
            description = process_data.get('adhocracy_core.sheets.description.IDescription').get('description')

            if process_type == 'adhocracy_meinberlin.resources.bplan.IProcess':
                continue

            image=None
            image_copyright=""

            if process_type == 'adhocracy_meinberlin.resources.collaborative_text.IProcess':
                image = Image.objects.get(pk=2)
                image_copyright = ""
            if process_type == 'adhocracy_meinberlin.resources.alexanderplatz.IProcess':
                image = Image.objects.get(pk=2)
                image_copyright = ""
            if process_type == 'adhocracy_meinberlin.resources.kiezkassen.IProcess':
                image = Image.objects.get(pk=3)
                image_copyright = "Foto K - Fotolia.com"
            if process_type == 'adhocracy_meinberlin.resources.burgerhaushalt.IProcess':
                image = Image.objects.get(pk=4)
                image_copyright = ""
            if process_type == 'adhocracy_meinberlin.resources.stadtforum.IProcess':
                image = Image.objects.get(pk=5)
                image_copyright = ""

            # if it's a Stadtforum process, import the polls 'as processes'
            if process_type == 'adhocracy_meinberlin.resources.stadtforum.IProcess':
                q = requests.get(process_url, params={
                    'content_type': 'adhocracy_core.resources.proposal.IProposalVersion',
                    'depth': 2,
                    'tag': 'LAST',
                    'elements': 'content',
                    }).json()
                polls = q.get('data').get('adhocracy_core.sheets.pool.IPool').get('elements')
                for poll in polls:

                    # check whether poll already exists in wagtail and hasn't been updated
                    poll_url = poll.get('path')
                    poll_data = poll.get('data')
                    poll_modification = dateutil.parser.parse(poll_data.get('adhocracy_core.sheets.metadata.IMetadata').get('modification_date'))
                    no_poll_import = False

                    matching_wagtailpolls = AdhocracyProcess.objects.filter(embed_url=poll_url)
                    matching_wagtailpoll = None
                    if matching_wagtailpolls:
                        matching_wagtailpoll = matching_wagtailpolls.first()

                    if matching_wagtailpoll:
                        if matching_wagtailpoll.latest_revision_created_at:
                            wagtailpoll_modification =  dateutil.parser.parse(matching_wagtailpoll.latest_revision_created_at)
                            if wagtailpoll_modification > poll_modification:
                                no_poll_import = True
                            else:
                                matching_wagtailpoll.delete()
                        else:
                            no_poll_import = True

                    if no_poll_import:
                        continue

                    # import poll
                    poll_data = poll.get('data')
                    city = poll_data.get('adhocracy_core.sheets.title.ITitle').get('title')
                    slug = slugify(city)[:50]
                    short_description =  process_data.get('adhocracy_core.sheets.description.IDescription').get('short_description')
                    title = 'Dialog'
                    archived = (process_data.get('adhocracy_core.sheets.workflow.IWorkflowAssignment').get('workflow_state') == 'closed')
                    poll_embed_url = poll.get('path')
                    description = process_data.get('adhocracy_core.sheets.description.IDescription').get('description')

                    adhocracyprocess = AdhocracyProcess(title=title, slug=slug, short_description=short_description, image=image, image_copyright=image_copyright, city=city, archived=archived, embed_url=poll_embed_url, description=description, process_type=process_type)
                    if archived == False:
                        live_process_index.add_child(instance=adhocracyprocess)
                    else:
                        archive_index.add_child(instance=adhocracyprocess)
                continue
            slug = process_data.get('adhocracy_core.sheets.name.IName').get('name')
            title = process_data.get('adhocracy_core.sheets.title.ITitle').get('title')
            short_description =  process_data.get('adhocracy_core.sheets.description.IDescription').get('short_description')
            city = ''
            archived = (process_data.get('adhocracy_core.sheets.workflow.IWorkflowAssignment').get('workflow_state') == 'closed')
            description = process_data.get('adhocracy_core.sheets.description.IDescription').get('description')

            adhocracyprocess = AdhocracyProcess(title=title, slug=slug,  short_description=short_description, image=None, image_copyright='Liquid Democracy e.V.', city=city, archived=archived, embed_url=embed_url, description=description, process_type=process_type)
            process_index.add_child(instance=adhocracyprocess)

            if archived == False:
                live_process_index.add_child(instance=adhocracyprocess)
            else:
                archive_index.add_child(instance=adhocracyprocess)
>>>>>>> a8204e7... add import_processes
