var fs = require('fs');

var MarkdownIt = require('markdown-it');
var Mustache = require('mustache');

var md = new MarkdownIt();


var view = {
    title: 'mein.berlin Information',
    jumpNav: [{
        id: 'features',
        title: 'Features',
    }, {
        id: 'processes',
        title: 'Prozesse',
    }, {
        id: 'contact',
        title: 'Kontakt',
    }],
    heroTitle: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
    heroBody: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
    introTitle: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
    introBody: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
    featuresTitle: 'Features',
    features: [{
        icon: 'Icon',
        title: 'Title',
        body: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
    }, {
        icon: 'Icon',
        title: 'Title',
        body: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
    }, {
        icon: 'Icon',
        title: 'Title',
        body: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
    }],
    processesTitle: 'Prozesse',
    processes: [{
        title: 'Cool example',
        body: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
        img: '',
        alt: 'foo',
    }, {
        title: 'Title',
        body: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
        img: '',
        alt: 'foo',
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
