var adhocracyOrigin = document.body.dataset.adhocracyUrl;

adhocracy.init(adhocracyOrigin, function(adhocracy) {
    adhocracy.embed(".adhocracy_marker");
});
