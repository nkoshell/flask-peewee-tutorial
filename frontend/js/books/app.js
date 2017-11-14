(function ($) {
    var apiUrl = window.apiUrl || 'http://localhost:5000/'; // Get from global ctx or set to 'http://localhost:5000/'
    var categoriesApiUrl = apiUrl + 'categories/';
    apiUrl += 'books/'

    var $searchForm = $('#searchBookByTitle');

    $searchForm.submit(function (evt) {
        evt.preventDefault();
        loadBooks();
    });


    // call on page loading
    loadBooks();
    loadCategories();


    $('#bookModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var book = {
            id: button.data('book-id'),
            title: button.data('book-title'),
            description: button.data('book-description'),
            url: button.data('book-url'),
            categoryId: button.data('book-category-id')
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
        form.find('#categoriesSelector').val(book.categoryId)

        // Call on modal show, bind action every time
        // Must be one time bind .click(callback) (.on('click', callback)) -> .one('click', callback)
        modal.find('#saveButton').one('click', function (evt) {
            evt.preventDefault();

            var formData = getFormData(form);
            var promise = updateBook(formData);

            promise.done(function (updatedBook) {
                console.log(updatedBook);
                modal.modal('hide');
            })

        })
    })

    $('#bookModal').on('hidden.bs.modal', function (e) {
        var modal = $(this);
        modal.find('#saveButton').off('click'); // unbind action
    })


    function getFormData(form, allowEmpty) {
        // if call getFormData($someForm), arg `allowEmpty` === undefined

        console.log('allowEmpty = %s', allowEmpty)

        var data = form.serializeArray();
        var params = {};
        data.forEach(function (element, index) {
            if (!allowEmpty && element.value === ''){
                return // continue for loop
            }
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
        params = params || getFormData($searchForm);
        $.getJSON(apiUrl, params).done(function (data) {
            $("#template-container").loadTemplate("/templates/book.tpl.html", data);
        });
    }

    function loadCategories(params) {
        params = params || {};
        $.getJSON(categoriesApiUrl, params).done(function (data) {
            var options = data.map(function (element, index) {
                return $('<option>', {value: element.id, text: element.title}); // Create select.option element
            });

            $('select#categoriesSelector').append(options); // Append option to select element
        });
    }

})(window.jQuery);
