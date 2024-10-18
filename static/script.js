
function validateForm() {
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




const data = {
  uid: 238746,
  cid: 2342,
  role: "User",
  handle: "marco",
  name: "Mark Twain",
  email: "marco123@aio.jp"

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

function refresh(){
  const dashboard = document.getElementById("dashboard");
  injectUserCard();
  console.log("User card is allegedly inject into the dashboard");
}

dashboard.onload = function() {refresh();}