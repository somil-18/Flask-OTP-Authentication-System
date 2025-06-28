# 🔐 Flask OTP Authentication System

A simple web-based user authentication system built using **Flask**, featuring user **signup/login**, **OTP verification via email**, and **session management**. This project includes secure password hashing, email-based OTP verification using Gmail SMTP, and SQLite as the backend database.

---

## 🚀 Features

- 📨 **Send OTP via Email** (Gmail SMTP)
- 🔐 **Secure Password Hashing** with `werkzeug`
- 🧾 **User Signup & Login**
- 🧠 **Session Management**
- ✅ **OTP Verification**
- 🔁 **Resend OTP**
- 📄 Multiple Page Templates: `signup`, `login`, `rent`, `list`, `contact`, `about`, `main`

---

## 📁 Project Structure

```
├── app.py               # Main Flask application
├── templates/
│   ├── signup.html
│   ├── login.html
│   ├── main.html
│   ├── rent.html
│   ├── list.html
│   ├── contact.html
│   └── about.html
├── user.db              # SQLite database
└── requirements.txt     # Python dependencies
```




---

## ✅ API Routes

| Method | Route         | Description                    |
|--------|---------------|--------------------------------|
| GET    | `/`           | Signup Page                    |
| GET    | `/login`      | Login Page                     |
| POST   | `/signup`     | Create User (JSON)             |
| POST   | `/auth`       | Authenticate User (JSON)       |
| POST   | `/send-otp`   | Send OTP to Email (JSON)       |
| POST   | `/verify-otp` | Verify OTP Code (JSON)         |
| POST   | `/resend-otp` | Resend OTP (JSON)              |
| GET    | `/logout`     | Clear session and logout       |
| GET    | `/main`       | Main Page                      |
| GET    | `/rent`       | Rent Page (Auth required)      |
| GET    | `/list`       | List Page (Auth required)      |
| GET    | `/contact`    | Contact Info                   |
| GET    | `/about`      | About Us                       |


---

## 📦 Dependencies
👉 To install all required libraries, see [requirments.txt](requirments.txt)

Installation:

```
pip install -r requirements.txt
```

---


## ⚠️ Disclaimer

This project is for **educational purposes only**.  
Please use email functionality responsibly and **do not expose sensitive data or credentials** in production.  
The developer is not responsible for any misuse or violation of third-party service policies.






