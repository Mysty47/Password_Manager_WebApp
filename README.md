# 🔐 Password Manager WebApp

## 🎯 1.1Project Purpose
This project is a web-based password manager designed to help users securely store and manage their passwords for various online services. It aims to provide a simple and safe way for individuals to handle sensitive credentials without relying on external tools.

## ⚙️ 1.2Core Functionalities
User registration and login with basic validation

Secure password storage using encryption

Add new entries (service name, username, password)

View and search saved passwords

Delete existing password entries

Clean, user-friendly interface

## 👥 1.3Target Users
This app is designed for individuals who:

Have accounts on multiple platforms

Want a centralized and secure password manager

Prefer to use a simple, lightweight, self-hosted solution

## 📚 1.4Use Cases

Add password: The user adds a new password with service name, username, and encrypted password.

View passwords: The user logs in and sees a list of all stored credentials.

Generate secure passwords: You can generate random secure password, with the help of 1 button.

Register/Login: New users create an account; existing users sign in to access their data.

##🏗️ Project Architecture and Technology Choices

## 🔧 2.1 – Technology Justification
This project uses Flask as the web framework due to its simplicity and suitability for small-to-medium web applications. SQLite is used as the database engine because it is lightweight and easy to integrate, especially for local or prototype apps. The frontend uses standard HTML/CSS, which allows for clear structure and user-friendly design.

## 🧱 2.2 – Architecture Model
The application follows a Model-View-Controller (MVC)-like architecture:

Model: The database (SQLite) and logic for managing stored passwords.

View: HTML templates in the /templates folder for rendering the UI.

Controller: Application logic and routes defined in app.py.

This structure keeps the codebase clean and modular, making it easier to maintain and expand.

## 🗂️ 2.3 – Module Separation and Dependencies
The project is organized as follows:

All application routes and business logic are in app.py.

HTML files are inside the templates/ folder.

Static assets like CSS are placed in the static/ directory.

Password entries are stored securely in database.db.

This modular layout separates concerns and simplifies debugging and enhancements.

## 🔄 2.4 – Maintainability and Expandability
Thanks to Flask’s modular design and the separation of logic and templates, the app can be easily extended. For example, adding new features like password generation, exporting to CSV, or two-factor authentication would only require minimal additions to the existing routes and templates without needing to restructure the core.



## 🚀 Features

✅ User registration and login
✅ Random password generation
✅ Save personal passwords with custom labels
✅ Store all data in a local **MySQL** database
✅ RESTful API interface (with Swagger documentation)
✅ **Dockerized** deployment with `docker-compose`

---

## 📁 Project Structure

```
Password_Manager_WebApp/
├── static/              # Frontend static files (CSS, JS)
├── templates/           # HTML templates
├── main.py              # FastAPI backend logic
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Docker orchestration
├── Dockerfile           # Backend container configuration
└── README.md            # Project documentation
```

---

## 🧪 Local Development Setup

### 1. Clone the Repository

```
git clone https://github.com/Mysty47/Password_Manager_WebApp.git
cd Password_Manager_WebApp
```

### 2. Start the Application with Docker

```
docker-compose up
```

* Access the app at: [http://localhost:8000](http://localhost:8000)
* Swagger UI for API testing: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Shut Down the Application

Press `Ctrl + C`, then run:

```
docker-compose down
```

### 4. Access the MySQL Database

```
docker-compose exec db mysql -u root -p
```

---

## 🔧 MySQL Database Setup (Schema Overview)

The application uses two main tables:

* `users` – Stores user credentials (with password hashing – planned)
* `passwords` – Stores labeled passwords per user

Refer to `main.py` for schema creation scripts if not using Docker.

---

## 📱 API Endpoints

| Method | Endpoint     | Description                   |
| ------ | ------------ | ----------------------------- |
| POST   | `/signup`    | Register a new user           |
| POST   | `/login`     | Authenticate user credentials |
| POST   | `/generate`  | Generate a random password    |
| POST   | `/save`      | Save a labeled password       |
| GET    | `/passwords` | Retrieve all saved passwords  |

Interactive API documentation is available at:
➡️ **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 🔐 Planned Security Improvements

* 🔐 Hashing passwords with **bcrypt**
* ✅ Input validation and error handling
* 📆 Using **environment variables** for sensitive config
* 🛡️ Protection against SQL Injection and other attacks
* 🔐 Password encryption before DB storage

---

## 🛠️ Future Enhancements

* JWT-based authentication and user sessions
* Mobile-responsive frontend design
* Unit tests and CI/CD integration
* Docker networking and volume improvements

---

## 👨‍💼 Author

Built with ❤️ by **[Mysty47](https://github.com/Mysty47)**

---

## 📄 License

This project is licensed under the **MIT License** – feel free to use and contribute!
