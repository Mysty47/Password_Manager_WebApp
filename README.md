# Password Manager WebApp

A simple password manager web application that allows users to securely generate, store, and manage their passwords. The application includes user authentication (login/signup), password labeling, and persistent storage via a local MySQL database.

---

## 🚀 Features

* ✅ User registration and login
* ✅ Random password generation
* ✅ Save personal passwords with labels
* ✅ Store all data in a local MySQL database
* ✅ RESTful API interface between frontend and backend
* ✅ Docker support (to be added)

---

## 📁 Project Structure

```
Password_Manager_WebApp/
├── static/              # CSS and JavaScript files
├── templates/           # HTML pages
├── main.py              # Backend server and logic
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🧪 Setup Instructions (Local)

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/Password_Manager_WebApp.git
   cd Password_Manager_WebApp
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare the MySQL database**

   * Create a local MySQL database
   * Set up the required `users` and `passwords` tables (refer to `main.py`)

4. **Run the application**

   ```bash
   uvicorn main:app --reload
   ```

5. **Access the app**

   ```
   http://127.0.0.1:8000
   ```

---

## 🐳 Docker (Coming Soon)

The project will include:

* `Dockerfile` for containerizing the FastAPI backend
* `docker-compose.yml` to orchestrate MySQL and the backend API

---

## 🔐 Security & Best Practices (Planned/Partially Implemented)

* Secure storage of user credentials (password hashing – upcoming)
* Input validation and error handling
* Environment variables for configuration
* Protection against common attacks (e.g., SQL Injection – planned)

---

## 📡 API Design

The backend follows a RESTful API architecture. The following endpoints are implemented or planned:

| Method | Endpoint     | Description                   |
| ------ | ------------ | ----------------------------- |
| POST   | `/signup`    | Register a new user           |
| POST   | `/login`     | Authenticate user credentials |
| POST   | `/generate`  | Generate a random password    |
| POST   | `/save`      | Save a custom password        |
| GET    | `/passwords` | Retrieve all saved passwords  |

> **Swagger UI** is available at [`/docs`](http://127.0.0.1:8000/docs) for interactive API testing.

---

## 📌 Future Improvements

* Add password encryption before saving in the database
* Add user sessions / JWT authentication
* Responsive frontend for mobile use
* Full Docker support
* Unit testing and CI integration

---

## 👨‍💻 Author

Built with ❤️ by \Mysty47

---

## 📄 License

This project is open-source and available under the MIT License.
