# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import migrations


def alter_beteiligungsverfahren_page(apps, schema_editor):

    SimplePage = apps.get_model('meinberlin.SimplePage')

    with open('initial_content.json') as fh:
        initial_content = json.load(fh)

    for entry in initial_content:
        if entry['pk'] == 11 and entry['model'] == 'meinberlin.simplepage':
            page = SimplePage.objects.get(pk=11)
            page.body = entry['fields']['body']
            page.save()
            break


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin', '0001_initial'),
        ('meinberlin', '0002_create_content'),
        ('meinberlin', '0007_auto_20160404_1022'),
    ]

    operations = [
        migrations.RunPython(alter_beteiligungsverfahren_page),
    ]
