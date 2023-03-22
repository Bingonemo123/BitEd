

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

function loadContent() {

    var contentHeight = document.documentElement.scrollHeight
    var winHeight = window.innerHeight;
    var scrTop = document.documentElement.scrollTop || document.body.scrollTop;
    var scrollMargin = contentHeight - (winHeight + scrTop)
    var csrftoken = getCookie('csrftoken');
    console.log(scrollMargin);

    if (scrollMargin <= 200 && end_pagination === false && block_request === false){
        block_request = true;
        page += 1;

        var xhttp = new XMLHttpRequest();

        xhttp.onload = function() {
            var jsonTiles = JSON.parse(this.responseText);
            // https://stackoverflow.com/questions/7327056/appending-html-string-to-the-dom
            var contentEl = document.querySelector('.content-container');
            contentEl.insertAdjacentHTML( 'beforeend', jsonTiles.scroll_content);
            block_request = false;
        }
        xhttp.open('GET', '/', true);
        xhttp.setRequestHeader("X-CSRFToken", csrftoken);
        xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xhttp.send();
        return true
        }
    };
var page = 1;
var block_request = false;
let end_pagination = false;
    
document.addEventListener('DOMContentLoaded', function() {
    // Send Signal that client is near the end of feed on scroll
    // 1. Get size of working are space -> window innerHeight
    // 2. Get nav bar size by getting content div location (not needed)
    // 3. Calculating visible size height by client ( not needed)
    // (must be recalculated on window resize)
    // 4. Getting height of content div (scrollHeight)
    // https://www.javascripttutorial.net/javascript-dom/javascript-width-height/


    // https://stackoverflow.com/questions/48443225/listening-to-scroll-event-on-window-vs-on-document-leads-to-conflict-between-ha
    for (const x of Array(5).keys()) {
        var csrftoken = getCookie('csrftoken');
        var xhttp = new XMLHttpRequest();

        xhttp.onload = function() {
            var jsonTiles = JSON.parse(this.responseText);
            // https://stackoverflow.com/questions/7327056/appending-html-string-to-the-dom
            var contentEl = document.querySelector('.content-container');
            contentEl.insertAdjacentHTML( 'beforeend', jsonTiles.scroll_content);
            block_request = false;
        }
        xhttp.open('GET', '/', true);
        xhttp.setRequestHeader("X-CSRFToken", csrftoken);
        xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xhttp.send();
      }
    while (loadContent()==true){}

    window.onscroll = loadContent;

});
