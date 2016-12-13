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
    introTitle: 'mein.berlin ist der Ort, an dem Sie mit Bürgern ins Gespräch kommen.',
    introBody: 'Hier können Sie Meinungen erfragen oder Stellungnahmen zu Ihrem Bebauungsplanverfahren erhalten. Mein Berlin soll in Zukunft alle gesetzlich geregelten und informellen Bürgerbeteiligungsverfahren Berlins beherbergen. Es haben bereits viele Beteiligungen stattgefunden: hier können Sie mehr über Möglichkeiten und Beispiele erfahren.',
    featuresTitle: 'Plattform',
    features: [{
        icon: 'images/icons/easy.png',
        title: 'Digitale Beteiligung einfach gemacht',
        body: 'mein.berlin bietet eine Reihe von Beteiligungsverfahren, die man einfach in Ihren Prozess einbinden und mit Ihrer Fragestellung kombinieren kann. Für Ihren Überblick finden Sie hier die verschiedenen Tools von mein.berlin mit Beispielen und Funktionalitäten.',
    }, {
        icon: 'images/icons/simple.png',
        title: 'Komplexe Prozesse unkompliziert anlegen',
        body: 'Sie haben bereits konkrete Vorstellungen oder Ihr Prozess ist sehr complex? Wir beraten Sie gerne persönlich weiter und besprechen die Umsetzung Ihres Prozesses.',
    }, {
        icon: 'images/icons/embedding.png',
        title: 'Mühelos einbetten und informieren',
        body: 'Mein.Berlin-Beteiligungsverfahren sind so konzipiert, dass sie auch einfach auf Ihrer berlin.de-Seite eingebettet werden können. So können Sie die Bürger auf Ihrer Seite und auf mein.berlin informieren und sie direkt zur Teilhabe einladen.',
    }],
    examplesTitle: 'Beispiele',
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
        icon: 'images/icons/opinion.png',
        title: 'Bebauungsplanverfahren',
        body: 'Begleiten Sie ganz einfach (online) eine frühzeitige Öffentlichkeitsbeteiligung oder eine öffentliche Auslegung mit dem Stellungnahmetool. Das Tool eignet sich auch für Verfahren zur Festsetzung von Naturschutz- oder Landschaftsschutzgebieten.',
    }, {
        icon: 'images/icons/vote.png',
        title: 'Umfragen',
        body: 'Ermöglichen Sie sehr niedrigschwellige Beteiligungsmöglichkeiten zu verschiedenen Themen mit dem Umfragetool. Das Verfahren eignet sich besonders, um ein Meinungsbild zu einer konkreten Frage einzuholen.',
    }, {
        icon: 'images/icons/budget.png',
        title: 'Bürgerhaushalte',
        body: 'Beteiligen Sie Bürger*innen an der lokalen Finanzplanung mit einem gut erprobten Bürgerhaushaltsverfahren. Sie werden zumeist als konsultatives Verfahren eingesetzt und eignen sich besonders auf kommunaler Ebene.',
    }, {
        icon: 'images/icons/idea.png',
        title: 'Ideensammlung und Diskussion',
        body: 'Die Ideensammlung ist das vielfältigste mein.Berlin-Verfahren. Man kann es sowohl für das Entwickeln einer Vision als auch zur Diskussion konkreter Ansätze im Bereich Statdentwicklung benutzen.',
    }, {
        icon: 'images/icons/discussion.png',
        title: 'Textbearbeitung',
        body: 'Das Tool zur kooperativen Textarbeit eignet sich vor allem für das Ende eines Beteiligungs- oder Planungsprozesses, wenn ein schon erarbeitetes Papier überprüft, ergänzt und überarbeitet werden soll.',
    }],
    contactTitle: 'Sie wollen sich weiter informieren lassen?',
    contactBody: 'Rufen Sie an und lassen sich kompetent beraten. Wir helfen gerne weiter, welche Verfahren sich für welche Fragen eignen oder geben einen vertieften Überblick.\n\nLiquid Democracy e.V.  \nJana Gähler  \nTelefon: 030 62984840  \nEmail: <jana.gaehler@liqd.de>  \n\nZum Testen der Verfahren können Sie außerdem <http://mein.berlin-demo.de> besuchen.',
    footerNav: [{
        url: 'https://liqd.net/de/impressum/',
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
