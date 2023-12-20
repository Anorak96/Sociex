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

