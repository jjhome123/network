document.addEventListener('DOMContentLoaded', () => {
    edit = document.querySelectorAll('.edit');
    edit.forEach(edit => {
        edit.addEventListener('click', () => {
            edit_entry(edit.dataset.post_id)
        })
    });
});

function edit_entry(post_id) {
    field = document.querySelector(`#edit_field${post_id}`);
    post_body = document.querySelector(`#post_body${post_id}`)
    field.style.display = 'block';
    post_body.style.display = 'none';
}