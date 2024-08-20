# RateMySetup

**RateMySetup** is a Django-based web application where developers can share and review their development setups, including detailed information about their hardware and software configurations.

## Features

- **User Authentication:** Custom user model with email-based login.
- **Setup Sharing:** Users can publish their setups with descriptions and images.
- **Review System:** Users can review and rate setups.
- **Admin Panel:** Manage users, setups, and reviews with Django's admin interface.
```markdown
## Project Structure

RateMySetup/
├── RateMySetup/               # Project settings and main configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py            # Main settings for the Django project
│   ├── urls.py                # URL configuration
│   ├── wsgi.py
│
├── myapp/                     # Main application directory
│   ├── migrations/            # Database migrations
│   ├── __init__.py
│   ├── admin.py               # Admin panel customization
│   ├── apps.py                # App configuration
│   ├── models.py              # Database models
│   ├── tests.py               # Automated tests
│   ├── views.py               # Application views
│
├── setups/                    # Directory for uploaded setup images (optional)
├── db.sqlite3                 # SQLite database file (excluded in .gitignore)
├── manage.py                  # Django management script
└── README.md                  # This readme file
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment tools (optional but recommended)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Kenanhi/RateMySetup.git
   cd RateMySetup
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply the migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:

   - Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to see the application.
   - Go to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) to access the admin panel.
```

You can copy and paste this directly into your `README.md` file.
