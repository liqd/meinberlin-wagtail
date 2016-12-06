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
        title: 'Beispiele',
    }, {
        id: 'processes',
        title: 'Verfahren',
    }, {
        id: 'contact',
        title: 'Kontakt',
    }],
    heroTitle: 'mein.berlin',
    heroBody: 'Herzlich Willkommen bei mein.berlin, der Plattform für Bürgerbeteiligungsprozesse in Berlin!',
    introTitle: 'Mein.berlin ist der Ort, an dem Sie mit Bürgern ins Gespräch kommen.',
    introBody: 'Hier können Sie Meinungen erfragen oder Stellungnahmen zu Ihrem Bebauungsplanverfahren erhalten. Mein Berlin soll in Zukunft alle gesetzlich geregelten und informellen Bürgerbeteiligungsverfahren Berlins beherbergen. Es haben bereits viele Beteiligungen stattgefunden: hier können Sie mehr über Möglichkeiten und Beispiele erfahren.',
    featuresTitle: 'Features',
    features: [{
        icon: 'images/icons/idea.png',
        title: 'Digitale Beteiligung einfach gemacht',
        body: 'Mein.berlin bietet eine Reihe von Beteiligungsverfahren, die man einfach in Ihren Prozess einbinden und mit Ihrer Fragestellung kombinieren kann. Für Ihren Überblick finden Sie hier die verschiedenen Tools von mein.berlin mit Beispielen und Funktionalitäten.',
    }, {
        icon: 'images/icons/budget.png',
        title: 'Komplexe Prozesse unkompliziert anlegen',
        body: 'Sie haben bereits konkrete Vorstellungen oder Ihr Prozess ist sehr complex? Wir beraten Sie gerne persönlich weiter und besprechen die Umsetzung Ihres Prozesses.',
    }, {
        icon: 'images/icons/discussion.png',
        title: 'Mühelos einbetten und informieren',
        body: 'Mein.Berlin-Beteiligungsverfahren sind so konzipiert, dass sie auch einfach auf Ihrer berlin.de-Seite eingebettet werden können. So können Sie die Bürger auf Ihrer Seite und auf mein.berlin informieren und sie direkt zur Teilhabe einladen.',
    }],
    examplesTitle: 'Beispiele',
    examples: [{
        title: 'Ideensammlungsverfahren ISEK Tegel',
        body: 'Der Dialog zum Flughafenumfeld Tegel wurde in verschiedenen Phasen mit dem Ideensammlungs-Tool begleitet. Es wurden erst offen und in einem zweiten Schritt zu konkreten Themen Vorschläge von Bürger*innen gesammelt und ausgewertet.',
        img: '',
        alt: 'foo',
    }, {
        title: 'Pflege- und Bebauungsplan Tempelhof',
        body: 'Mit dem Textarbeitstool wurde kooperativ mit Bürger*innen der Pflege- und Bebauungsplan für das alte Flugfeld Tempelhof erstellt. Der Textentwurf wurde über 200 mal kommentiert und anschließend vom Abgeordnetenhaus angenommen.',
        img: '',
        alt: 'foo',
    }, {
        title: 'Umfragen des Familienportals',
        body: 'Das Familienportal führt regelmäßig Umfragen rund um das Thema Familie “Zuhause in Berlin” durch. Die Umfragen dauern jeweils einen Monat. Die Ergebnisse der Online-Debatten fließen direkt in die Diskussion der Sitzungen des Berliner Beirats für Familienfragen mit ein.',
        img: '',
        alt: 'foo',
    }],
    processesTitle: 'Prozesse',
    processes: [{
        icon: 'images/icons/opinion.png',
        title: 'Bebauungsplanverfahren',
        body: 'Mit dem Stellungnahmetool können Sie ganz einfach (online) eine frühzeitige Öffentlichkeitsbeteiligung oder eine öffentliche Auslegung begleiten. Das Tool eignet sich auch für Verfahren zur Festsetzung von Naturschutz- oder Landschaftsschutzgebieten.',
    }, {
        icon: 'images/icons/prioritize.png',
        title: 'Umfragen',
        body: 'Umfragen zu verschiedenen Themen geben sehr niedrigschwellige Beteiligungsmöglichkeiten. Das Verfahren eignet sich besonders, um ein Meinungsbild zu einer konkreten Frage einzuholen.',
    }, {
        icon: 'images/icons/vote.png',
        title: 'Bürgerhaushalte',
        body: 'Bürgerhaushalte sind eine gut erprobte Lösung, um Bürger*innen an der lokalen Finanzplanung zu beteiligen. Sie werden zumeist als konsultatives Verfahren eingesetzt und eignen sich besonders auf kommunaler Ebene.',
    }, {
        icon: 'images/icons/vote.png',
        title: 'Ideensammlung und Diskussion',
        body: 'Die Ideensammlung ist das vielfältigste mein.Berlin-Verfahren. Man kann es sowohl für das Entwickeln einer Vision als auch zur Diskussion konkreter Ansätze im Bereich Statdentwicklung benutzen.',
    }, {
        icon: 'images/icons/vote.png',
        title: 'Textbearbeitung',
        body: 'Das Tool zur kooperativen Textarbeit eignet sich vor allem für das Ende eines Beteiligungs- oder Planungsprozesses, wenn ein schon erarbeitetes Papier überprüft, ergänzt und überarbeitet werden soll.',
    }],
    contactTitle: 'Another coll example',
    contactBody: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
    contactButton: 'Call to Action',
    outro: [{
        title: 'First of two columns',
        body: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
    }, {
        title: 'First of two columns',
        body: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
    }],
    footerNav: [{
        url: '',
        title: 'Impressum',
    }],
    markdown: function() {
        return function(text, render) {
            return md.render(render(text));
        };
    },
};

var template = fs.readFileSync('index.mustache', 'utf8');

var output = Mustache.render(template, view);

console.log(output);
