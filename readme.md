# 🏠 SmartHome Core

A **production-grade IoT backend** built with **Flask**, designed to simulate and manage smart home devices, users, and real-time device interactions.

This project demonstrates **clean backend architecture**, security best practices, real-time communication, and deployment readiness.

---

## 🚀 Features

### 🔧 Device Management

* Create, read, update, delete smart home devices
* Device fields:

  * `id`
  * `name`
  * `type` (light, sensor, lock, etc.)
  * `location`
  * `state`
  * `last_updated`

### ⚡ Real-Time Updates

* WebSocket support using **Flask-SocketIO**
* Instant device state updates
* Event-driven architecture

### 👤 Authentication & Authorization

* JWT-based authentication
* Role-Based Access Control (RBAC)

  * **Admin**: manage devices
  * **User**: view devices, send commands

### 🧠 Command Handling

* Send commands to devices
* Simulated device behavior
* Command execution tracking

### 🛡️ Security

* JWT authentication
* Role-based route protection
* Rate limiting (anti-abuse)
* Input validation

### 📊 Observability

* Application logging
* Immutable audit trails

### 📘 API Documentation

* Swagger / OpenAPI UI
* JWT-enabled interactive testing

### ☁️ Deployment Ready

This project is deployed using **Render** with **MongoDB Atlas** as the managed database.

* No Docker required
* Environment variables managed via Render dashboard
* Cloud-hosted MongoDB (Atlas)

---

## 🏗️ Architecture Overview

```text
Client (Web / Mobile / IoT)
        ↓
REST API + WebSockets
        ↓
Routes (HTTP handling)
        ↓
Services (Business logic)
        ↓
Models (Data shape)
        ↓
MongoDB
```

---

## 📁 Project Structure

```text
SmartHome-Core/
│
├── app/
│   ├── __init__.py          # App factory & extensions
│   ├── run.py               # Application entry point
│   │
│   ├── routes/              # HTTP & WebSocket routes
│   │   ├── devices.py
│   │   ├── auth.py
│   │   ├── commands.py
│   │   └── socket_events.py
│   │
│   ├── services/            # Business logic
│   │   ├── device_service.py
│   │   ├── command_service.py
│   │   └── user_service.py
│   │
│   ├── models/              # Data models
│   │   └── device.py
│   │
│   ├── utils/               # Shared utilities
│   │   ├── logger.py
│   │   ├── audit.py
│   │   ├── roles.py
│   │   ├── validators.py
│   │   └── rate_limit_error.py
│   │
│   ├── config.py            # Environment configuration
│   └── docs.py              # Swagger / OpenAPI setup
│
├── logs/
│   ├── app.log
│   └── audit.log
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

* Python 3.11
* Flask
* Flask-JWT-Extended
* Flask-SocketIO
* Flask-Limiter
* Flask-RESTX (Swagger)
* MongoDB


---

## ⚙️ Installation (Local)

```bash
git clone <repo-url>
cd SmartHome-Core
python3 -m venv venv
source venv/bin/activate || source venv/Scripts/activate
pip install -r requirements.txt
python3 run.py
```

---

## 🐳 Docker Deployment

```bash
docker compose up --build
```

---

## 🔐 Authentication

Use JWT tokens in requests:

```http
Authorization: Bearer <access_token>
```

---

## 📘 API Documentation

Swagger UI:

```
http://127.0.0.1:5000/docs
```

---

## 📊 Logging & Audit

* App logs: `logs/app.log`
* Audit logs: `logs/audit.log`

---

## 🚦 Rate Limiting

* Login: 5/min
* Commands: 5/min
* Updates: 5/min

Returns:

```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many requests, slow down."
}
```

---

## 📦 Deployment Targets

* Render
* Fly.io
* AWS
* DigitalOcean

---

## 👤 Author

**Heritage Adeleke**
Backend Engineer

---

## 📄 License

Educational & demonstration use.
