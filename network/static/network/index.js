document.addEventListener('DOMContentLoaded', function() {

    // Select all edit tags
    let edit_tags = document.querySelectorAll("#edit")
    for (let i = 0; i < edit_tags.length; i++) {
        edit_tags[i].addEventListener('click', () => {

            //Get the parent element
            const button_parent = edit_tags[i].parentElement;
            const text_field = button_parent.children[1];
            const post_id = button_parent.children[4].dataset.edit;

            if(edit_tags[i].textContent === 'Edit') {
                
                //Create new child element
                const new_input = document.createElement('textarea');
                new_input.classList = 'form-control';
                new_input.value = text_field.textContent;
                button_parent.insertBefore(new_input, text_field);
                text_field.remove();

                //Change edit button to save
                edit_tags[i].textContent = 'Save';
                console.log(new_input.value);
            } else if(edit_tags[i].textContent === 'Save') {
                const change_input = text_field;
                console.log(post_id)
                edited_text = document.createElement('p');
                edited_text.textContent = change_input.value;
                button_parent.insertBefore(edited_text, text_field);
                change_input.remove();

                edit_tags[i].textContent = 'Edit';
                console.log(change_input);

                //Send a POST request to update the database
                fetch("/save", {
                    method: 'POST',
                    body: JSON.stringify({
                        post_id: post_id,
                        content: edited_text.textContent
                    })
                })
            }
        })
    }

    // Select all like tags
    let like_tags = document.querySelectorAll("#like")
    for (let j = 0; j < like_tags.length; j++) {
        like_tags[j].addEventListener('click', () => {

            const like_post_id = like_tags[j].dataset.like;

            //Change 'Like to 'Unlike' and vice versa
            if (like_tags[j].textContent === "Like") {
                like_tags[j].classList.remove('btn-info');
                like_tags[j].classList.add('btn-secondary');
                like_tags[j].textContent = "Unlike";

                //Send a POST request to update the database with a like
                fetch("/like", {
                    method: 'POST',
                    body: JSON.stringify({
                        post_id: like_post_id,
                        like: "like"
                    })
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result)
                //Update the like number
                like_number = document.querySelector(`#like-count-${like_post_id}`);
                like_number.textContent = result["like_count"]
                })

                //Below updates the number without using data from the response
                
                //like_number_int = parseInt(like_number.textContent);
                //like_number_int = like_number_int + 1;
                //like_number.textContent = like_number_int;

            } else {
                like_tags[j].classList.add('btn-info');
                like_tags[j].classList.remove('btn-secondary');
                like_tags[j].textContent = "Like";

                //Send a POST request to update the database with an unlike
                fetch("/like", {
                    method: 'POST',
                    body: JSON.stringify({
                        post_id: like_post_id,
                        like: "unlike"
                    })
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                
                //Update the like number
                like_number = document.querySelector(`#like-count-${like_post_id}`);
                like_number.textContent = result["like_count"];
                })
                
                //Below updates the number without using data from the response

                //like_number_int = parseInt(like_number.textContent);
                //like_number_int--;
                //like_number.textContent = like_number_int;
            }
        })
    }
})