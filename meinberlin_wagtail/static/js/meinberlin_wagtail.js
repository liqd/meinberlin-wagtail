var adhocracyOrigin = document.body.dataset.adhocracyUrl;

if (typeof adhocracy !== "undefined") {
    adhocracy.init(adhocracyOrigin, function(adhocracy) {
        adhocracy.embed(".adhocracy_marker");
    });
}

(function() {
    "use strict";

    var loggedIn = null;

    var removeClass = function(el, cl) {
        if(el) {
            el.className = el.className.replace(" " + cl, "");
            el.className = el.className.replace(cl, "");
        }
    };

    var addClass = function(el, cl) {
        if(el) el.className = el.className + " " + cl;
    };

    var toggleMenu = function(el) {
        if (el.className.indexOf("m-open") > -1) {
            removeClass(el, "m-open");
        } else {
            addClass(el, "m-open");
        }
    };

    var forEachElement = function(cls, callback) {
        var elements = document.getElementsByClassName(cls);
        for (var i = 0; i < elements.length; i++) {
            callback(elements[i]);
        }
    };

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
        forEachElement("user-indicator-name", function(el) {
            el.textContent = userName;
        });
        forEachElement("user-indicator", function(el) {
            addClass(el, "is-logged-in");
        });

        // this check is a bit shaky, but should be fine
        if (loggedIn === false && location.href.match(/adh/)) {
            location.href = '/';
        }

        loggedIn = true;
    };

    var onLogout = function() {
        forEachElement("user-indicator", function(el) {
            removeClass(el, "is-logged-in");
        });
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

    forEachElement("user-indicator-logout", function(el) {
        el.addEventListener("click", function(event) {
            event.preventDefault();
            localStorage.removeItem("user-session");
            onLogout();
        });
    });

    document.getElementById("menu-button").addEventListener("click", function(event) {
        event.preventDefault();
        toggleMenu(document.getElementById("main-nav"));
    });
})();
