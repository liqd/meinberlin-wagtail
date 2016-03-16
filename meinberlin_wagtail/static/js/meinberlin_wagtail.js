var adhocracyOrigin = document.body.dataset.adhocracyUrl;

adhocracy.init(adhocracyOrigin, function(adhocracy) {
    adhocracy.embed(".adhocracy_marker");
});

(function() {
    "use strict";

    var loggedIn = null;

    var http = function(url, cb) {
        var req = new XMLHttpRequest();

        req.onreadystatechange = function(e) {
            if (req.readyState === 4 && req.status < 400) {
                cb(e.target.response);
            }
        };

        req.open('GET', url, true);
        req.send(null);
    };

    var onLogin = function(userName) {
        document.getElementById("user-name").textContent = userName;
        document.getElementById("user-indicator").className = "is-logged-in";

        // this check is a bit shaky, but should be fine
        if (loggedIn === false && location.href.match(/adh/)) {
            location.href = '/';
        }

        loggedIn = true;
    };

    var onLogout = function() {
        document.getElementById("user-indicator").className = "";
        loggedIn = false;
    };

    var getUserName = function(url, cb) {
        var key = 'userName:' + url;
        var userName = localStorage.getItem(key);
        if (userName) {
            cb(userName);
        } else {
            http(url, function(response) {
                var data = JSON.parse(response);
                var userName = data.data["adhocracy_core.sheets.principal.IUserBasic"].name;
                localStorage.setItem(key, userName);
                cb(userName);
            });
        }
    };

    var getLoginState = function() {
        var sessionValue = localStorage.getItem("user-session");
        if (sessionValue) {
            var session = JSON.parse(sessionValue);
            var url = session["user-path"];
            getUserName(url, onLogin);
        } else {
            onLogout();
        }
    };

    window.addEventListener("storage", getLoginState);
    getLoginState();

    document.getElementById("logout").addEventListener("click", function(event) {
        event.preventDefault();
        localStorage.removeItem("user-session");
        onLogout();
    });
})();
