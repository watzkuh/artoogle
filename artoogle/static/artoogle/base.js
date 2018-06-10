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
    });
    console.log($.cookie("lang"));
    $("#language_selector").val($.cookie("lang"));
});


function onLanguageSekection(a) {
    console.log(a.value);
    $.cookie("lang", a.value);
    window.location.reload();
}

function onSearch(request, response) {
    $.getJSON("/autosuggest", {"arg": (encodeURIComponent(request.term))}, function (data) {
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
