

// document.addEventListener("DOMContentLoaded", () => {
//     let nav_next_button = document.getElementById("navbar-next-button");

//     let all_radios = Array.from( document.querySelectorAll("[type='radio']"));
//     let all_radios_checked = all_radios.map(x => x.checked)
//     all_radios_checked.push(true);
//     console.log(all_radios, all_radios_checked);

//     if (all_radios_checked.some((x) =>  x === true)) {
//         console.log('T')
//     }
//     else {
//         console.log('F')
//     }

// }

// )

// Listen for click on toggle switch

window.addEventListener("DOMContentLoaded", (event) => {

    var switch_dark_mode= document.getElementById("DarkModeSwitchCheckDefault");
    switch_dark_mode.addEventListener("click", (event) => {
        if(switch_dark_mode.checked) {
                    document.body.classList.add("dark_mode");
                } else {
                    document.body.classList.remove("dark_mode");
                    
    }})

});
