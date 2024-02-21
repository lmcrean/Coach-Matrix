// static/js/login.js
// This file is used to handle the login form, specifically the following features:
// 1. Video pause/play
// 2. Signup and login form toggle

var video = document.getElementById("myVideo");
var btn = document.getElementById("pause-video");

function pauseVideo() {
  if (video.paused) {
    video.play();
    btn.innerHTML = "Pause video";
  } else {
    video.pause();
    btn.innerHTML = "Play video";
  }
}

function toggleSignup() {
  // Set styles for the signup button to appear active
  document.getElementById("signup-toggle").style.backgroundColor =
    "var(--primary-color)";
  document.getElementById("signup-toggle").style.color = "#fff";

  // Set styles for the login button to appear inactive
  document.getElementById("login-toggle").style.backgroundColor = "#fff";
  document.getElementById("login-toggle").style.color = "var(--primary-color)";

  // Toggle the form display
  document.getElementById("login-form").style.display = "none";
  document.getElementById("signup-form").style.display = "block";
}

function toggleLogin() {
  // Set styles for the login button to appear active
  document.getElementById("login-toggle").style.backgroundColor =
    "var(--primary-color)";
  document.getElementById("login-toggle").style.color = "#fff";

  // Set styles for the signup button to appear inactive
  document.getElementById("signup-toggle").style.backgroundColor = "#fff";
  document.getElementById("signup-toggle").style.color = "var(--primary-color)";

  // Toggle the form display
  document.getElementById("signup-form").style.display = "none";
  document.getElementById("login-form").style.display = "block";
}
