````markdown
# RateMySetup 🖥️

![CI Status](https://github.com/Kenanhi/RateMySetup/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

**RateMySetup** is a containerized Django web application that allows developers to publish, share, and review development setups. This project has been modernized to include a fully functional REST API, Docker orchestration, and a CI/CD pipeline.

## 🚀 Features

* **User Authentication:** Custom user model with secure email-based login and JWT-ready structure.
* **Setup Sharing:** Users can publish their setups with detailed descriptions and image uploads.
* **Review System:** Community-driven rating system (1-5 stars) with comments.
* **REST API:** Fully browseable API built with Django Rest Framework (DRF).
* **Admin Panel:** Manage users, setups, and reviews via the Django Admin interface.
* **CI/CD Pipeline:** Automated testing and build verification via GitHub Actions.
* **Containerized:** "Infrastructure as Code" using Docker and Docker Compose with PostgreSQL.

## 🛠️ Tech Stack

* **Backend:** Python 3.11, Django 4.2, Django Rest Framework
* **Database:** PostgreSQL 15 (Dockerized)
* **Containerization:** Docker, Docker Compose
* **Testing:** Pytest, Pytest-Django
* **Deployment:** Gunicorn (WSGI)

## 📂 Project Structure

```text
RateMySetup/
├── .github/workflows/         # CI/CD Pipeline (GitHub Actions)
├── RateMySetup/               # Project settings and configuration
├── myapp/                     # Main application (Models, Views, Serializers)
│   ├── migrations/            # Database schema versions
│   ├── tests.py               # Automated tests
│   └── ...
├── setups/                    # Directory for user-uploaded images
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Container orchestration (Web + DB)
├── manage.py                  # Django management script
├── pytest.ini                 # Test configuration
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
````

## ⚙️ Getting Started

You can run this project locally using Docker (Recommended) or standard Python virtual environments.

### Prerequisites

  * **Docker Desktop** (Installed and running)
  * **Git**

### 🐳 Installation (Docker Method)

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/Kenanhi/RateMySetup.git](https://github.com/Kenanhi/RateMySetup.git)
    cd RateMySetup
    ```

2.  **Build and Start the Stack:**
    This command builds the container and starts both the Web Server and PostgreSQL Database.

    ```bash
    docker compose up -d --build --wait
    ```

3.  **Apply Database Migrations:**
    Initialize the PostgreSQL database schema.

    ```bash
    docker compose exec web python manage.py migrate
    ```

4.  **Create an Admin User:**
    Create a superuser to access the admin panel.

    ```bash
    docker compose exec web python manage.py createsuperuser
    ```

5.  **Access the Application:**

      * **API Root:** [http://localhost:8000/api/](https://www.google.com/search?q=http://localhost:8000/api/)
      * **Admin Panel:** [http://localhost:8000/admin/](https://www.google.com/search?q=http://localhost:8000/admin/)

-----

## 🧪 Automated Testing

This project uses `pytest` for unit and integration testing. The tests cover user registration, setup creation, and API endpoint validity.

**To run tests locally:**

```bash
docker compose exec web pytest -v
```

**To view tests in CI/CD:**
Navigate to the **Actions** tab in this GitHub repository to see the automated test results for every commit.

-----

## 📡 API Documentation

The API allows full CRUD operations. You can interact with it via the Browsable API interface at `/api/`.

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/users/` | `POST` | Register a new user (Open registration) |
| `/api/users/` | `GET` | List users (Admin/Authenticated) |
| `/api/setups/` | `GET` | View all shared setups |
| `/api/setups/` | `POST` | Create a new setup (Requires Login) |
| `/api/reviews/` | `POST` | Rate a setup (Requires Login) |

```
```