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

    const introData = localStorage.getItem('introSeenTimestamp');
    const now = new Date().getTime();

    const ONE_HOUR = 60 * 60 * 1000;

    if (!introData || now - parseInt(introData) > ONE_HOUR) {
        // Show intro
        realLogoContainer.style.opacity = 0;

        setTimeout(() => {
            screen.classList.add('reveal-bg');
        }, 300);

        setTimeout(() => {
            screen.classList.add('show-logo');
        }, 800);

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

        setTimeout(() => {
            screen.style.transition = 'opacity 1s ease';
            screen.style.opacity = 0;

            realLogoContainer.style.transition = 'opacity 0.5s ease';
            realLogoContainer.style.opacity = 1;

            content.style.transition = 'opacity 1s ease';
            content.style.opacity = 1;

            setTimeout(() => {
                screen.style.display = 'none';
                localStorage.setItem('introSeenTimestamp', now.toString()); // Save new timestamp
            }, 1000);
        }, 3700);

    } else {
        // Skip intro
        screen.style.display = 'none';
        realLogoContainer.style.opacity = 1;
        content.style.opacity = 1;
    }
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
