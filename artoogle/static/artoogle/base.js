'use strict';

var searchBox;
var button;
$(document).ready(function () {
    searchBox = $("#searchbox");
    button = $("#searchButton");
    //searchBox.autocomplete({source: [ "c++", "java"]});
    searchBox.autocomplete({
        source: onSearch,
        autoFocus: true,
        delay: 5,
        select: onSelect
    });
});

function onSearch(request, response) {
    console.log("suche nach:" + request.term);
    $.getJSON("/autosuggest", {"arg":encodeURI(request.term)}, function (data) {
        console.log(data["suggestions"]);
        var suggestions = [];
        data["suggestions"].forEach(function(entry) {
            suggestions.push(decodeURI(entry));
        });
        console.log(suggestions);
        response(suggestions);

    });
}

function onSelect(event, ui) {
    console.log("clicked");
    console.log(ui.item.value);
    searchBox.value = ui.item.value;
}
