(function ($) {
   var apiUrl = window.apiUrl || 'http://localhost:5000/'; // Get from global ctx or set to 'http://localhost:5000/'

    $.getJSON(apiUrl + 'books').done(function (data) {
        console.log('called');
        $("#template-container").loadTemplate("/templates/book.tpl.html", data);
    });
})(window.jQuery);
