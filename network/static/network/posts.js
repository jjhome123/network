document.addEventListener('DOMContentLoaded', () => {
    // Adds edit functionality to edit buttons on profile or index page
    edit = document.querySelectorAll('.edit');
    edit.forEach(edit => {
        edit.addEventListener('click', () => {
            edit_entry(edit.dataset.post_id)
        });
    });

    // Adds follow functionality to follow button on profile page
    follows();

    // Adds like functionality to like buttons on profile or index page
    likes();

});

function edit_entry(post_id) {
    field = document.querySelector(`#edit_field${post_id}`);
    post_body = document.querySelector(`#post_body${post_id}`)
    field.style.display = 'block';
    field.focus();
    post_body.style.display = 'none';
}

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
                    follow_button.innerHTML = 'Un-Follow';
                } else if (follow_button.innerHTML.includes('Un-Follow')) {
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