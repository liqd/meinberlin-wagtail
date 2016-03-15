import requests
import json
url = (
    'https://embed.mein.berlin.de/api?'
    'content_type=adhocracy_core.resources'
    '.process.IProcess&depth=all&elements=content'
)
r = requests.get(url).json()

processes = r.get('data').get('adhocracy_core.sheets.pool.IPool').get('elements')
exports = []

with open('exports.json', 'w') as fh:
    for process in processes:
        data = process.get('data')
        if process.get('content_type') == 'adhocracy_meinberlin.resources.bplan.IProcess':
            continue
        exports.append({
            'type': process.get('content_type'),
            'embed_code': (
                '<script src="https://embed.mein.berlin.de/AdhocracySDK.js"></script>'
                '<script> adhocracy.init(\'https://embed.mein.berlin.de\', '
                'function(adhocracy) { adhocracy.embed(\'.adhocracy_marker\'); }); </script>'
                '<div class="adhocracy_marker" data-widget="plain" data-initial-url="/r/' + process.get('path') + '" data-autoresize="false" data-locale="de" data-autourl="true" style="height:500px"></div>'
            ),
            'title': data.get('adhocracy_core.sheets.title.ITitle').get('title'),
            'short_description': data.get('adhocracy_core.sheets.description.IDescription').get('short_description'),
            'archived': (data.get('adhocracy_core.sheets.workflow.IWorkflowAssignment').get('workflow_state') == 'closed')
        })
    json.dump(exports, fh, indent=2)

# print exports
