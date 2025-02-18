//this is the code for an animation? i guess. not really an animation more just changing the photo when clicked.
//javascript is something I learned when I was young, 16-17, so I have not messed with it in around 4
//years. I am going to try to make sense of all of this!!!!!!

//So this function I guess is similar to what goes on in roblox. there is an event listener that checks
//for something to happen. the type is what is confusing me, DOMContentLoaded? let me research it
//It just makes sure the page is loaded IG. so this would be an event!!!! it makes sure itsl oaded
//to actually get everything
const offScreenMenu = document.querySelector('.off-screen-menu');
const dropdown = document.querySelector(".dropdown");
const content = document.querySelector(".content");
//FOR THE CATEGORIES
dropdown.addEventListener("click", function (event) {
        event.stopPropagation(); // Prevents event bubbling
        content.classList.toggle("active");
    });
document.addEventListener("DOMContentLoaded", function() {
    //obviously the menu button is what is waiting to be clicked
    const menuButton = document.getElementById("menu-toggle");
    //then the menu icon is what is going to be changed into another photo
    const menuIcon = document.getElementById("menu-icon");

    // Store the correct static paths manually
    const menuClosed = menuIcon.getAttribute("data-closed");
    const menuOpen = menuIcon.getAttribute("data-open");

    menuButton.addEventListener("click", function() {
        offScreenMenu.classList.toggle('active')
        if (menuIcon.src.includes("linesCLOSED.png")) {
            menuIcon.src = menuOpen; // Change to open icon
        } else {
            menuIcon.src = menuClosed; // Change back
        }
    });
});