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
let form = document.getElementById("follow_form")
console.log(form)
form.addEventListener("submit", follow)

function follow(e) {
    alert('hj')
    // let comm = document.getElementById("id_comment").value
    // const data = { comment : comm };
    // let url = "/post/comment/<pk>/"

    // fetch(url, {
    //     method: 'POST', // or 'PUT'
    //     headers: {
    //         'Content-Type': 'application/json',
    //         'X-CSRFToken': csrftoken,
    //     },
    //     body: JSON.stringify(data),
    // })
    // .then(response => response.json())
    // .then(data => {
    //     console.log('Success:', data);
    // })
    // .catch((error) => {
    //     console.error('Error:', error);
    // });
}