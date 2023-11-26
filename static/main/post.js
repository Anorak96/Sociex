// =============Detail Like==================================
let post_like = document.getElementById("likeBTN")
let post_id = document.getElementById("post_pk").value
let unliked = document.getElementById("unliked")
let liked = document.getElementById("liked")
let num_of_likes = document.getElementById("like_count")

post_like.addEventListener('click', likePost)

function likePost(e) {
    let url = "/post/<pk>/like/"
    const data = {pk:post_id}

    fetch(url, {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
    })
    .then(res => res.json())
    .then(data => {
        console.log('Success:', data);
        // if(data["check"] == 1){
        //     unliked.classList.remove("far")
        //     liked.classList.add('fa')
        // }
        // else{
        //     unliked.classList.add("far")
        //     unliked.classList.remove('fa')
        // }
        num_of_likes.innerHTML = data["num_of_likes"]
    })
}

// =============Detail Comment==================================
let form = document.getElementById("comment_form")
form.addEventListener("submit", comment)
function comment(e) {
    e.preventDefault()
    let comm = document.getElementById("id_comment").value
    
    const data = { comment : comm };
    let url = "/post/comment/<pk>/"

    fetch(url, {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}