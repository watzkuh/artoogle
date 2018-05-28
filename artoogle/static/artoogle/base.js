'use strict';

var searchBox;
var button;
$(document).ready(function () {
    searchBox = $("#searchbox");
    button = $("#searchButton");
    searchBox.autocomplete({
        source: onSearch,
        autoFocus: true,
        delay: 5,
        select: onSelect
    });
});

function onSearch(request, response) {
    $.getJSON("/autosuggest", {"arg":encodeURI(request.term)}, function (data) {
        var suggestions = [];
        data["suggestions"].forEach(function(entry) {
            suggestions.push(decodeURI(entry));
        });
        response(suggestions);

    });
}

function onSelect(event, ui) {
    searchBox.value = ui.item.value;
}
