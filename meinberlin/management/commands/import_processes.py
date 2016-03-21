import requests
import json

from django.core.management.base import BaseCommand
# from django.template.defaultfilters import slugify

from meinberlin.models import *

class Command(BaseCommand):
    help = u'Imports all processes from the adhocracy productive server that are not BPlan processes and imports them to the meinberlin CMS'

    def handle(self, *args, **options):
        url = (
            'https://embed-meinberlin-stage.liqd.net/api?'
            'content_type=adhocracy_core.resources'
            '.process.IProcess&depth=all&elements=content'
        )
        r = requests.get(url).json()

        exported_processes = r.get('data').get('adhocracy_core.sheets.pool.IPool').get('elements')
        import_objects = []

        process_index = OverviewPage.objects.first()

        for exported_process in exported_processes:
            if exported_process.get('content_type') == 'adhocracy_meinberlin.resources.bplan.IProcess':
                continue
            data = exported_process.get('data')
            slug = data.get('adhocracy_core.sheets.name.IName').get('name')
            title = data.get('adhocracy_core.sheets.title.ITitle').get('title')
            short_description =  data.get('adhocracy_core.sheets.description.IDescription').get('short_description')
            city = 'Berlin'
            archived = (data.get('adhocracy_core.sheets.workflow.IWorkflowAssignment').get('workflow_state') == 'closed')
            embed_url = exported_process.get('path')
            description = data.get('adhocracy_core.sheets.description.IDescription').get('description')
            process_type = exported_process.get('content_type')

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

# print('done!')
