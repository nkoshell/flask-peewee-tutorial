(function ($) {
     posts = [
        {
            author: 'Joe Bloggs',
            date: '25th May 2013',
            authorPicture: '',
            post: 'This is the contents of my other post'
        },
        {
            author: 'John Blogger',
            date: '25th October 2017',
            authorPicture: '',
            post: 'This is the contents of my other post'
        }
    ]

    $("#template-container").loadTemplate("/templates/book.tpl.html", posts);

})(window.jQuery);
