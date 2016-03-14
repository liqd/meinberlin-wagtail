# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_homepage(apps, schema_editor):
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    Page = apps.get_model('wagtailcore.Page')
    Site = apps.get_model('wagtailcore.Site')
    HomePage = apps.get_model('meinberlin.HomePage')
    SimplePage = apps.get_model('meinberlin.SimplePage')
    OverviewPage = apps.get_model('meinberlin.OverviewPage')
    ArchivePage = apps.get_model('meinberlin.ArchivePage')

    # Delete the default homepage
    Page.objects.get(id=2).delete()

    homepage_content_type, created = ContentType.objects.get_or_create(
        model='homepage', app_label='meinberlin')
    simplepage_content_type, created = ContentType.objects.get_or_create(
        model='simplepage', app_label='meinberlin')
    overviewpage_content_type, created = ContentType.objects.get_or_create(
        model='overviewpage', app_label='meinberlin')
    archivepage_content_type, created = ContentType.objects.get_or_create(
        model='archivepage', app_label='meinberlin')

    homepage = HomePage.objects.create(
        title="meinBerlin",
        slug='home',
        content_type=homepage_content_type,
        path='00010001',
        depth=2,
        numchild=8,
        url_path='/meinberlin/',
        description=(
            'meinBerlin ist die Plattform, auf der zukünftig alle '
            'öffentlichen Beteiligungsverfahren der Verwaltungen des Landes '
            'Berlin erreichbar sein werden. Es gibt Beteiligungsverfahren für '
            'viele Bereiche. Manche sind rechtlich vorgeschrieben und haben '
            'gesetzlich vorgegebene Regeln (z.B. Bebauungsplanverfahren). '
            'Andere Verfahren richten sich nach der jeweiligen Fragestellung. '
            'Es gibt unterschiedliche Wege der Beteiligung – von der Frage '
            'nach Vorschlägen und Meinungen bis hin zu '
            'Entscheidungsfindungen. Machen Sie mit!'
        ),
    )

    # Create a site with the new homepage set as the root
    Site.objects.create(
        hostname='localhost', root_page=homepage, is_default_site=True)

    OverviewPage.objects.create(
        title='Prozesse',
        slug='prozesse',
        content_type=overviewpage_content_type,
        path='000100010001',
        depth=3,
        numchild=0,
        url_path='/meinberlin/prozesse/',
        description='',
    )

    ArchivePage.objects.create(
        title='Archiv',
        slug='archiv',
        content_type=archivepage_content_type,
        path='000100010002',
        depth=3,
        numchild=0,
        url_path='/meinberlin/archiv/',
        description='',
    )

    nutzungsbedingungen = SimplePage.objects.create(
        title='Nutzungsbedingungen',
        slug='nutzungsbedingungen',
        content_type=simplepage_content_type,
        path='000100010003',
        depth=3,
        numchild=0,
        url_path='/meinberlin/nutzungsbedingungen/',
        show_in_menus=True,
        body=(
            '<p>Mit der Anmeldung als Nutzerin bzw. Nutzer bei '
            'meinBerlin akzeptieren Sie die nachfolgenden '
            'Nutzungsbedingungen. Die Plattform meinBerlin wird vom '
            'Liquid Democracy e.V. im Auftrag des Landes Berlin, '
            'vertreten durch die Senatskanzlei Berlin betrieben. Die '
            'Kontaktdaten sind dem Impressum zu '
            'entnehmen.</p>'
            '<h4>Zugangsvoraussetzungen, Registrierung</h4>'
            '<p>Jede natürliche Person kann sich auf '
            'der Plattform registrieren unter Angabe eines selbst '
            'gewählten Benutzernamens (Pseudonyms), der E-Mail-Adresse '
            'und eines selbst gewählten Passworts. Weitere Angaben '
            'können freiwillig hinzugefügt werden.  Nimmt der Anbieter '
            'den Registrierungsantrag an, erhält der registrierte '
            'Nutzer eine entsprechende Bestätigung per '
            'E-Mail.</p><p>Für jede natürliche Person ist nur eine '
            'Registrierung zulässig. Eine stellvertretende '
            'Registrierung für Dritte ist unzulässig. Der Betreiber '
            'behält sich vor, Nutzungsverhältnisse fristlos zu '
            'kündigen, wenn sie auf mehrfacher Registrierung derselben '
            'natürlichen Person oder auf Stellvertretung für einen '
            'Dritten beruhen.</p><p>Die Nutzung der Plattform ist '
            'unentgeltlich.</p>'
            '<h4>Einstellen von Inhalten</h4>'
            '<p>Registrierte Nutzerinnen bzw. Nutzer '
            'können Beiträge – auch solche, die sich auf Beiträge '
            'anderer Nutzerinnen und Nutzer beziehen - über die '
            'entsprechenden Funktionen in die Plattform einstellen. '
            'Beiträge müssen in deutscher Sprache verfasst '
            'sein.</p><p>Die Beiträge müssen sachlich sein; sie dürfen '
            'keinen beleidigenden Charakter haben und keine Inhalte '
            'umfassen, die straf- oder zivilrechtlich verboten sind. '
            'Für die weitere Diskussionskultur gilt die&nbsp;<a '
            'href="/netiquette/">Netiquette</a>, '
            'die hier einsehbar ist.</p>'
            '<h4>Haftung für Inhalte</h4>'
            '<p>Die Abläufe der Plattform sind '
            'automatisiert. Der Betreiber prüft eingestellte Daten und '
            'Inhalte vor Veröffentlichung nicht auf inhaltliche '
            'Angemessenheit, sachliche Richtigkeit oder auf etwaige '
            'Rechtsverstöße. Der Betreiber verpflichtet sich jedoch, '
            'konkreten Hinweisen auf problematische Daten unverzüglich '
            'nachzugehen.</p>'
            '<h4>Rechte an Inhalten</h4>'
            '<p>Nutzerinnen '
            'bzw. Nutzer räumen dem Betreiber mit dem Einstellen eines '
            'Beitrags ein unbeschränktes, unwiderrufliches und '
            'übertragbares Nutzungsrecht an dem jeweiligen Beitrag '
            'ein, welches den Betreiber Vorhaltung des Beitrags auf '
            'den Seiten des Stadtinformationssystems berlin.de '
            'berechtigt sowie zur Veröffentlichung, Vervielfältigung '
            'und Verbreitung in Printmedien.</p><p>Nutzerinnen bzw. '
            'Nutzer stellen den Betreiber von allen Ansprüchen frei, '
            'die Dritte gegenüber dem Betreiber wegen etwaiger '
            'Rechtsverletzungen durch die eingestellten Beiträge '
            'erheben. Der Freistellungsanspruch umfasst auch die in '
            'einem solchen Zusammenhang erforderlich werdenden Kosten '
            'einer angemessenen Prüfung und ggf.  Rechtsverteidigung, '
            'es sei denn, dass die Nutzerinnen bzw. Nutzer die '
            'Beanstandung des Dritten nicht zu vertreten '
            'haben.</p>'
            '<h4>Beendigung des Nutzungsverhältnisses</h4>'
            '<p>Jeder Nutzerin bzw. jeder '
            'Nutzer kann jederzeit sein Nutzungsverhältnis gegenüber '
            'dem Betreiber kündigen.</p><p>Die Beendigung eines '
            'Nutzungsverhältnisses berührt nicht die dem Betreiber bis '
            'dahin eingeräumten Rechte; diese gelten vielmehr fort. '
            'Gesetzlich unabdingbare Rechte der Nutzerinnen und '
            'Nutzer, etwa auf Rückruf seiner Rechte, bleiben '
            'unberührt.</p><p>Die Plattform wird auf unbestimmte Zeit '
            'betrieben; ein Anspruch der Nutzer auf unbegrenzte '
            'Laufzeit besteht nicht.</p>'
        ),
    )

    impressum = SimplePage.objects.create(
        title='Impressum',
        slug='impressum',
        content_type=simplepage_content_type,
        path='000100010004',
        depth=3,
        numchild=0,
        url_path='/meinberlin/impressum/',
        show_in_menus=True,
        body=(
            '<h3>Herausgeber</h3>'
            '<p>Senatskanzlei Berlin</br>'
            'Berliner Rathaus</br>'
            'Jüdenstraße 1</br>'
            '10178 Berlin</p>'
            ''
            '<h3>Vertretungsberechtigt:</h3>'
            '<p>Chef der Senatskanzlei</br>'
            'Björn Böhning</p>'
            ''
            '<h3>Inhaltlich verantwortlich:</h3>'
            '<p>Chefin des Presse- und Informationsamts</br>'
            'Daniela Augenstein</br>'
            'Berliner Rathaus</br>'
            'Jüdenstraße 1</br>'
            '10178 Berlin</p>'
            ''
            '<h3>Redaktion:</h3>'
            '<p>'
            'Senatskanzlei Berlin</br>'
            'Landesredaktion / Koordinierung Berlin.de</br>'
            'Telefon: (030) 9026 – 2435</br>'
            'Telefax: (030) 9026 – 2285</br>'
            'E-Mail: <a href="mailto:landesredaktion@senatskanzlei.berlin.de">'
            'landesredaktion@senatskanzlei.berlin.de</a></p>'
            ''
            '<h3>Hinweis:</h3>'
            '<p>Die einzelnen Beteiligungsverfahren '
            'auf der Plattform meinBerlin werden von den zuständigen '
            'Behörden eigenverantwortlich aufbereitet und '
            'durchgeführt. Die entsprechenden Angaben finden Sie bei '
            'den jeweiligen Beteiligungsverfahren.</p>'
            ''
            '<h3>Betreiber und technischer Betrieb:</h3>'
            '<p>Das Stadtinformationssystem berlin.de wird von der '
            '<a href="http://www.berlin.de/wir-ueber-uns-be/impressum/" '
            'target="_blank">BerlinOnline Stadtportal GmbH & Co.KG</a>  '
            'betrieben. Betreiber der Beteiligungsplattform meinBerlin '
            'ist Liquid Democracy e.V. (<a href="https://liqd.net/about/" '
            'target="_blank">https://liqd.net/about/</a>)</p>'
        ),
    )

    hilfe = SimplePage.objects.create(
        title='Hilfe',
        slug='hilfe',
        content_type=simplepage_content_type,
        path='000100010005',
        depth=3,
        numchild=0,
        url_path='/meinberlin/hilfe/',
        show_in_menus=True,
        body='',
    )

    netiquette = SimplePage.objects.create(
        title='Netiquette',
        slug='netiquette',
        content_type=simplepage_content_type,
        path='000100010006',
        depth=3,
        numchild=0,
        url_path='/meinberlin/netiquette/',
        body='',
    )

    datenschutz = SimplePage.objects.create(
        title='Datenschutz',
        slug='datenschutz',
        content_type=simplepage_content_type,
        path='000100010007',
        depth=3,
        numchild=0,
        url_path='/meinberlin/datenschutz/',
        body='',
    )

    beteiligungsverfahren = SimplePage.objects.create(
        title='Beteiligungsverfahren',
        slug='beteiligungsverfahren',
        content_type=simplepage_content_type,
        path='000100010008',
        depth=3,
        numchild=0,
        url_path='/meinberlin/beteiligungsverfahren/',
        body='',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin', '0001_initial'),
        ('wagtailredirects', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_homepage),
    ]
