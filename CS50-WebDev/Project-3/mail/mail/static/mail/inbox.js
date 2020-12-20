document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);
    document.querySelector('#compose-form').addEventListener('submit', event => send_email(event));

    // By default, load the inbox
    load_mailbox('inbox');
});

window.onpopstate = function(event){
  if(event.state.now === 'compose'){
    compose_email();
  }
  else{
    load_mailbox(event.state.now);
  }
}

function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#single-view').style.display = 'none';
    document.querySelector('#mail-archive').style.display = 'none';
    document.querySelector('#mail-unarchive').style.display = 'none';
    document.querySelector('#reply-button').style.display = 'none';

    history.pushState({now : "compose"} , "" , "");
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#single-view').style.display = 'none';
    document.querySelector('#mail-archive').style.display = 'none';
    document.querySelector('#mail-unarchive').style.display = 'none';
    document.querySelector('#reply-button').style.display = 'none';

    history.pushState({now : mailbox} , "" , "");

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    // load relevant emails
    load_content(mailbox);
}

function send_email(event){

    // stop automatic form submission to url
    event.preventDefault();

    recipients = document.querySelector('#compose-recipients').value;
    subject = document.querySelector('#compose-subject').value;
    body = document.querySelector('#compose-body').value;


    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients : recipients,
        subject : subject,
        body: body
      })
    })
    .then(response => response.json())
    .then( _ => {
      load_mailbox('sent');
    })
    .catch((error) => {
      console.error(error);
    });

}

// load the emails
function load_content(mailbox){

    // start clean very loading each time
    document.querySelector('#emails-view').innerHTML =  `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      emails.forEach(add_email);
    })
    .catch((error) => {
      console.error(error);
    });
}

function add_email(contents){

    const email = document.createElement('div');
    email.classList.add("email-card");
    const message = 
    `<h4>${contents.subject}</h4>
    <p><b>From:</b> ${contents.sender}</p>
    <p><b>Sent at:</b> ${contents.timestamp}</p>`;
    email.innerHTML = message;

    //Event listener for viewing the email
    const id = contents.id;
    email.addEventListener('click' , () => display_email(id));
    
    if(contents.read){
      email.style.backgroundColor = "gray";
    }
    else{
      email.style.backgroundColor = "white";
    }

    document.querySelector('#emails-view').append(email);
  }


function display_email(id){

    // Show the single email and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#single-view').style.display = 'block';
    document.querySelector('#mail-archive').style.display = 'none';
    document.querySelector('#mail-unarchive').style.display = 'none';

    // Selectively display archive buttons
    if(history.state.now === "inbox"){
      document.querySelector('#reply-button').style.display = 'inline';
      document.querySelector('#mail-archive').style.display = 'inline';
      document.querySelector('#mail-archive').addEventListener('click' , () => archive_mail(id));
      document.querySelector('#reply-button').addEventListener('click' , () => reply_email(id));
    }
    else if(history.state.now === "archive"){
      document.querySelector('#reply-button').style.display = 'inline';
      document.querySelector('#mail-unarchive').style.display = 'inline';
      document.querySelector('#mail-unarchive').addEventListener('click' , () => unarchive_mail(id));
      document.querySelector('#reply-button').addEventListener('click' , () => reply_email(id));
    }

    // clear for each click
    document.querySelector('#single-view').innerHTML = "";

    // get data from api
    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      //console.log(email);
      get_email(email);
    })
    .catch((error) => {
      console.error(error);
    });

    // mark email as read
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read : true
      })
    })
}

function get_email(email){

    const sender = email.sender;
    const recipients = email.recipients.join();
    const subject = email.subject;
    const timestamp = email.timestamp;
    const body = email.body;

    const element = document.createElement('div');
    // display data
    let content = 
    `<br>
    <p><b>From:</b> ${sender}</p>
    <hr>
    <p><b>To:</b> ${recipients}</p>
    <hr>
    <p><b>About:</b> ${subject}</p>
    <hr>
    <p><b>Sent at:</b> ${timestamp}</p>
    <hr>
    <p>${body}</p>`;

    element.innerHTML = content;

    document.querySelector('#single-view').append(element);

}


function archive_mail(id){
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: true
      })
    });
    load_mailbox('inbox');
}

function unarchive_mail(id){
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: false
      })
    })
    load_mailbox('inbox');
}

function reply_email(id){
  
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-view').style.display = 'none';
  document.querySelector('#mail-archive').style.display = 'none';
  document.querySelector('#mail-unarchive').style.display = 'none';
  document.querySelector('#reply-button').style.display = 'none';

  history.pushState({now : "compose"} , "" , "");

  // get original email data
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    const sender = email.sender;
    let subject = email.subject;
    const timestamp = email.timestamp;
    const body = email.body;

    if(!subject.startsWith('Re:')){
      subject = 'Re: ' + subject;
    }

    const newBody =
    `On ${timestamp} ${sender} wrote:
${body}`;

    // pre-fill
    document.querySelector('#compose-recipients').value = sender;
    document.querySelector('#compose-subject').value = subject;
    document.querySelector('#compose-body').value = newBody;
    
  })
  .catch((error) => {
    console.error(error);
  });

}