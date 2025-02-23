 // Generate a random password function
 function generateRandomPassword() {
    const length = 12;
    const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()";
    let password = "";
    for (let i = 0; i < length; i++) {
      password += charset.charAt(Math.floor(Math.random() * charset.length));
    }
    return password;
  }

  // Save password to the list
  function savePassword() {
    const passwordName = document.getElementById("new-password-name").value;
    const passwordValue = document.getElementById("password-display").textContent;

    if (!passwordName || passwordValue === "Your new password will appear here.") {
      alert("Please generate a password and enter a password name.");
      return;
    }

    const passwordItem = document.createElement("div");
    passwordItem.classList.add("password-item");
    passwordItem.innerHTML = `
      <div class="password-name">${passwordName}</div>
      <div class="password-value">${passwordValue}</div>
    `;
    document.getElementById("saved-passwords").appendChild(passwordItem);

    // Reset the input fields
    document.getElementById("new-password-name").value = "";
    document.getElementById("password-display").textContent = "Your new password will appear here.";
  }

  // Generate new password when the button is clicked
  document.getElementById("generate-btn").addEventListener("click", function() {
    const newPassword = generateRandomPassword();
    document.getElementById("password-display").textContent = newPassword;
  });

  // Save password when the button is clicked
  document.getElementById("save-password-btn").addEventListener("click", savePassword);

  // Simple search functionality for the password list
  document.getElementById("search-bar").addEventListener("input", function() {
    const searchTerm = document.getElementById("search-bar").value.toLowerCase();
    const passwordItems = document.querySelectorAll(".password-item");

    passwordItems.forEach(item => {
      const passwordName = item.querySelector(".password-name").textContent.toLowerCase();
      if (passwordName.includes(searchTerm)) {
        item.style.display = "block";
      } else {
        item.style.display = "none";
      }
    });
  });