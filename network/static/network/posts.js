document.addEventListener('DOMContentLoaded', () => {
    // Adds edit functionality to edit buttons on profile or index page
    edit = document.querySelectorAll('.edit');
    edit.forEach(edit => {
        edit.addEventListener('click', () => {
            edit_entry(edit.dataset.post_id)
        })
    });

    // Adds follow functionality to follow button on profile page
    if (document.querySelector('h3').innerHTML !== 'Your Profile') {
        user = document.querySelector('h5').innerHTML;
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
                    .then(document.querySelector('#follower-num').innerHTML = parseInt(document.querySelector('#follower-num').innerHTML) + 1);
                    follow_button.innerHTML = 'Un-Follow';
                } else if (follow_button.innerHTML.includes('Un-Follow')) {
                    fetch(`/profile/${user}`, {
                        method: "POST",
                        body: JSON.stringify({
                            follow: false
                        })   
                    })
                    .then(document.querySelector('#follower-num').innerHTML -= 1);
                    follow_button.innerHTML = ' Follow';
                }
            }
        }
    }
});

function edit_entry(post_id) {
    field = document.querySelector(`#edit_field${post_id}`);
    post_body = document.querySelector(`#post_body${post_id}`)
    field.style.display = 'block';
    field.focus();
    post_body.style.display = 'none';
}