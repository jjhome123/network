document.addEventListener('DOMContentLoaded', () => {
    
    // Adds edit functionality to edit buttons on profile or index page
    edit = document.querySelectorAll('.edit');
    edit.forEach(edit => {
        edit.addEventListener('click', () => {
            field = document.querySelector(`#edit_field${edit.dataset.post_id}`);
            post_body = document.querySelector(`#post_body${edit.dataset.post_id}`);
            field.style.display = 'block';
            post_body.style.display = 'none';
        });
    });
    e_button = document.querySelectorAll('.edit-button');
    e_button.forEach(button => {
        button.addEventListener('click', () => {            
            csrftoken = button.parentElement.firstElementChild.value; // This is the csrf token value
            request = new Request(
                `/post/${button.dataset.button_num}`,
                {
                    method: "POST",
                    headers: {"X-CSRFToken": csrftoken},
                }
            );
            fetch(request, {
                body: JSON.stringify({
                    post_id: button.dataset.button_num,
                    post: document.querySelector(`#edit_post_body${button.dataset.button_num}`).value,
                })
            })

            setTimeout(() => {
                fetch(`/post/${button.dataset.button_num}`)
                .then(response => {
                    return response.json()
                })
                .then(result => {
                    document.querySelector(`#post_body${button.dataset.button_num}`).firstElementChild.innerHTML = result["post"];
                    field = document.querySelector(`#edit_field${button.dataset.button_num}`);
                    post_body = document.querySelector(`#post_body${button.dataset.button_num}`);
                    field.style.display = 'none';
                    post_body.style.display = 'block';
                })
            }, 150)
        })
    })

    // Adds follow functionality to follow button on profile page
    follows();

    // Adds like functionality to like buttons on profile or index page
    likes();

});


function likes() {
    like = document.querySelectorAll('.like_button');
    n = document.querySelectorAll('.like_num');
    n.forEach(n => {
        fetch(`/likes/${n.dataset.num_id}`)
            .then(response => response.json())
            .then(result => {
                document.querySelector(`#like-count${n.dataset.num_id}`).innerHTML = result["post_likes"];
            });
    })
    like.forEach(like => {
        fetch(`/likes/${like.dataset.like_id}`)
        .then(response => response.json())
        .then(result => {
            if (result["post_liked"] == true) {
                like.innerHTML = '❤️';
            }
        });
        like.addEventListener('mouseover', () => {
            like.style.cursor = 'pointer';
        });
        like.addEventListener('click', () => {
            if (like.innerHTML === '🤍') {
                fetch(`/likes/${like.dataset.like_id}`, {
                    method: "POST",
                    body: JSON.stringify({
                        post_id: like.dataset.like_id,
                        liked: true,
                    })                  
                })
                .catch(error => {
                    console.log('Error:', error);
                });
                setTimeout(() => {
                    fetch(`/likes/${like.dataset.like_id}`)
                    .then(response => response.json())
                    .then(result => {
                        document.querySelector(`#like-count${like.dataset.like_id}`).innerHTML = result["post_likes"];
                        like.innerHTML = '❤️';
                    })
                    .catch(error => {
                        console.log('Error:', error);
                    });
                }, 150);
            } else {
                fetch(`/likes/${like.dataset.like_id}`, {
                    method: "POST",
                    body: JSON.stringify({
                        post_id: like.dataset.like_id,
                        liked: false,
                    })
                })
                .catch(error => {
                    console.log('Error:', error);
                });
                setTimeout(() => {
                    fetch(`/likes/${like.dataset.like_id}`)
                    .then(response => response.json())
                    .then(result => {
                        document.querySelector(`#like-count${like.dataset.like_id}`).innerHTML = result["post_likes"];
                        like.innerHTML = '🤍';
                    })
                    .catch(error => {
                        console.log('Error:', error);
                    });
                }, 150);
            }
        });
    });
}


function follows() {
    user = document.querySelector('h5').innerHTML;
    if (document.querySelector('h3').innerHTML !== 'Your Profile') {
        follow_button = document.querySelector('#follow');
        if (follow_button !== null) {
            follow_button.onclick = () => {
                if (follow_button.innerHTML.includes(' Follow')) {
                    fetch(`/profile/${user}`, {
                        method: "POST",
                        body: JSON.stringify({
                            follow: true
                        })
                    })
                    follow_button.innerHTML = 'Unfollow';
                } else if (follow_button.innerHTML.includes('Unfollow')) {
                    fetch(`/profile/${user}`, {
                        method: "POST",
                        body: JSON.stringify({
                            follow: false
                        })   
                    })
                    follow_button.innerHTML = ' Follow';
                }
                setTimeout(() => {
                    fetch(`/user-data/${user}`)
                    .then(response => response.json())
                    .then(result => {
                        document.querySelector('#follower-num').innerHTML = result["followers"];
                        document.querySelector('#following-num').innerHTML = result["following"];
                    });
                },100);
            }
        }
    }
}