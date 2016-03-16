import requests
import json
import sqlite3

url = (
    'https://embed.mein.berlin.de/api?'
    'content_type=adhocracy_core.resources'
    '.process.IProcess&depth=all&elements=content'
)
r = requests.get(url).json()

exported_processes = r.get('data').get('adhocracy_core.sheets.pool.IPool').get('elements')
import_objects = []
db = sqlite3.connect("db.sqlite3")

query = "insert into meinberlin.process values (?,?,?,?)"
adhquery = "insert into meinberlin.adhocracyprocess values (?,?,?)"
# columns = ['title', 'short_description', 'archived', 'city']
# adhcolumns = ['embed_url', 'description', 'process_type']

process_counter = 1
for counter, exported_process in enumerate(exported_processes):
    if exported_process.get('content_type') == 'adhocracy_meinberlin.resources.bplan.IProcess':
        continue
    data = exported_process.get('data')
    process = {
        "model": "meinberlin.process",
        "pk": counter,
        "fields": {
            'title': data.get('adhocracy_core.sheets.title.ITitle').get('title'),
            'short_description': data.get('adhocracy_core.sheets.description.IDescription').get('short_description'),
            'archived': (data.get('adhocracy_core.sheets.workflow.IWorkflowAssignment').get('workflow_state') == 'closed'),
            'city': 'Berlin'
            }
        }
    import_objects.append(process)
    adhprocess = {
        "model": "meinberlin.adhocracyprocess",
        "pk": process_counter,
        "fields": {
            'embed_url': exported_process.get('path'),
            'description': data.get('adhocracy_core.sheets.description.IDescription').get('description'),
            'process_type': exported_process.get('content_type')
        }
    }
    import_objects.append(adhprocess)
    process_counter = process_counter + 1

# print exports
