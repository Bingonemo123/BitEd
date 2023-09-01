
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  

window.addEventListener("DOMContentLoaded", (event) => {

    var switch_dark_mode= document.getElementById("DarkModeSwitchCheckDefault");
    switch_dark_mode.addEventListener("click", (event) => {
        var xhttp = new XMLHttpRequest();
        xhttp.open('POST', '/dark_mode', true);
        var csrftoken = getCookie('csrftoken');
        xhttp.setRequestHeader("X-CSRFToken", csrftoken);
        xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");

        if(switch_dark_mode.checked) {
                    document.body.classList.add("dark_mode");
                    xhttp.send(JSON.stringify({
                        theme: 'dark'
                    }));
                } else {
                    document.body.classList.remove("dark_mode");
                    xhttp.send(JSON.stringify({
                        theme: 'light'
                    }));
                    
    }})

});
