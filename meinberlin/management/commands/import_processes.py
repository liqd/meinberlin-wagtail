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

            adhocracyprocess = AdhocracyProcess(title=title, slug=slug,  short_description=short_description, image=None, image_copyright='Liquid Democracy e.V.', city=city, archived=archived, embed_url=embed_url, description=description, process_type=process_type)
            process_index.add_child(instance=adhocracyprocess)

# print('done!')
