// static/js/bg-logo.js
// This file is used to handle the background logo, so that it places itself randomly on the screen on every page load.


document.addEventListener("DOMContentLoaded", (event) => {
    // Function to get a random number within a range
    function getRandomNumber(min, max) {
      return Math.random() * (max - min) + min;
    }
  
    // Function to position the logo within a random range
    function positionLogoRandomly() {
      const logo = document.querySelector(".logo");
      const range = 35; // The range in vw units
      const randomTop = getRandomNumber(5, range); // 5vw is the initial top position
      const randomLeft = getRandomNumber(0, range); // 5vw is the initial left position
  
      // Apply the random position to the logo
      logo.style.top = `${randomTop}vw`;
      logo.style.left = `${randomLeft}vw`;
    }
  
    // Get the button by its ID
    const randomPositionButton = document.getElementById(
      "random-bg-logo-position"
    );
  
    // Add click event listener to the button
    randomPositionButton.addEventListener("click", positionLogoRandomly);
  });
  