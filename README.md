# 🔐 Password Manager WebApp

A simple and secure **Password Manager Web Application** built with **FastAPI** and **MySQL**, allowing users to generate, store, and manage passwords with labeled entries. Designed with security in mind and an intuitive RESTful API interface.

---

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
