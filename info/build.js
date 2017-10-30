var fs = require('fs');

var MarkdownIt = require('markdown-it');
var Mustache = require('mustache');

var md = new MarkdownIt();


var view = {
    title: 'Info',
    jumpNav: [{
        id: 'features',
        title: 'Plattform',
    }, {
        id: 'examples',
        title: 'Referenzprojekte',
    }, {
        id: 'processes',
        title: 'Verfahren',
    }, {
        id: 'contact',
        title: 'Kontakt',
    }],
    heroTitle: 'meinBerlin',
    heroBody: 'DIE Beteiligungsplattform des Landes Berlin. Herzlich Willkommen!',
    introTitle: 'meinBerlin ist der Ort, an dem Sie mit Bürger*innen der Stadt ins Gespräch kommen.',
    introBody: 'Hier können Sie Meinungen erfragen oder Stellungnahmen zu Ihrem Bebauungsplanverfahren erhalten. Mein Berlin soll in Zukunft alle gesetzlich geregelten und informellen Bürgerbeteiligungsverfahren Berlins beherbergen. Es haben bereits viele Beteiligungen stattgefunden: hier können Sie mehr über verschiedene Möglichkeiten erfahren und Referenzprojekte finden.',
    featuresTitle: 'Plattform',
    features: [{
        icon: 'images/icons/click.png',
        title: 'Digitale Beteiligung ganz einfach',
        body: 'meinBerlin bietet eine Reihe von Beteiligungsverfahren, die man einfach in Ihren Prozess einbinden und mit Ihrer Fragestellung kombinieren kann. Die verschiedenen Tools von meinBerlin mit Beispielen und Funktionalitäten finden Sie hier im Überblick.',
    }, {
        icon: 'images/icons/simple.png',
        title: 'Komplexe Prozesse bequem anlegen',
        body: 'Sie haben bereits konkrete Vorstellungen oder komplexe Prozesse umzusetzen? Wir beraten Sie gerne persönlich zur Umsetzung Ihres Prozesses.',
    }, {
        icon: 'images/icons/embedding.png',
        title: 'Direkt einbetten und informieren',
        body: 'meinBerlin-Beteiligungsverfahren sind so konzipiert, dass sie auch einfach auf Ihrer berlin.de-Seite eingebunden werden können. So können Sie die Bürger*innen auf beiden Seiten informieren und direkt zur Teilhabe einladen.',
    }],
    examplesTitle: 'Referenzprojekte',
    examples: [{
        title: 'Ideensammlungsverfahren ISEK Tegel',
        body: 'Der Dialog zum Flughafenumfeld Tegel wurde in verschiedenen Phasen mit dem Ideensammlungs-Tool begleitet. Es wurden erst offen und in einem zweiten Schritt zu konkreten Themen Vorschläge von Bürger*innen gesammelt und ausgewertet.',
        img: 'images/examples/Tegel.png',
        alt: '',
        url: 'http://www.stadtentwicklung.berlin.de/staedtebau/projekte/tegel/stadtumbau/dokumentation.shtml#!/r/isek/tegel/',
    }, {
        title: 'Entwicklungs- und Pflegeplan Tempelhof',
        body: 'Mit dem Textarbeitstool wurde kooperativ mit Bürger*innen der Pflege- und Bebauungsplan für das alte Flugfeld Tempelhof erstellt. Der Textentwurf wurde über 200 mal kommentiert und anschließend vom Abgeordnetenhaus angenommen.',
        img: 'images/examples/Tempelhof.jpg',
        alt: '',
        url: 'https://mein.berlin.de/w/prozesse/epptf/ ',
    }, {
        title: 'Umfragen des Familienportals',
        body: 'Das Familienportal führt regelmäßig Umfragen rund um das Thema Familie “Zuhause in Berlin” durch. Die Umfragen dauern jeweils einen Monat. Die Ergebnisse der Online-Debatten fließen direkt in die Diskussion der Sitzungen des Berliner Beirats für Familienfragen mit ein.',
        img: 'images/examples/Familienportal.png',
        alt: '',
        url: 'https://mein.berlin.de/w/prozesse/treiben-sie-mit-ihrer-familie-sport-welche-angebot/',
    }],
    processesTitle: 'Verfahren',
    processes: [{
        icon: 'images/icons/idea.png',
        title: 'Brainstorming, Ideensammlung und Diskussion',
        body: 'Das Brainstorming und die Ideensammlung sind die vielfältigsten meinBerlin-Verfahren. Man kann es sowohl für das Entwickeln einer Vision als auch zur Diskussion konkreter Ansätze im Bereich Stadtentwicklung benutzen. Sammeln Sie ortspezifische und/oder themenspezifische Ideen, kommentieren und bewerten Sie diese! Ortspezifische Ideen können außerdem auf einer Karte verortet werden.',
    }, {
        icon: 'images/icons/agenda.png',
        title: 'Agenda festlegen',
        body: 'Identifizieren Sie mit diesem Verfahren Themen und definieren Sie das Selbstverständnis und die Grundprinzipien. Im Anschluss können die Themen bewertet und kommentiert werden. Darüber erhalten Sie eine quantitative Rückmeldung mittels der Bewertung der Ideen.',
    }, {
        icon: 'images/icons/comment_on_document.png',
        title: 'Textbearbeitung',
        body: 'Das Tool zur kooperativen Textarbeit eignet sich hervorragend für das Ende eines Beteiligungs- oder Planungsprozesses, um ein bereits erarbeitetes Papier zu überprüfen, ergänzen und zu überarbeiten. Textentwürfe können dabei erstellt und kommentiert werden.',
    }, {
        icon: 'images/icons/budget.png',
        title: 'Bürgerhaushalte',
        body: 'Beteiligen Sie Bürger*innen an der lokalen Finanzplanung mit einem gut erprobten Bürgerhaushaltsverfahren. Sie werden zumeist als konsultatives Verfahren eingesetzt und eignen sich besonders auf kommunaler Ebene. Vorschläge können mit einem Budget versehen und auf einer Karte verortet werden, sowie anschließend bewertet und kommentiert werden.',
    }, {
        icon: 'images/icons/external.png',
        title: 'Externes Projekt',
        body: 'Auch externe Projekte, die auf einer anderen Plattform zu finden sind, können auf mein.Berlin.de mühelos verlinkt werden.',
    }, {
        icon: 'images/icons/vote.png',
        title: 'Umfragen',
        body: 'Ermöglichen Sie sehr niedrigschwellige Beteiligungsmöglichkeiten zu verschiedenen Themen mit dem Umfragetool. Das Verfahren eignet sich besonders, um ein Meinungsbild zu einer konkreten Frage einzuholen.',
    }, {
        icon: 'images/icons/topicprio.png',
        title: 'Themenpriorisierung',
        body: 'Mit diesem Verfahren können relevante Themen und Handlungsfelder eingebracht, identifiziert und priorisiert werden. Durch die Kommentar- und Abstimmungsfunktion kann eine rege Diskussion entstehen und ein kontinuierlicher Dialog gefördert werden.',
    }, {
        icon: 'images/icons/building.png',
        title: 'Bebauungsplanverfahren',
        body: 'Begleiten Sie ganz einfach (online) eine frühzeitige Öffentlichkeitsbeteiligung oder eine öffentliche Auslegung mit einem Formular zur Stellungnahme. Dieses Formular kann auf externen Seiten eingebunden werden und eignet sich auch für Verfahren zur Festsetzung von Naturschutz- oder Landschaftsschutzgebieten.',
    }, {
        icon: 'images/icons/kiezkasse.png',
        title: 'Kiezkasse',
        body: 'Mit diesem Tool können Vorschläge mit einem Budget versehen werden und sie auf einer Karte verortet werden. Diese Vorschläge können bewertet und kommentiert werden und dienen als wertvolle Rückmeldung für alle Beteiligten.',
    }],
    contactTitle: 'Möchten Sie weitere Informationen?',
    contactBody: 'Kontaktieren Sie uns, wir beraten Sie gern welche Verfahren sich für welche Fragen eignen und geben Ihnen einen vertieften Überblick.\n\nDaniel Kämpfe-Fehrle  \nReferent für E-Partizipation in der Landesredaktion/-koordinierung Berlin.de  \nTelefon: 030 90262283  \nE-Mail: <daniel.kaempfe-fehrle@senatskanzlei.berlin.de>\n\nZum Testen der Verfahren können Sie außerdem <https://meinberlin-demo.liqd.net> besuchen.',
    footerNav: [{
        url: 'https://mein.berlin.de/impressum/',
        title: 'Impressum',
    }],
    markdown: function() {
        return function(text, render) {
            var originalEscape = Mustache.escape;
            Mustache.escape = function(x) {return x} ;
            var result = md.render(render(text));
            Mustache.escape = originalEscape;
            return result;
        };
    },
};

var template = fs.readFileSync('index.mustache', 'utf8');

var output = Mustache.render(template, view);

console.log(output);
