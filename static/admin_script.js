// Injecting logs into DOM
function injectLogs(jsonObj){
  let logsContainer = document.getElementById("logs-container");
  for (log of jsonObj){
  let p = document.createElement('p');
  p.innerHTML=log;
  p.className='log';
  logsContainer.appendChild(p);
  }
}

// Injecting jsonObj into 
function inject(jsonObj) {
  let logsContainer = document.getElementById("logs-container");

  injectLogs(jsonObj);
}

// onload preparations
window.onload = function () {
  
    const xmlhttp = new XMLHttpRequest();
    xmlhttp.onload = function() {
      const jsonObj = JSON.parse(this.responseText);
      inject(jsonObj);
    }
    xmlhttp.open("GET", "/get_logs", true);
    xmlhttp.send();
  
}


