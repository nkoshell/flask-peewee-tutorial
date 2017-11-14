(function ($) {
    var apiUrl = window.apiUrl || 'http://localhost:5000/'; // Get from global ctx or set to 'http://localhost:5000/'
    apiUrl += 'books/'

    // call on page loading
    loadBooks();

    var $searchForm = $('#searchBookByTitle');

    $searchForm.submit(function (evt) {
        evt.preventDefault();
        loadBooks(getFormData($searchForm));
    });


    $('#bookModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var book = {
            id: button.data('book-id'),
            title: button.data('book-title'),
            description: button.data('book-description'),
            url: button.data('book-url'),
        };

        // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        var modal = $(this);
        modal.find('.modal-title').text('Edit book with id: ' + book.id);

        var form = modal.find('form');
        form.find('#id').val(book.id);
        form.find('#title').val(book.title);
        form.find('#description').val(book.description);
        form.find('#url').val(book.url);

        modal.find('#saveButton').click(function (evt) {
            evt.preventDefault();

            var formData = getFormData(form);
            var promise = updateBook(formData);

            promise.done(function (updatedBook) {
                console.log(updatedBook);
                modal.modal('hide');
            })

        })
    })


    function getFormData(form) {
        var data = form.serializeArray();
        var params = {};

        data.forEach(function (element, index) {
            params[element.name] = element.value;
        })

        return params
    }

    function updateBook(book) {
        console.log(book);

        book.id = parseInt(book.id);

        return $.ajax({
            url: apiUrl + book.id,
            data: JSON.stringify(book),
            dataType: 'json',
            method: 'PUT'
        }).done(function (updatedBook) {
            loadBooks();
            return updateBook;
        })
    }

    function loadBooks(params) {
        params = params || {};
        $.getJSON(apiUrl, params).done(function (data) {
            console.log('called');
            $("#template-container").loadTemplate("/templates/book.tpl.html", data);
        });
    }

})(window.jQuery);
