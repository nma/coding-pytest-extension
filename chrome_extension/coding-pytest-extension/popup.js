$.get(chrome.extension.getURL('/template.html'), function(data) {
    $(data).appendTo('body');
});