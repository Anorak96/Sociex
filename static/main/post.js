$(document).on('submit', '#post_pk', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '',
        data: {
           csrfmiddlewaretoken: $('') 
        },
        success: function(data) {
            
        }
    })
})
