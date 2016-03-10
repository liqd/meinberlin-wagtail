# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-17 20:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0010_change_on_delete_behaviour'),
        ('wagtailcore', '0023_alter_page_revision_on_delete_behaviour'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True, primary_key=True, serialize=False,
                    to='wagtailcore.Page')),
                ('header', models.CharField(max_length=255, blank=True)),
                ('description', models.CharField(max_length=255, blank=True)),
                ('info1_title', models.CharField(max_length=255, blank=True)),
                ('info1_text', models.CharField(max_length=255, blank=True)),
                ('info2_title', models.CharField(max_length=255, blank=True)),
                ('info2_text', models.CharField(max_length=255, blank=True)),
                ('info3_title', models.CharField(max_length=255, blank=True)),
                ('info3_text', models.CharField(max_length=255, blank=True)),
                ('netiquette_linktext', models.CharField(max_length=255, blank=True)),
                ('privacy_linktext', models.CharField(max_length=255, blank=True)),
                ('processes_linktext', models.CharField(max_length=255, blank=True)),
                ('current_processes_linktext', models.CharField(max_length=255, blank=True)),
                ('view_all_linktext', models.CharField(max_length=255, blank=True)),
                ('past_processes_linktext', models.CharField(max_length=255, blank=True)),
                ('external_processes_linktext', models.CharField(max_length=255, blank=True)),
                ('further_possibilities_linktext', models.CharField(max_length=255, blank=True)),
                ('further_possibilities_infotext', models.CharField(max_length=255, blank=True)),
                ('click_here', models.CharField(max_length=255, blank=True))
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='OverviewPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('description', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('short_description', models.CharField(max_length=255)),
                ('image_copyright', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('archived', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SimplePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='AdhocracyProcess',
            fields=[
                ('process_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='meinberlin.Process')),
                ('embed_code', models.TextField()),
                ('description', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('meinberlin.process',),
        ),
        migrations.CreateModel(
            name='ArchivePage',
            fields=[
                ('overviewpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='meinberlin.OverviewPage')),
            ],
            options={
                'abstract': False,
            },
            bases=('meinberlin.overviewpage',),
        ),
        migrations.CreateModel(
            name='ExternalProcess',
            fields=[
                ('process_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='meinberlin.Process')),
                ('external_url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
            bases=('meinberlin.process',),
        ),
        migrations.AddField(
            model_name='process',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
