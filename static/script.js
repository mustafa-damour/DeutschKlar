log = console.log;

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

function validateRegForm() {
  let fname = document.forms["RegForm"]["fname"].value;
  let lname = document.forms["RegForm"]["lname"].value;
  let handle = document.forms["RegForm"]["handle"].value;
  let email = document.forms["RegForm"]["email"].value;
  let password = document.forms["RegForm"]["password"].value;
  let confirm_password = document.forms["RegForm"]["confirm_password"].value;
  // let age = document.forms["RegForm"]["age"].value;
  // let gender = document.forms["RegForm"]["gender"].value;
  // let level = document.forms["RegForm"]["level"].value;
  // let city = document.forms["RegForm"]["city"];

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

const data = {
  uid: 238746,
  cid: 2342,
  role: "User",
  handle: "marco",
  name: "Mark Twain",
  email: "marco123@aio.jp",
};

function injectUserCard() {
  let cardId = data.cid;
  let userId = data.uid;
  let role = data.role;
  let handle = data.handle;
  let name = data.name;
  let email = data.email;
  let inner = `
      <div class="card-header">
      <span class="role">${role}</span>
        <span class="handle">@${handle}</span>
      </div>
      <div class="contacts-container">

        <span class="contact">${name}</span>
        <span class="contact">${email}</span>
      </div>
`;
  let cardContainer = document.createElement("div");
  cardContainer.className = "card-container";
  cardContainer.id = `c-u${userId}-${cardId}`;
  cardContainer.innerHTML = inner;
  dashboard.appendChild(cardContainer);
}

function refresh() {
  const dashboard = document.getElementById("dashboard");
  injectUserCard();
  console.log("User card is allegedly inject into the dashboard");
}

window.onload = function () {
  refresh();
};
