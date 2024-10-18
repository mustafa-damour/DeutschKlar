const container = document.getElementById("dashboard");

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






function injectUserCard(id, data) {
  
}