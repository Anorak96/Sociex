$(document).ready(function() {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $('#post-container').on('click', '#like-button', function() {
        var postId = $(this).closest('.feed').data('post-id');
        console.log(postId)
        var _url = $(this).data("url");
        console.log(_url)
        $.ajax({
            type: 'POST',
            url: _url,
            data: {
                post_pk: postId
            },
            headers: {'X-CSRFToken': csrftoken},
            success: function(data) {
                $("#like-count" + postId).text(data.likes);
                if (data.isliked) {
                    $('#heartIcon' + postId).removeClass('far').addClass('fas')
                } else {
                    $('#heartIcon' + postId).removeClass('fas').addClass('far')
                }
                console.log('likes:', data.likes);
                console.log('likeStatus:', data.isliked);
            },
            error: function(error) {
                console.log(error)
            }
        });
    });
});

  