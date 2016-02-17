import requests

from django.core.management.base import BaseCommand, CommandError

from meinberlin.models import AdhocracyProcess


def get_processes(api):
    pool = requests.get(api, params={
        'content_type': 'adhocracy_core.resources.process.IProcess',
        'depth': 2,
        'elements': 'content',
    }).json()

    processes = pool['data']['adhocracy_core.sheets.pool.IPool']['elements']

    for process in processes:
        yield {
            'url': process['path'],
            'content_type': process['content_type'],
            'title': process['data']['adhocracy_core.sheets.title.ITitle']['title'],
            'name': process['data']['adhocracy_core.sheets.name.IName']['name'],
            'creation_date': process['data']['adhocracy_core.sheets.metadata.IMetadata']['item_creation_date'],
            'workflow_state': process['data']['adhocracy_core.sheets.workflow.IWorkflowAssignment']['workflow_state'],
        }


class Command(BaseCommand):
    help = 'Pull new processes from adhocracy'

    def handle(self, *args, **options):
        for p in get_processes('https://embed.mein.berlin.de/api/'):
            process = AdhocracyProcess(
                title=p['title'],
                description='',
                short_description='',
                image=None,
                image_copyright='',
                city='',
                archived=False,
                embed_code='',
                depth=4,
                path='/prozesse/%s/' % p['name'])
            process.save()

            self.stdout.write(self.style.SUCCESS('Successfully created process "%s"' % p['name']))
