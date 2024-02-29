document.addEventListener("DOMContentLoaded", function () {
    var backToTopButton = document.getElementById("back-to-top-btn");
  
    // Show/hide the button based on scroll position
    window.addEventListener("scroll", function () {
      if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        backToTopButton.style.display = "block";
      } else {
        backToTopButton.style.display = "none";
      }
    });
  
    // Scroll to the top when the button is clicked
    backToTopButton.addEventListener("click", function () {
      document.body.scrollTop = 0; // For Safari
      document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE, and Opera
    });
  });
  
// ===========================================================================================================
// ===========================================================================================================
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