
if (window.location.pathname==='/login'){
  localStorage.clear();
}



// login form validation
function validateLoginForm() {
  let handle = document.forms["loginForm"]["handle"].value;
  let password = document.forms["loginForm"]["password"].value;

  if (handle.length <= 3) {
    alert("Name must be more than 3 letters.");
    return false;
  } else if (password.length < 8) {
    alert("Name must be at least 8 chracters/numbers.");
    return false;
  }
}

// Registeration Form validation
function validateRegForm() {
  let fname = document.forms["RegForm"]["fname"].value;
  let lname = document.forms["RegForm"]["lname"].value;
  let handle = document.forms["RegForm"]["handle"].value;
  let email = document.forms["RegForm"]["email"].value;
  let password = document.forms["RegForm"]["password"].value;
  let confirm_password = document.forms["RegForm"]["confirm_password"].value;


  if (fname.length < 3 || lname.length < 3) {
    alert("name must be at least 3 letters.");
    return false;
  }

  if (handle.length < 4) {
    alert("handle must be at least 4 letters.");
    return false;
  }

  if (password !== confirm_password) {
    alert("The password has to be the same.");
    return false;
  }

  if (!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)) {
    alert("Please enter a valid email!  ");
    return false;
  }


}


function validateEditForm() {
  let fname = document.forms["RegForm"]["fname"].value;
  let lname = document.forms["RegForm"]["lname"].value;

  if (fname.length < 3 || lname.length < 3) {
    alert("name must be at least 3 letters.");
    return false;
  }

}


// function to cardify contacts, turning them into card HTML templates
function cardify(
  role,
  handle,
  first_name,
  last_name,
  email,
  statusText
) {

  let inner = `
      <div class="card-header">
      <span class="role">${role}</span>
        <span class="handle">@${handle}</span>
      </div>
      <div class="contacts-container">

        <p class="contact">full name ${first_name} ${last_name}</p>
        <p class="contact"><a href="mailto:${email}">${email}</a></p>
        <div class="status-container">
          <img class="status-icon"src="static/status.svg">
          <p class="status-p">${statusText}</p>
        </div>
        
      </div>
`;

return inner;
}

let tHandle = '';

function injectUserCard(jsonObj) {
  let user = jsonObj['user'];
  let moderator = jsonObj['moderator'];
  let members = jsonObj['members'];
  let cardIdCount = 0;
  tHandle = user['handle'];
  if(!(localStorage.getItem('suffix'))&&(user['handle'])){
    localStorage.setItem('suffix', ` | @${tHandle}`);
    sessionStorage.setItem('same', 'True');
    document.title+=(localStorage.getItem('suffix'));
    document.getElementById('profile-nav').style.visibility='visible';
    document.getElementById('login-logout').innerText='logout ';

  }

  // removing loader when cards are loaded
  let cardsLoader = document.getElementById("cards-loader");
  dashboard.removeChild(cardsLoader);

  // Moderator card

  const cardHTML = cardify(
    role='Moderator',
    handle=moderator['handle'],
    first_name=moderator['first_name'],
    last_name=moderator['last_name'],
    email=moderator['email'],
    statusText=moderator['status']
  );
  let moderatorId = moderator['id']
  let cardContainer = document.createElement("div");
  cardContainer.className = "card-container";
  cardContainer.id = `c-m${moderatorId}-${cardIdCount}`;
  cardContainer.innerHTML = cardHTML;
  dashboard.appendChild(cardContainer);
  cardIdCount+=1;

  // Injecting members cards
  for (member in members){

    member = members[member];

    if (member['id']===user['user_id']){
      continue;
    }
    let cardHTML = cardify(
      role='Member',
      handle=member['handle'],
      first_name=member['first_name'],
      last_name=member['last_name'],
      email=member['email'],
      statusText=member['status']
    );
    let userId = member['id']
    let cardContainer = document.createElement("div");
    cardContainer.className = "card-container";
    cardContainer.id = `c-u${userId}-${cardIdCount}`;
    cardContainer.innerHTML = cardHTML;
    dashboard.appendChild(cardContainer);
    cardIdCount+=1;
  }

  
}

// refreshing page by injecting fetched data

function refresh(jsonObj) {
  const dashboard = document.getElementById("dashboard");
  injectUserCard(jsonObj);
}


function setFields(jsonObj){
  document.getElementById('edit-fname').value = jsonObj['first_name'];
  document.getElementById('edit-lname').value = jsonObj['last_name'];
  document.getElementById('edit-phone-number').value = jsonObj['phone_number'];
  document.getElementById('edit-age').value = jsonObj['age'];
  document.getElementById('edit-level').value = jsonObj['level'];

  if(localStorage.hasOwnProperty('cached-fields')){
    if (localStorage.getItem('cached-fields')!==JSON.stringify(jsonObj)){
      alert('Info has been updated sucessfully.');
      localStorage.setItem('cached-fields', JSON.stringify(jsonObj));
    }
  }
  else{
      localStorage.setItem('cached-fields', JSON.stringify(jsonObj));
  }
  

}


function injectProfile(jsonObj){

  const profileContainer = document.getElementById('profile-container');

  let handle = jsonObj['handle'];
  let fname = jsonObj['first_name'];
  let lname = jsonObj['last_name'];
  let email = jsonObj['email'];
  let phone_number = jsonObj['phone_number'];
  let age = jsonObj['age'];
  let gender = jsonObj['gender'];
  let level = jsonObj['level'];
  let city = jsonObj['city'];
  let status = jsonObj['status'];


  profileContainer.innerHTML = `
  
        <div id="profile-details" class="profile-details">
            <img class="profile-pic" alt="Flag of Germany" src="static/germany-flag.jpg">
            <p class="profile-contact"> Handle | @${handle} (fixed) </p>
            <p class="profile-contact"> Name | ${fname} ${lname}</p>
            <p class="profile-contact"> Email | ${email} (fixed)</p>
            <p class="profile-contact"> Phone Number | ${phone_number}</p>
            <p class="profile-contact"> Age | ${age} years old</p>
            <p class="profile-contact"> Gender | ${gender} (fixed) </p>
            <p class="profile-contact"> Language Level | ${level} </p>
            <p class="profile-contact"> City | ${city} (fixed)</p>

            <a href="/edit"><button id="edit-profile" class="edit-profile">Edit</button></a>

        <h2 class="status-title">Status</h2>
        
        <form class="status" action="/update_status" method="post">
            <textarea type="text" name="status" id="status" class="status-field">${status}</textarea>
                <input type="submit" value="Update">
        </form>
        </div>
  
  `;


}




window.onload = function () {

  if (window.location.pathname==='/login'){
    document.getElementById('profile-nav').style.visibility='hidden';
    document.getElementById('login-logout').innerText='login';

  }

  if(localStorage.getItem('suffix')){
    document.title+=(localStorage.getItem('suffix'));
    document.getElementById('profile-nav').style.visibility='visible';
    document.getElementById('login-logout').innerText='logout';

  }


  const loginLogoutButton = document.getElementById("login-logout");

  loginLogoutButton.addEventListener('click', function(event){
    // if value exists and user click, they are logging out
    if(localStorage.getItem('suffix')){
      localStorage.removeItem('suffix');
    }
    window.location.href('/in_out');
  });

  // onload preparations

  if (window.location.pathname==='/dashboard'){
    const xmlhttp = new XMLHttpRequest();
    xmlhttp.onload = function() {
      const jsonObj = JSON.parse(this.responseText);
      refresh(jsonObj);
    }
    xmlhttp.open("GET", "/cards", true);
    xmlhttp.send();
  }

  
  if (window.location.pathname==='/edit'){
    const xmlhttp = new XMLHttpRequest();
    xmlhttp.onload = function() {
      const jsonObj = JSON.parse(this.responseText);
      setFields(jsonObj);
    }
    xmlhttp.open("GET", "/fields", true);
    xmlhttp.send();
  }


  if (window.location.pathname==='/profile'){
    const xmlhttp = new XMLHttpRequest();
    xmlhttp.onload = function() {
      const jsonObj = JSON.parse(this.responseText);
      injectProfile(jsonObj);
    }
    xmlhttp.open("GET", "/get_profile", true);
    xmlhttp.send();
  }

}