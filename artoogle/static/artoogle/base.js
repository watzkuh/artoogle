'use strict';

let searchBox;
let button;
$(document).ready(function () {
    searchBox = $("#searchbox");
    button = $("#searchButton");
    searchBox.autocomplete({
        source: onSearch,
        delay: 5,
        select: onSelect,
    })
});

function onSearch(request, response) {
    $.getJSON("/autosuggest", {"arg": encodeURI(request.term)}, function (data) {
        let suggestions = [];
        data["suggestions"].forEach(function (entry) {
            suggestions.push(decodeURI(entry));
        });
        response(suggestions);
    });
}

function onSelect(event, ui) {
    searchBox.value = ui.item.value;
    setTimeout(function () {
        searchBox.parents("form").submit();
    }, 10)
}
