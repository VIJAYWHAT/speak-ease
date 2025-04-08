document.addEventListener("DOMContentLoaded", () => {
    const learnButtons = document.querySelectorAll(".learn-group button");
    const submitButton = document.querySelector(".submit-btn");
    const fromTime = document.getElementById("from-time");
    const toTime = document.getElementById("to-time");
    const errorMessage = document.getElementById("error-message");
  
    // Toggle button selection
    learnButtons.forEach((button) => {
      button.addEventListener("click", () => {
        button.classList.toggle("active");
      });
    });
  
    // Validate availability time
    submitButton.addEventListener("click", (e) => {
      if (parseInt(fromTime.value) >= parseInt(toTime.value)) {
        errorMessage.textContent = "From Time should be less than To Time.";
        errorMessage.style.display = "block";
        e.preventDefault();
      } else {
        errorMessage.style.display = "none";
        alert("Form submitted!");
      }
    });
  });


  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".learn-group button").forEach(button => {
      button.addEventListener("click", () => {
        button.classList.toggle("selected");
      });
    });
  });
  
  
  document.addEventListener("DOMContentLoaded", function () {
    const togglePassword = document.querySelector(".toggle-password");
    const passwordField = document.getElementById("password");
  
    togglePassword.addEventListener("click", function () {
      if (passwordField.type === "password") {
        passwordField.type = "text";
        togglePassword.textContent = "🙈"; // Change icon to hidden
      } else {
        passwordField.type = "password";
        togglePassword.textContent = "👁️"; // Change icon to visible
      }
    });
  });
  document.addEventListener("DOMContentLoaded", function () {
    const contactInput = document.getElementById("contact");
    const errorMessage = document.getElementById("error-message");
  
    contactInput.addEventListener("input", function () {
      const value = contactInput.value.trim();
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Email format
      const phoneRegex = /^\d{10,15}$/; // 10 to 15 digit phone number
  
      if (emailRegex.test(value) || phoneRegex.test(value)) {
        errorMessage.style.display = "none"; // Hide error if valid
      } else {
        errorMessage.style.display = "block"; // Show error if invalid
      }
    });
  });
  

  function toggleSelection(button) {
    button.classList.toggle("selected");
    updateHiddenFields();
}

function updateHiddenFields() {
    document.getElementById("learning_languages").value = 
        Array.from(document.querySelectorAll(".learn-group button.selected[data-value]"))
            .map(btn => btn.getAttribute("data-value")).join(",");

    document.getElementById("learning_reason").value = 
        Array.from(document.querySelectorAll(".reason-group button.selected[data-value]"))
            .map(btn => btn.getAttribute("data-value")).join(",");

    document.getElementById("days").value = 
        Array.from(document.querySelectorAll(".days-group button.selected[data-value]"))
            .map(btn => btn.getAttribute("data-value")).join(",");
}

document.getElementById("login-form").addEventListener("submit", function() {
  let button = document.getElementById("login-button");
  let spinner = document.getElementById("loading-spinner");

  // Show the spinner and disable the button
  spinner.style.display = "block";
  button.classList.add("disabled");
  button.disabled = true;
});

