$(document).ready(function() {
    $('#likeForm').on('submit', function (e) {
        e.preventDefault();
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        
        var postId = $(this).find('button').data("post-id");
        console.log(postId)
        
        var _url = $(this).data("url");
        console.log(_url)
        
        $.ajax({
            type: 'POST',
            url: _url,
            data: {
                post_pk: $('#postpk').val()
            },
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(data) {
                // $("#like-count").text(data.likes)
                $("#like-count" + postId).text(data.likes)
                console.log("it works")
            },
            error: function(error) {
                console.log(error)
            }
        })
    })
})


