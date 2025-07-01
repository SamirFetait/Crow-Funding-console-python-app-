# 🧩 Crowd-Funding Console App (Python)

A simple console-based crowd-funding platform built in Python. Users can register, log in, and create, view, edit, and delete their own fundraising projects. All data is persisted using JSON files.

---

## 🚀 Features

### 🔐 Authentication System
- **Register** with username, email, password, and phone number
- **Login** with email and password
- **Account activation** required before logging in
- Validations for all fields (name, email, password, phone)

### 📁 Project Management
- **Create a project** with:
  - Title (alpha only)
  - Description (min 10 characters)
  - Target amount (EGP)
  - Start and end dates (valid and logical ranges)
- **View all projects** listed with details and owner
- **Edit** only your own projects
- **Delete** only your own projects

---

## 📂 Data Storage

Data is stored locally in JSON files:

- `users.json`: Stores user information (credentials, activation state)
- `projects.json`: Stores all project records with IDs and owner references

---

## 🧰 Requirements

- Python 3.6+
- No external libraries required

---

## 💻 How to Run

1. Clone or download the repo
2. Run the script:
```bash
python crowd-funding.py
