document.addEventListener('DOMContentLoaded', () => {
    // Adds edit functionality to edit buttons on profile or index page
    edit = document.querySelectorAll('.edit');
    edit.forEach(edit => {
        edit.addEventListener('click', () => {
            edit_entry(edit.dataset.post_id)
        })
    });

    // Adds follow functionality to follow button on profile page
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
});

function edit_entry(post_id) {
    field = document.querySelector(`#edit_field${post_id}`);
    post_body = document.querySelector(`#post_body${post_id}`)
    field.style.display = 'block';
    field.focus();
    post_body.style.display = 'none';
}