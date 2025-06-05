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

## 🧪 API Endpoints (Overview)

| Method | Endpoint                                | Description                                   |
|--------|-----------------------------------------|-----------------------------------------------|
| GET    | `/api/tasks/`                           | List all tasks                                |
| POST   | `/api/tasks/`                           | Create a new task                             |
| GET    | `/api/tasks/review/`                    | List tasks with status "review"               |
| GET    | `/api/tasks/high-prio/`                 | List high priority tasks                      |
| GET    | `/api/tasks/assigned/`                  | Tasks assigned to the logged-in user          |
| GET    | `/api/tasks/<task_id>/comments/`        | List comments for a specific task             |
| POST   | `/api/tasks/<task_id>/comments/`        | Create a comment on a specific task           |

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
