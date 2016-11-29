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
        id: 'examples',
        title: 'Beispiele',
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
        icon: 'images/icons/idea.png',
        title: 'Title',
        body: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
    }, {
        icon: 'images/icons/budget.png',
        title: 'Title',
        body: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
    }, {
        icon: 'images/icons/discussion.png',
        title: 'Title',
        body: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
    }],
    examplesTitle: 'Beispiele',
    examples: [{
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
    processesTitle: 'Prozesse',
    processes: [{
        icon: 'images/icons/opinion.png',
        title: 'Title',
        body: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
    }, {
        icon: 'images/icons/prioritize.png',
        title: 'Title',
        body: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
    }, {
        icon: 'images/icons/vote.png',
        title: 'Title',
        body: 'MeinBerlin makes online pariticipation powerful and easy for you. And for everyone else.',
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
