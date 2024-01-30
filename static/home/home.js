// function getCookie(name) {
//   var cookieValue = null;
//   if (document.cookie && document.cookie !== '') {
//       var cookies = document.cookie.split(';');
//       for (var i = 0; i < cookies.length; i++) {
//           var cookie = cookies[i].trim();
//           // Does this cookie string begin with the name we want?
//           if (cookie.substring(0, name.length + 1) === (name + '=')) {
//               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//               break;
//           }
//       }
//   }
//   return cookieValue;
// }

// function loadContent() {

//     // The scrollHeight property returns the height of an element including padding, but excluding borders, scrollbars, or margins.
//     // Document.documentElement returns the Element that is the root element of the document (for example, the <html> element for HTML documents).
//     var docHeight = document.documentElement.scrollHeight // document.documentElement should resolve on root element with highest height
//     var winHeight = window.innerHeight; 
//     // var contentHeight = document.querySelector('.content-container').scrollHeight;
//     // var navbarHeight = document.querySelector('.navigation-bar').scrollHeight;
//     // var scrollingScreenHeight = winHeight - navbarHeight; 

//     var scrTop = document.documentElement.scrollTop || document.body.scrollTop;
//     var scrollMargin = docHeight - (winHeight + scrTop)
//     var csrftoken = getCookie('csrftoken');
    

//     if (scrollMargin <= 200 && end_pagination === false){ // && block_request === false
//         block_request = true;
//         page += 1;

//         var xhttp = new XMLHttpRequest();

//         xhttp.onload = function() {
//             var jsonFolders = JSON.parse(this.responseText);
//             // https://stackoverflow.com/questions/7327056/appending-html-string-to-the-dom
//             // var contentEl = document.querySelector('.grid-container');
//             firstLoadingFolder = document.getElementById("loading_folder");
//             console.log(firstLoadingFolder);
//             firstLoadingFolder.insertAdjacentHTML("beforebegin", jsonFolders.scroll_content);
//             firstLoadingFolder.remove();
//             block_request = false;
//             loadContent();
//         }
//         xhttp.open('GET', '/', true);
//         xhttp.setRequestHeader("X-CSRFToken", csrftoken);
//         xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
//         xhttp.send();
//         var contentEl = document.querySelector('.grid-container');
//         var loadingFolder =  document.querySelector('#template_folder').cloneNode(true);
//         loadingFolder.classList.remove("d-none");
//         loadingFolder.id = "loading_folder";
//         contentEl.insertAdjacentElement( 'beforeend', loadingFolder);
//         return true
//         }
//     };
// var page = 1;
// var block_request = false;
// let end_pagination = false;
    
// document.addEventListener('DOMContentLoaded', function() {
//     // Send Signal that client is near the end of feed on scroll
//     // 1. Get size of working are space -> window innerHeight
//     // 2. Get nav bar size by getting content div location (not needed)
//     // 3. Calculating visible size height by client ( not needed)
//     // (must be recalculated on window resize)
//     // 4. Getting height of content div (scrollHeight)
//     // https://www.javascripttutorial.net/javascript-dom/javascript-width-height/


//     // https://stackoverflow.com/questions/48443225/listening-to-scroll-event-on-window-vs-on-document-leads-to-conflict-between-ha
//     // for (const x of Array(5).keys()) {
//     //     var csrftoken = getCookie('csrftoken');
//     //     var xhttp = new XMLHttpRequest();

//     //     xhttp.onload = function() {
//     //         var jsonFolders = JSON.parse(this.responseText);
//     //         // https://stackoverflow.com/questions/7327056/appending-html-string-to-the-dom
//     //         var contentEl = document.querySelector('.content-container');
//     //         contentEl.insertAdjacentHTML( 'beforeend', jsonFolders.scroll_content);
//     //         block_request = false;
//     //     }
//     //     xhttp.open('GET', '/', true);
//     //     xhttp.setRequestHeader("X-CSRFToken", csrftoken);
//     //     xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
//     //     xhttp.send();
//     //   }
//     while (loadContent()==true){}
//     window.onscroll = loadContent;

// });
