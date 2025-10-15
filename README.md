

***

# Simple Team-Based Bug Tracker 🐞

A lightweight, database-driven web application built in Django for small teams. Log, assign, track, and resolve software defects. Demonstrates core Django features including user authentication, role-based permissions, foreign keys, and a customized admin interface.

***

## Features

- **User Authentication:** Secure registration, login, and logout.
- **Role-Based Permissions:**  
  - *Reporters:* Create/view all bug tickets.  
  - *Developers:* Assigned tickets, can update ticket status.
- **Ticket Management:** Full CRUD for bug tickets (web interface & Django admin).
- **Workflow Management:** Simple ticket status (`To Do` → `In Progress` → `Resolved`).
- **Ticket Assignment:** Reporters assign tickets to Developers.
- **Dynamic Filtering:** Filter tickets by assignment, status, or all.
- **Built-in Security:** Django's default protections, including CSRF.
- **Admin Interface:** Convenient panel for managing data and configuring roles.

***

## Technology Stack

- **Backend:** Python 3, Django
- **Database:** SQLite 3 (default; can swap for PostgreSQL/MySQL)
- **Frontend:** HTML, CSS

***

## Installation

### Prerequisites

- Python 3.8+
- `pip` and `venv` (with Python)
- Git

### Steps

1. **Clone the Repository**

   ```bash
   git clone <your-repository-url>
   cd bug-tracker
   ```

2. **Set Up Virtual Environment**

   ```bash
   python -m venv venv
   ```

   Activate:

   - Windows: `.\venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   # Or if requirements.txt doesn't exist yet:
   pip freeze > requirements.txt
   ```

4. **Database Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create Superuser**

   ```bash
   python manage.py createsuperuser
   # Follow prompts for username/email/password
   ```

***

## Running the App

1. **Start Development Server**

   ```bash
   python manage.py runserver
   ```

2. **Access:**

   - Main site: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

***

## Example Workflow

- **Admin:**
  - Log in to `/admin/` with superuser.
  - Register users (or allow self-registration).
  - Assign roles in Teams > Profiles.

- **Reporter:**
  - Log in.
  - Click "New Ticket", describe bug, set priority, assign to Developer.
  - Submit form.

- **Developer:**
  - Log in.
  - Filter "My Assigned Tickets."
  - Open ticket, update status as work progresses (`To Do`, `In Progress`, `Resolved`).

***

## Running Tests

Run the built-in Django test suite for models, view permissions, and security:

```bash
python manage.py test
```

***

## Project Structure

- `teams/`: Profiles, roles (Reporter/Developer), registration/authentication.
- `tickets/`: Ticket models, views (CRUD), status logic, filtering.

***

## Planned Improvements

- Comment system for ticket discussions.
- File attachments (screenshots, logs) for tickets.
- Email notifications for assignments/updates.
- Dashboard with team activity statistics.
- Advanced search for tickets by title or description.

***

> Questions, bug reports, and contributions are welcome via GitHub Issues and Pull Requests!

---
