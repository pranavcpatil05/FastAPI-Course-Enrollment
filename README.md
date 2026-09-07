# 🎓 Course Enrollment System

A full-stack **Course Enrollment Management System** built with **FastAPI, SQLAlchemy, PostgreSQL, Pydantic V2, and Streamlit**.

The application provides a RESTful API and interactive web dashboard for managing students, courses, and enrollments. It implements relational database integrity, automatic course capacity management, duplicate enrollment prevention, and request/response validation.

---

## ✨ Key Features

* RESTful API built with **FastAPI**
* PostgreSQL database with **SQLAlchemy ORM**
* Request validation and response serialization using **Pydantic V2**
* Interactive API documentation with **Swagger UI** and **ReDoc**
* Streamlit-based web dashboard
* Automatic course seat allocation and restoration
* Duplicate enrollment prevention
* Unique student email validation
* Relational data integrity between students, courses, and enrollments
* Environment-based database configuration
* Database reset utility for development

---

## 🛠️ Tech Stack

| Technology        | Purpose                                         |
| ----------------- | ----------------------------------------------- |
| **Python 3.10+**  | Core programming language                       |
| **FastAPI**       | Backend REST API framework                      |
| **SQLAlchemy**    | ORM and database interaction                    |
| **PostgreSQL**    | Relational database                             |
| **Pydantic V2**   | Data validation and serialization               |
| **Streamlit**     | Interactive frontend dashboard                  |
| **Requests**      | HTTP communication between frontend and backend |
| **Python-Dotenv** | Environment variable management                 |
| **Uvicorn**       | ASGI server                                     |

---

## 🏗️ System Architecture

```text
┌────────────────────────────┐
│     Streamlit Frontend     │
│      Web Dashboard UI      │
└─────────────┬──────────────┘
              │ HTTP Requests
              ▼
┌────────────────────────────┐
│          FastAPI           │
│       REST API Layer       │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│        SQLAlchemy          │
│          ORM Layer         │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│        PostgreSQL          │
│       Relational DB        │
└────────────────────────────┘
```

---

## 📁 Project Structure

```text
FastAPI-Course-Enrollment/
│
├── app/
│   ├── models/                     # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── course.py
│   │   ├── enrollment.py
│   │   └── student.py
│   │
│   ├── routers/                    # FastAPI route handlers
│   │   ├── __init__.py
│   │   ├── course.py
│   │   ├── enrollment.py
│   │   └── student.py
│   │
│   ├── schemas/                    # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── course.py
│   │   ├── enrollment.py
│   │   └── student.py
│   │
│   ├── __init__.py
│   └── database.py                 # Database engine, session and Base
│
├── frontend/
│   └── app_ui.py                   # Streamlit dashboard
│
├── .env.example                    # Environment variable template
├── .gitignore                      # Git ignored files
├── main.py                         # FastAPI application entry point
├── requirements.txt                # Python dependencies
└── reset_db.py                     # Database reset utility
```

> **Note:** The actual `.env` file should not be committed to GitHub because it contains database credentials.

---

## 🗄️ Database Design

The system uses three primary entities:

### Student

Stores student information such as:

* Student ID
* Name
* Email

### Course

Stores course information such as:

* Course ID
* Course name
* Course capacity
* Available seats

### Enrollment

Connects students with courses and stores enrollment information.

The relationship can be represented as:

```text
Student
   │
   │ 1
   │
   │
   │ N
Enrollment
   │
   │ N
   │
   │ 1
Course
```

### Data Integrity

* A student's email must be unique.
* A student cannot enroll in the same course more than once.
* A course cannot accept enrollments when no seats are available.
* Available seats are automatically updated when enrollment status changes.

---

## 📌 API Endpoints

The application provides **16 REST API endpoints**.

### 👤 Student Endpoints

| Method   | Endpoint                 | Description                      |
| -------- | ------------------------ | -------------------------------- |
| `GET`    | `/students/`             | Retrieve all registered students |
| `GET`    | `/students/{student_id}` | Retrieve a student by ID         |
| `POST`   | `/students/`             | Register a new student           |
| `PUT`    | `/students/{student_id}` | Update an existing student       |
| `DELETE` | `/students/{student_id}` | Delete a student                 |

### 📚 Course Endpoints

| Method   | Endpoint               | Description                           |
| -------- | ---------------------- | ------------------------------------- |
| `GET`    | `/courses/`            | Retrieve all courses                  |
| `GET`    | `/courses/available`   | Retrieve courses with available seats |
| `GET`    | `/courses/{course_id}` | Retrieve a course by ID               |
| `POST`   | `/courses/`            | Create a new course                   |
| `PUT`    | `/courses/{course_id}` | Update course information             |
| `DELETE` | `/courses/{course_id}` | Delete a course                       |

### 📝 Enrollment Endpoints

| Method   | Endpoint                           | Description                        |
| -------- | ---------------------------------- | ---------------------------------- |
| `GET`    | `/enrollment/`                     | Retrieve all active enrollments    |
| `GET`    | `/enrollment/{enrollment_id}`      | Retrieve an enrollment by ID       |
| `GET`    | `/enrollment/student/{student_id}` | Retrieve enrollments for a student |
| `POST`   | `/enrollment/`                     | Enroll a student in a course       |
| `DELETE` | `/enrollment/{enrollment_id}`      | Cancel an enrollment               |

---

## ⚙️ Core Business Logic

### Automatic Seat Allocation

When a student successfully enrolls in a course:

```text
seats_available = seats_available - 1
```

If no seats are available, the enrollment request is rejected.

### Automatic Seat Restoration

When an enrollment is cancelled:

```text
seats_available = seats_available + 1
```

This ensures that course capacity remains synchronized with active enrollments.

### Duplicate Enrollment Prevention

The system prevents a student from enrolling in the same course more than once.

### Student Validation

Student registration validates email uniqueness and applies the configured name formatting logic before storing the record.

### Pydantic Serialization

Pydantic V2 schemas are used to validate incoming data and serialize database records into API responses.

---

## 🚀 Getting Started

### 1. Prerequisites

Make sure the following are installed:

* Python 3.10 or later
* PostgreSQL
* Git

---

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/FastAPI-Course-Enrollment.git
cd FastAPI-Course-Enrollment
```

---

### 3. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/Course_Enrollment_DB
```

Replace `your_password` with your PostgreSQL password.

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

### 6. Create the PostgreSQL Database

Create a PostgreSQL database named:

```text
Course_Enrollment_DB
```

The application will use the database URL configured in `.env`.

---

### 7. Initialize the Database

To reset the existing database tables and recreate the schemas:

```bash
python reset_db.py
```

> **Warning:** The reset script may remove existing database tables/data. Use it only when resetting the development database.

---

## ▶️ Running the Application

The application requires two processes:

### Step 1 — Start FastAPI

From the project root:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Step 2 — Start Streamlit

Open a second terminal, activate the virtual environment, and run:

```bash
streamlit run frontend/app_ui.py
```

The Streamlit dashboard will be available at:

```text
http://localhost:8501
```

---

## 📚 API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

Swagger UI can be used to test API endpoints directly from the browser.

---

## 🔄 Enrollment Workflow

The enrollment process follows this flow:

```text
Student submits enrollment request
            │
            ▼
Check student exists
            │
            ▼
Check course exists
            │
            ▼
Check duplicate enrollment
            │
            ▼
Check available seats
            │
       ┌────┴────┐
       │         │
      No        Yes
       │         │
       ▼         ▼
   Reject      Create
   Request    Enrollment
                 │
                 ▼
       Decrease Available Seats
```

When an enrollment is cancelled:

```text
Cancel Enrollment
        │
        ▼
Delete Enrollment Record
        │
        ▼
Restore Available Seat
        │
        ▼
Course Capacity Updated
```

---

## 🔐 Error Handling

The API uses appropriate HTTP status codes for common failure scenarios, including:

* `400 Bad Request` — Invalid business operation such as enrolling when no seats are available
* `404 Not Found` — Requested student, course, or enrollment does not exist
* `409 Conflict` — Duplicate records where applicable
* `422 Unprocessable Entity` — Invalid request data handled through Pydantic validation

---

## 🎯 Project Objectives

This project demonstrates practical implementation of:

* REST API development
* Backend application architecture
* Relational database design
* ORM-based database operations
* Data validation
* CRUD operations
* Business rule implementation
* Database relationships
* API documentation
* Frontend-backend integration
* Environment configuration

---
## 📄 License

This project is intended for educational and portfolio purposes.
