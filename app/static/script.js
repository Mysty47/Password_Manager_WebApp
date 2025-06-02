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

async function savePassword() {
   const passwordName = document.getElementById("new-password-name").value.trim();
   const passwordInput = document.getElementById("new-password-input").value.trim();
   const passwordDisplay = document.getElementById("password-display").textContent;

   if (passwordName.length > 16) {
       alert("Password name should not exceed 16 characters.");
       return;
   }
   if (passwordInput.length > 16) {
       alert("Password should not exceed 16 characters.");
       return;
   }

   let passwordToSave = passwordInput || (passwordDisplay !== "Your new password will appear here." ? passwordDisplay : "");

   if (!passwordName || !passwordToSave) {
       alert("Please enter a password name and either type a password or generate one.");
       return;
   }

   // Send the password to FastAPI
   try {
       const response = await fetch("http://localhost:8000/save_password/", {
           method: "POST",
           headers: {
               "Content-Type": "application/json"
           },
           body: JSON.stringify({
               name: passwordName,
               password: passwordToSave
           })
       });

       const result = await response.json();
       if (result.status === "success") {
           loadPasswords(); // Refresh password list
       } else {
           const errorData = await response.json();
           if (response.status === 401) {
               errorMessage = "Error saving password: not logged in";
           } else if (errorData.detail) {
               alert("Error saving password: " + errorData.detail);
           } else {
               alert("Error saving password: " + result.message);
           }
       }
   } catch (error) {
       console.error("Error saving password:", error);
       alert("Failed to save password.");
   }

   document.getElementById("new-password-name").value = "";
   document.getElementById("new-password-input").value = "";
   document.getElementById("password-display").textContent = "Your new password will appear here.";
}

// Attach event listener to save button
document.getElementById("save-password-btn").addEventListener("click", savePassword);


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

function buttonDisappear() {
  document.getElementById("login-btn").style.display = "none";
}

document.addEventListener("DOMContentLoaded", function () {
  // Select the login link and the user-info div
  const loginLink = document.getElementById("login-link");
  const userInfoDiv = document.querySelector(".user-info");

  // We still need these for setting username and adding logout listener, but not for initial visibility
  const usernameDisplay = document.getElementById("username-display");
  const logoutBtn = document.getElementById("logout-btn");

  const loggedIn = localStorage.getItem("loggedIn") === "true";
  const username = localStorage.getItem("username");

  console.log("DOMContentLoaded fired. Logged in:", loggedIn, "Username:", username); // Log for debugging
  console.log("Elements found:", { loginLink, userInfoDiv, usernameDisplay, logoutBtn }); // Log elements found

  if (loggedIn) {
      // If logged in, hide the login link and show the user info div
      if (loginLink) loginLink.style.display = "none";
      if (userInfoDiv) userInfoDiv.style.display = "flex"; // Or 'block', depending on your layout needs

      // Set username if the element is found
      if (usernameDisplay) {
          usernameDisplay.textContent = `👤 ${username}`;
      }

  } else {
      // If not logged in, show the login link and hide the user info div
      if (loginLink) loginLink.style.display = "block"; // Or 'inline'/'flex' depending on original display type
      if (userInfoDiv) userInfoDiv.style.display = "none";
  }

  // Add logout functionality if the logout button is found
  if (logoutBtn) {
    logoutBtn.addEventListener("click", async function () {
        // Optional: Call a backend logout endpoint if needed for server-side cleanup
        // try {
        //     await fetch('http://localhost:8000/logout', { method: 'POST' });
        // } catch (error) {
        //     console.error('Logout error:', error);
        // }
        
        localStorage.removeItem("loggedIn");
        localStorage.removeItem("username"); // Remove username from storage
        window.location.href = '/'; // Redirect to home page
    });
  }
});

// Function to fetch saved passwords and display them
async function loadPasswords() {
  try {
      const response = await fetch("http://localhost:8000/saved_passwords");
      const data = await response.json();

      console.log("Data received for passwords:", data); // Log the entire data object

      const passwordContainer = document.getElementById("saved-passwords");
      passwordContainer.innerHTML = ""; // Clear existing content

      if (!data.passwords || data.passwords.length === 0) {
          passwordContainer.innerHTML = "<p>No saved passwords found.</p>";
          console.log("No passwords found or data structure unexpected.", data); // Log if no passwords
          return;
      }

      console.log("Passwords array:", data.passwords); // Log the passwords array

      data.passwords.forEach(password => {
          console.log("Processing password item:", password); // Log each password item
          console.log("Keys available on password item:", Object.keys(password)); // Log the keys
          const passwordItem = document.createElement("div");
          passwordItem.classList.add("password-item");
          passwordItem.innerHTML = `
              <div class="password-name"><strong>${password.name}</strong></div>
              <div class="password-value">${password.password}</div>
          `;
          passwordContainer.appendChild(passwordItem);
      });

  } catch (error) {
      console.error("Error fetching saved passwords:", error);
      document.getElementById("saved-passwords").innerHTML = "<p>Error loading passwords.</p>";
  }
}

// Run the function when the page loads
document.addEventListener("DOMContentLoaded", loadPasswords);

// Dropdown menu functionality
document.addEventListener('DOMContentLoaded', function() {
    const dropdownBtn = document.querySelector('.dropdown-btn');
    const dropdownContent = document.querySelector('.dropdown-content');
    const menuLinks = document.querySelectorAll('.dropdown-content a');

    // Toggle dropdown menu on click
    dropdownBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        dropdownContent.classList.toggle('show');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!dropdownContent.contains(e.target) && !dropdownBtn.contains(e.target)) {
            dropdownContent.classList.remove('show');
        }
    });

    // Prevent dropdown from closing when clicking inside it
    dropdownContent.addEventListener('click', function(e) {
        e.stopPropagation();
    });

    // Menu button functionality
    menuLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const action = this.textContent.toLowerCase();
            
            switch(action) {
                case 'home':
                    window.location.href = '/';
                    break;
                case 'features':
                    // Scroll to features section or navigate to features page
                    const featuresSection = document.querySelector('#features');
                    if (featuresSection) {
                        featuresSection.scrollIntoView({ behavior: 'smooth' });
                    }
                    break;
                case 'pricing':
                    // Scroll to pricing section or navigate to pricing page
                    const pricingSection = document.querySelector('#pricing');
                    if (pricingSection) {
                        pricingSection.scrollIntoView({ behavior: 'smooth' });
                    }
                    break;
                case 'about':
                    // Scroll to about section or navigate to about page
                    const aboutSection = document.querySelector('#about');
                    if (aboutSection) {
                        aboutSection.scrollIntoView({ behavior: 'smooth' });
                    }
                    break;
            }
            
            // Close dropdown after clicking a menu item
            dropdownContent.classList.remove('show');
        });
    });
});

// Simulate login (Replace this with actual authentication logic)
document.querySelector("#login-form button[type='submit']")?.addEventListener("click", async function (event) {
    event.preventDefault(); // Prevent actual form submission

    const usernameInput = document.querySelector('#login-form input[type="text"]');
    const passwordInput = document.querySelector('#login-form input[type="password"]');
    const username = usernameInput.value;
    const password = passwordInput.value;

    try {
        const response = await fetch('http://localhost:8000/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username: username,
                password: password,
            }),
        });

        const result = await response.json();

        if (result.status === 'success') {
            localStorage.setItem("loggedIn", "true");
            localStorage.setItem("username", result.username); // Store the username
            window.location.href = '/'; // Redirect to home page
        } else {
            alert("Login failed: " + result.message);
        }
    } catch (error) {
        console.error("Login error:", error);
        alert("An error occurred during login.");
    }
});
