# 🧠 Kanmind – Backend API

This is the backend of the **Kanmind** app – a task and comment management system with user authentication and role-based logic, built using **Django** and **Django REST Framework**.

---

## 🔧 Features

- 🔐 Authentication via DRF (login required for POST/PUT/DELETE)
- ✅ Task management with status & priority
- 💬 Comments on tasks
- 📌 Custom views for:
  - Assigned tasks (`worked`)
  - Tasks in review mode
  - High priority tasks
- 👮‍♂️ User permissions (e.g., `IsOwnerOrReadOnly`)

---

## 📁 Project Structure

```
kanmind/
├── tasks_app/
│   ├── models.py          # Tasks and Comments
│   ├── api/
│   │   ├── views.py       # ViewSets including filter logic
│   │   ├── serializers.py # Model serialization
│   │   ├── permissions.py # Custom permissions
│   └── ...
├── manage.py
└── ...
```

---

## 🚀 Setup & Installation

```bash
git clone https://github.com/your-username/kanmind-backend.git
cd kanmind-backend

python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 🔑 Authentication

Login is required for POST, PUT, or DELETE requests. Authentication is handled via Django Sessions or Tokens (depending on setup).

---

## 🧪 API Endpoints Overview

### General

| Method | Endpoint           | Description                       |
|--------|--------------------|---------------------------------|
| POST   | /api/registration/ | User registration               |
| POST   | /api/login/        | User login                      |

### Boards

Everything related to creating, editing, and retrieving boards.

| Method | Endpoint                 | Description                      |
|--------|--------------------------|---------------------------------|
| GET    | /api/boards/             | List all boards                 |
| POST   | /api/boards/             | Create a new board              |
| GET    | /api/boards/{board_id}/  | Retrieve details of a board    |
| PATCH  | /api/boards/{board_id}/  | Update a board                 |
| DELETE | /api/boards/{board_id}/  | Delete a board                 |
| GET    | /api/email-check/        | Check email availability       |

### Tasks

Everything related to creating, editing, and retrieving tasks.

| Method | Endpoint                         | Description                            |
|--------|----------------------------------|--------------------------------------|
| GET    | /api/tasks/assigned-to-me/       | List tasks assigned to the logged-in user |
| GET    | /api/tasks/reviewing/            | List tasks currently under review    |
| POST   | /api/tasks/                     | Create a new task                    |
| PATCH  | /api/tasks/{task_id}/           | Update a task                       |
| DELETE | /api/tasks/{task_id}/           | Delete a task                       |
| GET    | /api/tasks/{task_id}/comments/ | List comments for a task             |
| POST   | /api/tasks/{task_id}/comments/ | Add a comment to a task              |
| DELETE | /api/tasks/{task_id}/comments/{comment_id}/ | Delete a specific comment         |

---

## 👤 User Permissions

- **Authenticated users**: can create their own tasks and comments
- **Unauthenticated users**: read-only access
- **Resource owners**: can update/delete their own entries
- **Admins**: full access

---

## 🧪 Postman Testing

You can test all endpoints easily using Postman. If needed, I can generate a `.json` Postman collection for you.

---

## 🧱 Technologies Used

- Django
- Django REST Framework
- SQLite (default, configurable)
- Python 3.11+

---

## 📄 License

This project is licensed under the MIT License. You are free to use, modify, and share it.

---

## ✍️ Author

**Jonas**  
Frontend & Backend Developer passionate about clean code and modern web technologies

---
