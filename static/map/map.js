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

var numberPattern = /\d+/g;


function sendGetAjax(mnode){
    
    var csrftoken = getCookie('csrftoken');
    var xhttp = new XMLHttpRequest();

    xhttp.onload = function() {
        var jsonFolders = JSON.parse(this.responseText);
        var columnNumber = parseInt(
            mnode.parentElement.parentElement.id.match(numberPattern).join(''));

        // make this mnode grey selected

        for (const child of mnode.parentElement.parentElement.children) {
            child.classList.remove("grey-selected");
          }
        
          let templateFolderItem = document.getElementById("root-item");
          
        if (mnode.parentElement != templateFolderItem) {
        mnode.parentElement.classList.add("grey-selected");
        }
        // Delete next nodes


        
        while (mnode.parentElement.parentElement.nextSibling != null ) {
            mnode.parentElement.parentElement.nextSibling.remove();
        }
        
        
        var newColumn = document.createElement("div");
        newColumn.classList.add('base-column');
        newColumn.id = `home-column-${columnNumber + 1}`;
        let columnsContainer = document.querySelector(".column-view");

        for (const subfolder of jsonFolders) {

            var newFolderItem = templateFolderItem.cloneNode(true);

            newFolderItem.querySelector('.folder-link').href = `/folder/${subfolder['pk']}/`;
            newFolderItem.querySelector('.folder-name').innerText = subfolder['fields']['name'];
            var inArrow = newFolderItem.querySelector('#go-in-folder-0');
            inArrow.addEventListener('click', function() {
                sendGetAjax(this);
            });
            inArrow.id = `go-in-folder-${subfolder['pk']}`;
            newFolderItem.removeAttribute("hidden"); 

            newColumn.appendChild(newFolderItem);


        }
        columnsContainer.appendChild(newColumn);

    }
    xhttp.open('GET', `/map?mnode=${ mnode.id }`, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhttp.send();
};


document.addEventListener('DOMContentLoaded', function() {
    let rootFolderButton = document.getElementById("go-in-folder-0");
    sendGetAjax(rootFolderButton);

});
