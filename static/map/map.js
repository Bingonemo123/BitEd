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

var requestedTiles = [];

function sendGetAjax(mnode){
    if (requestedTiles.includes(mnode.id))
        {
            return;
        }

    var csrftoken = getCookie('csrftoken');
    var xhttp = new XMLHttpRequest();

    xhttp.onload = function() {
        var jsonTiles = JSON.parse(this.responseText);
        subAccordion_target = mnode.getAttribute('data-bs-target');
        subAccordion_container = document.querySelector(subAccordion_target);
        subAccordion_body = subAccordion_container.querySelector('.accordion-body');
        
        var subAccordion = document.createElement("div");
        subAccordion.class = 'accordion';
        subAccordion.id = `Tile_${mnode.id}_container`;

        for (const subtile of jsonTiles) {
            var subAccordion_item = document.createElement('div');
            subAccordion_item.setAttribute('class', 'accordion-item');

            var subAccordion_button = document.createElement('button');
            subAccordion_button.setAttribute('class', "accordion-button collapsed");
            subAccordion_button.id = `tile-${subtile['pk']}`;
            subAccordion_button.type = 'button';
            subAccordion_button.setAttribute('data-bs-toggle', "collapse");
            subAccordion_button.setAttribute('data-bs-target',
                                            `#tile_target-${subtile['pk']}`);
            subAccordion_button.setAttribute('aria-expanded', 'false');
            subAccordion_button.setAttribute('aria-controls', `tile_target-${subtile['pk']}`);
            subAccordion_button.textContent = subtile['fields']['tile_headline'];
            subAccordion_button.innerHTML += "&nbsp";

            subAccordion_button.addEventListener('click', function() {
                sendGetAjax(this);
            });

            var link_button = `<a href="/tiles/${subtile['pk']}/"><img height="20" width="20" src="/static/map/icon/green-play-button-icon.svg" alt=""></a>`
            subAccordion_button.innerHTML += link_button;
            subAccordion_button.innerHTML += "&nbsp";

            subAccordion_item.appendChild(subAccordion_button);

            var subAccordion_content = document.createElement('div');
            subAccordion_content.id = `tile_target-${subtile['pk']}`;
            subAccordion_content.setAttribute('class', "accordion-collapse collapse");
            subAccordion_button.setAttribute('data-bs-parent', `Tile_${mnode.id}_container`);

            var subAccordion_content_body = document.createElement('div');
            subAccordion_content_body.setAttribute('class', "accordion-body");

            subAccordion_content.appendChild(subAccordion_content_body);
            subAccordion_item.appendChild(subAccordion_content);

            subAccordion.appendChild(subAccordion_item);

        }
        subAccordion_body.appendChild(subAccordion);
        requestedTiles.push(mnode.id);




    }
    xhttp.open('GET', `/map?mnode=${ mnode.id }`, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhttp.send();
};


document.addEventListener('DOMContentLoaded', function() {
    root_button = document.querySelector('#tile-0');
    root_button.addEventListener('click', function() {
        sendGetAjax(this)

    });

});
