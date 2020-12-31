
document.addEventListener('DOMContentLoaded', function() {

    let edit = document.querySelector('.edit');

    if(edit){
        
        let edits = document.querySelectorAll('.edit');
        for(let i=0 ; i < edits.length ; i++){
            edits[i].addEventListener('click' , (event) => { show_edit(event) });
        }

        let saves = document.querySelectorAll('.edit-form');
        for(let i=0 ; i<saves.length; i++){
            saves[i].addEventListener('submit' , (event)=> { save_edit(event) });
        }

    }

    let like_buttons = document.querySelectorAll('.like');
    for(let i=0; i < like_buttons.length; i++){
        like_buttons[i].addEventListener('click' , (event)=>{ like_post(event) });
    }
    
});


function show_edit(event){

    const parent_div = event.target.parentNode.parentNode;
    
    // hide content
    const cur_content = parent_div.querySelector('.content');
    cur_content.style.display = 'none';
    
    // hide edit link
    const edit = parent_div.querySelector('.edit');
    edit.style.display = 'none';
    
    // display edit form
    const form = parent_div.querySelector('.edit-form');
    form.style.display = 'block';

}


function save_edit(event){

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

}


function like_post(event){

    event.preventDefault();

    const button = event.target;
    const parent_div = button.parentNode.parentNode;
    const post_id = parent_div.querySelector('.id').innerHTML;
    

    const counts = parent_div.querySelector('.count');
    const num_likes = parseInt(counts.innerHTML);
    
    fetch(`/like/${post_id}`)
    .then(response => response.json())
    .then( (result) => {
        if(result["to_like"]){
            button.style.color = 'red';
            counts.innerHTML = num_likes+1;
        }
        else{
            button.style.color = 'grey';
            counts.innerHTML = num_likes-1;
        }
    })
    .catch((error) => {
        console.error(error);
    });

}