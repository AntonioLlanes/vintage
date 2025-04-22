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
window.addEventListener('load', () => {
    const screen = document.getElementById('intro-screen');
    const introLogo = document.getElementById('intro-logo');
    const realLogo = document.querySelector('.logo img');
    const realLogoContainer = document.querySelector('.logo');
    const content = document.getElementById('site-content');

    // Make sure homepage logo is hidden initially
    realLogoContainer.style.opacity = 0;

    // Step 1: Fade to background color
    setTimeout(() => {
        screen.classList.add('reveal-bg');
    }, 300);

    // Step 2: Show intro logo
    setTimeout(() => {
        screen.classList.add('show-logo');
    }, 800);

    // Step 3: Animate intro logo into homepage logo position
    setTimeout(() => {
        const logoRect = realLogo.getBoundingClientRect();
        const introRect = introLogo.getBoundingClientRect();

        const deltaX = logoRect.left - introRect.left;
        const deltaY = logoRect.top - introRect.top;
        const scaleX = logoRect.width / introRect.width;
        const scaleY = logoRect.height / introRect.height;

        introLogo.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(${scaleX}, ${scaleY})`;
        introLogo.style.transition = 'transform 1s ease-in-out';
    }, 2500);

  // Step 4: Reveal main content and homepage logo
setTimeout(() => {
    // Fade out intro screen
    screen.style.transition = 'opacity 1s ease';
    screen.style.opacity = 0;

    // Fade in real logo
    realLogoContainer.style.transition = 'opacity 0.5s ease';
    realLogoContainer.style.opacity = 1;

    // Fade in page content
    content.style.transition = 'opacity 1s ease';
    content.style.opacity = 1;

    // After fade-out is done, fully remove intro screen
    setTimeout(() => {
        screen.style.display = 'none';
    }, 1000);
}, 3700);
});

// Burger menu & dropdown toggle
document.addEventListener("DOMContentLoaded", () => {
    const offScreenMenu = document.querySelector('.off-screen-menu');
    const dropdown = document.querySelector(".dropdown");
    const dropdownContent = document.querySelector(".content");
    const menuButton = document.getElementById("menu-toggle");
    const menuIcon = document.getElementById("menu-icon");

    const menuClosed = menuIcon.getAttribute("data-closed");
    const menuOpen = menuIcon.getAttribute("data-open");

    dropdown.addEventListener("click", function (event) {
        event.stopPropagation();
        dropdownContent.classList.toggle("active");
    });

    menuButton.addEventListener("click", function () {
        offScreenMenu.classList.toggle('active');
        if (menuIcon.src.includes("linesCLOSED.png")) {
            menuIcon.src = menuOpen;
        } else {
            menuIcon.src = menuClosed;
        }
    });
});
