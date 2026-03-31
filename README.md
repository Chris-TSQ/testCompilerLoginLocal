# 🚀 Full-Stack Auth System + Auto Test Generator

A lightweight full-stack authentication system with a built-in **automatic test generation plugin**.  
This project demonstrates backend API design, frontend integration, and developer tooling for generating tests.

---

## 📌 Features

### 🔐 Authentication System
- User signup & login
- Secure password hashing (SHA-256)
- Token-based session management
- Session expiration (24 hours)
- Logout & token invalidation

### 🌐 Frontend
- Simple UI for:
  - Signup
  - Login
  - Dashboard
- LocalStorage-based session handling
- Error handling & validation

### ⚙️ Backend API (Flask)
- RESTful API with:
  - `/api/signup`
  - `/api/login`
  - `/api/logout`
  - `/api/verify`
- SQLite database
- CORS enabled

### 🧪 Test Generator Plugin
- Automatically generates:
  - **PyTest** tests for Python backend
  - **Cypress** tests for frontend
- Pluggable architecture
- File-type-based test generation

---

## 🏗️ Project Structure


project/
│
├── backend/
│ ├── app.py
│ ├── database.py
│ └── tests/
│ └── test_app.py
│
├── frontend/
│ ├── api.js
│ ├── app.js
│ └── cypress/
│ └── e2e/
│
├── generators/
│ ├── TestGenerator.js
│ ├── PyTestGenerator.js
│ └── CypressTestGenerator.js
│
├── CompilerTestGenPlugin.js
└── README.md


---

## 🧰 Tech Stack

**Backend**
- Python
- Flask
- SQLite

**Frontend**
- Vanilla JavaScript
- HTML/CSS

**Testing**
- PyTest
- Cypress

**Tooling**
- Node.js (Test Generator Plugin)

---

## ⚡ Getting Started

### 1️⃣ Backend Setup

```bash
cd backend
pip install flask flask-cors pytest
python app.py
```
Server runs at:

http://localhost:5000
2️⃣ Frontend Setup

Open your HTML file (or serve it):

cd frontend

# Option 1: open index.html manually

# Option 2: serve locally
npx serve .
3️⃣ Run Tests
✅ PyTest (Backend)
pytest
✅ Cypress (Frontend)
npx cypress open
🔌 API Endpoints
➕ Signup
POST /api/signup
```
{
  "username": "test",
  "email": "test@test.com",
  "password": "123"
}
```
🔑 Login
POST /api/login

Response:
```
{
  "message": "Login successful",
  "token": "TOKEN",
  "username": "test"
}
```
🚪 Logout
POST /api/logout
Authorization: Bearer <token>
✅ Verify Session
GET /api/verify
Authorization: Bearer <token>
🧪 Test Generator Plugin

Automatically generates tests based on file type.

Usage
```
const CompilerTestGenPlugin = require('./CompilerTestGenPlugin');

const plugin = new CompilerTestGenPlugin({
  outputDir: 'generated-tests'
});

plugin.run('backend/app.py');   // Generates PyTest tests
plugin.run('frontend/app.js');  // Generates Cypress tests
```
🔍 How It Works
File Type	Generator Used
.py	PyTestGenerator
.js / .html	CypressTestGenerator
🔐 Security Notes
Passwords are hashed using SHA-256 (consider bcrypt for production)
Tokens are generated using secrets.token_urlsafe
Sessions expire after 24 hours
🚧 Future Improvements
Use JWT instead of custom tokens
Add refresh tokens
Improve frontend UI/UX
Add role-based access control
Docker support
CI/CD integration
📄 License

MIT License
