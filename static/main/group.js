$(document).on('submit', '#message_form', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: 'message/',
        data: {
            message: $('message').val(),
            group_pk: $('group_message').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data) {
            $(h5).html(data)
            console.log('success')
            console.log(data)
        }
    })
})
