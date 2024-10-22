
function injectLogs(jsonObj){
  for (log in jsonObj){
  let p = document.createElement('p');
  p.innerHTML=log;
  p.className='log';
  logsContainer.appendChild(p);
  }
}


function inject(jsonObj) {
  const logsContainer = document.getElementById("logs-container");
  injectLogs(jsonObj);
}

window.onload = function () {
  
    const xmlhttp = new XMLHttpRequest();
    xmlhttp.onload = function() {
      const jsonObj = JSON.parse(this.responseText);
      inject(jsonObj);
    }
    xmlhttp.open("GET", "/get_logs", true);
    xmlhttp.send();
  
}


