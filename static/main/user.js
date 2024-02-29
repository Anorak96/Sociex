// LOGIN
const togglePassword = document.getElementById('togglePassword');
const password = document.getElementById('password');
if (togglePassword) {
    togglePassword.addEventListener('click', () => {
        console.log('btn clicked')

        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        
        if (password.type === "password") {
            document.getElementById('togglePassword').className = "fas fa-eye-slash pwshow";
        } else {
            document.getElementById('togglePassword').className = "fas fa-eye pwshow";
        }
    });
}
// ===============================================================================================
$(document).ready(function() {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $('#profile-button').on('click', '#fllw-btn', function() {
        var userId = $(this).closest('.btn').data('user-id');
        console.log(userId)
        var _url = $(this).data("url");
        console.log(_url)
        $.ajax({
            type: 'POST',
            url: _url,
            data: {
                prof_pk: userId,
                csrfmiddlewaretoken: '{{ csrf_token }}',
            },
            headers: {'X-CSRFToken': csrftoken},
            dataType: 'json',
            success: function(data) {
                console.log('succss:', 'works')
            },
            error: function(error) {
                console.log(error)
            }
        });
    });
});