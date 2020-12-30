
document.addEventListener('DOMContentLoaded', function() {

    let edit = document.querySelector('.edit');

    if(edit){
        let edits = document.querySelectorAll('.edit');

        for(let i=0 ; i < edits.length ; i++){
            edits[i].addEventListener('click' , (event) => {
                
                const parent_div = event.target.parentNode.parentNode;
                const post_id = parent_div.querySelector('.id').innerHTML;
               
                // hide content
                const cur_content = parent_div.querySelector('.content');
                cur_content.style.display = 'none';
                
                // hide edit link
                const edit = parent_div.querySelector('.edit');
                edit.style.display = 'none';
                
                // display edit form
                const form = parent_div.querySelector('.edit-form');
                form.style.display = 'block';
               

               
            })
        }

        let saves = document.querySelectorAll('.edit-form');
        for(let i=0 ; i<saves.length; i++){
            saves[i].addEventListener('submit' , (event)=> {
                
                event.preventDefault();
                

                const parent_div = event.target.parentNode;
                const post_id = parent_div.querySelector('.id').innerHTML;
               
                // update change in content and display
                const new_content = parent_div.querySelector('.new-content').value;
                const cur_content = parent_div.querySelector('.content');
                cur_content.innerHTML = new_content;
                cur_content.style.display = 'block';
                
                // display edit link
                const edit = parent_div.querySelector('.edit');
                edit.style.display = 'block';
                
                // hide edit form
                const form = parent_div.querySelector('.edit-form');
                form.style.display = 'none';

                console.log(new_content);
                //save new content in db
                fetch(`/edit/${post_id}` , {
                    method: 'PUT',
                    body: JSON.stringify({
                        content : new_content
                    })
                })
                .then(response => response.json())
                .then( (result) => {
                    console.log(result);
                })
                .catch((error) => {
                    console.error(error);
                });
              
            })
        }

    }
});