# 🧩 Employee Management API (Flask + SQLite + Pydantic)

This project is a **RESTful API** built using **Flask**, **SQLite**, and **Pydantic** for data validation.  
It allows you to manage **Employees** and their **Projects** with full CRUD operations and JSON/XML support.

---

## 🚀 Features

- Add, update, partially update, view, and delete employees.
- Manage multiple projects per employee (Many-to-Many relationship).
- Data validation using **Pydantic**.
- SQLite database with **Foreign Key & Cascade** support.
- Supports both **JSON** and **XML** data formats.

---

## 🧱 Tech Stack

| Component | Description |
|------------|-------------|
| **Flask** | Backend framework for API development |
| **SQLite** | Lightweight local database |
| **Pydantic** | Data validation and type checking |
| **xmltodict** | XML parsing and conversion |
| **Postman** | API testing tool |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate    # For Windows
# OR
source venv/bin/activate # For Mac/Linux
```

### 3️⃣ Install Dependencies
```bash
pip install flask pydantic xmltodict
```

### 4️⃣ Run the Flask Server
```bash
python 9225eea5-52c9-4e6e-a722-5dd65aefae2c.py
```

Your API will run on  
👉 **http://127.0.0.1:5000**

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/employees` | Get employee by name/id/salary/email |
| `GET` | `/all` | Get all employees with their projects |
| `POST` | `/employees` | Add a new employee with project details |
| `PUT` | `/employees/<id>` | Update an employee completely |
| `PATCH` | `/employees/<id>` | Partially update an employee |
| `DELETE` | `/employees/<id>` | Delete an employee |

---

## 🧾 Example Request (POST)
```json
{
  "emp_id": 1,
  "emp_name": "Amit Sawant",
  "salary": 60000,
  "email": "amit@example.com",
  "project": [
    {
      "project_id": 101,
      "project_name": "Data Analytics Dashboard",
      "status": "Ongoing"
    }
  ]
}
```

---

## 🧩 Database Schema

**employees**
| emp_id | emp_name | salary | email |
|--------|-----------|--------|-------|

**project**
| project_id | project_name |
|-------------|---------------|

**employees_project**
| emp_id | project_id | status |

---

## 💾 Notes

- Cascading delete and update are enabled.
- Validation errors are handled via Pydantic models.
- Works with both JSON and XML payloads.

---

## 👨‍💻 Author

**Amit Sawant**  
📧 Email: [amitsawant3892@gmail.com]  
💼 GitHub: [https://github.com/amitsawant3892](https://github.com/amitsawant3892)

---



