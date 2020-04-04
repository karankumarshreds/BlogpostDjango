window.onload = initAll;

var like_button;
function initAll(){
    like_button = document.getElementById('like');
    like_button.onclick = random_function;
}

function random_function(){
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            
        }
  };
  req.open("GET", "ajax_info.txt", true);
  req.send();
}