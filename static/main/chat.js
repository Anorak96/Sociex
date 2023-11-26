function getData() {
    var receivePK = $('#chat_pk').val();
    console.log(receivePK)
    
    var chatPk = "{{ uchat.pk }}"
    var apiUrl = '/chat/';
    console.log(apiUrl)

    $.ajax({
        type: 'GET',
        url: apiUrl,  // Replace with the actual URL of your view
        data: {
            'receiver_user': receivePK,
        },
        success: function (response) {
            $('#result').html('Server response: ' + response);
        }
    });
}
window.onload = function() {
    getData();
};