$(document).on('submit', '#chatform', function (e) {
    e.preventDefault();
    
    let _body = $("#id_body").val()
    console.log(_body)
    let _receiver_user = $('#receiver_user').val()
    console.log(_receiver_user)
    var mydiv = document.getElementById('chatform')
    var _url = mydiv.getAttribute('data-url')
    console.log('URL:', _url)
    
    $.ajax({
        type: "POST",
        url: _url,
        data: {
            body: _body,
            receiver_user: _receiver_user,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(success) {
            console.log(success)
            console.log(data)
        },
        error: function(error) {
            console.log(error)
        }
    });
    document.getElementById("body").value=""
});