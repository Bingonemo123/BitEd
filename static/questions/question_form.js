let choiceForm = document.querySelectorAll(".choice-form");
let addButton = document.querySelector("#add-form");
let totalForms = document.querySelector("#id_form-TOTAL_FORMS");
let container = document.querySelector("#form-container");

let formNum = choiceForm.length - 1;
addButton.addEventListener('click', addForm);

function addDeleteEvents() {
    let DeleteButtons = document.querySelectorAll(".delete-form");
    DeleteButtons.forEach((element) => {
        element.addEventListener('click', 
        () => { element.parentNode.remove()} )
    })
}

addDeleteEvents();

function addForm(e){
    e.preventDefault();

    let newForm = choiceForm[0].cloneNode(true);
    let formRegex = RegExp('form-(\\d){1}-', 'g');

    formNum++;
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`);
    container.insertBefore(newForm, addButton)

    totalForms.setAttribute('value', `${formNum+1}`)
    addDeleteEvents();

}
