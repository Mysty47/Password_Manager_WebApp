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
           alert("Error saving password: " + result.message);
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
  const loginBtn = document.querySelector(".login-btn");

  // Check if user is logged in and hide login button
  if (localStorage.getItem("loggedIn") === "true") {
      if (loginBtn) loginBtn.style.display = "none";
  }

  // Simulate login (Replace this with actual authentication logic)
  document.getElementById("login-form")?.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent actual form submission
      localStorage.setItem("loggedIn", "true");
      if (loginBtn) loginBtn.style.display = "none";
  });

  // Logout functionality (Optional)
  document.getElementById("logout-btn")?.addEventListener("click", function () {
      localStorage.removeItem("loggedIn");
      location.reload(); // Refresh to show login button again
  });
});

async function fetchPasswords() {
  try {
      const response = await fetch("http://localhost:8000/saved_passwords"); // Adjust the URL if needed
      const data = await response.json();

      if (data.passwords) {
          displayPasswords(data.passwords);
      } else {
          console.error("Error fetching passwords:", data.message);
      }
  } catch (error) {
      console.error("Fetch error:", error);
  }
}

// Function to display passwords in the UI
function displayPasswords(passwords) {
  const container = document.getElementById("saved-passwords");
  container.innerHTML = ""; // Clear previous entries

  passwords.forEach(item => {
      const passwordItem = document.createElement("div");
      passwordItem.classList.add("password-item");
      passwordItem.innerHTML = `
          <div><strong>${item.place}</strong>: ${item.password}</div>
      `;
      container.appendChild(passwordItem);
  });
}

// Call the function when the page loads
document.addEventListener("DOMContentLoaded", fetchPasswords);

// Function to fetch saved passwords and display them
async function loadPasswords() {
  try {
      const response = await fetch("http://localhost:8000/saved_passwords");
      const data = await response.json();

      const passwordContainer = document.getElementById("saved-passwords");
      passwordContainer.innerHTML = ""; // Clear existing content

      if (data.passwords.length === 0) {
          passwordContainer.innerHTML = "<p>No saved passwords found.</p>";
          return;
      }

      data.passwords.forEach(password => {
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
