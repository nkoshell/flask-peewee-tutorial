(function ($) {
    var apiUrl = window.apiUrl || 'http://localhost:5000/'; // Get from global ctx or set to 'http://localhost:5000/'

    // call on page loading
    loadBooks();

    var $searchForm = $('#searchBookByTitle');

    $searchForm.submit(function (evt) {
        evt.preventDefault();
        var data = $searchForm.serializeArray();
        var params = {};

        data.forEach(function (element, index) {
            params[element.name] = element.value;
        })

        loadBooks(params);
    });


    function loadBooks(params) {
        params = params || {};
        $.getJSON(apiUrl + 'books', params).done(function (data) {
            console.log('called');
            $("#template-container").loadTemplate("/templates/book.tpl.html", data);
        });
    }

})(window.jQuery);
