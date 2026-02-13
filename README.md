# 📋 Todo Web App - Full-Featured Task Management System

A modern, production-structured Django web application for managing tasks with complete user authentication, profile management, and interactive features.

## ✨ Features

### User Authentication & Account Management
- ✅ User Registration with email validation
- ✅ Login & Logout functionality
- ✅ Update profile (username, email, name)
- ✅ Change password securely
- ✅ Delete account with password confirmation
- ✅ User profile with bio section

### Task Management
- ✅ Create, Read, Update, Delete (CRUD) tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Task priority levels (Low, Medium, High)
- ✅ Due dates with overdue indicators
- ✅ Task descriptions
- ✅ Task filtering (All, Completed, Pending)
- ✅ Priority-based filtering
- ✅ Search functionality
- ✅ Quick task addition from dashboard

### Dashboard & Statistics
- ✅ Task overview cards (Total, Completed, Pending)
- ✅ Completion progress visualization
- ✅ Quick add task widget
- ✅ Recent tasks display
- ✅ Overdue task alerts
- ✅ Due today notifications

### Dynamic Features
- ✅ AJAX-based task updates (no page reload)
- ✅ Smooth animations and transitions
- ✅ Real-time completion percentage
- ✅ Form validation
- ✅ Success/error notifications
- ✅ Responsive mobile-first design

## 🎨 Design System

### Color Palette
```css
Primary: #4F46E5 (Indigo)
Secondary: #14B8A6 (Teal)
Danger: #EF4444 (Red)
Success: #22C55E (Green)
Background: #F8FAFC (Slate)
```

### Architecture
- **Atomic Design**: Components organized into atoms, molecules, and organisms
- **Clean Architecture**: Separation of concerns with modular structure
- **Responsive Design**: Mobile-first approach with adaptive layouts
- **Modern UI**: Flat design with subtle shadows and smooth transitions

## 🛠 Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Django 4.2** | Web framework |
| **SQLite 3** | Database |
| **Django ORM** | Database abstraction |
| **Django Templates** | Server-side rendering |
| **Vanilla JavaScript** | Client-side interactivity |
| **HTML5 & CSS3** | Frontend structure & styling |

## 📁 Project Structure

```
todo_project/
├── manage.py                          # Django management command
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
│
├── todoapp/                           # Project configuration
│   ├── __init__.py
│   ├── settings.py                   # Django settings
│   ├── urls.py                       # Project URLs
│   ├── asgi.py                       # ASGI config
│   └── wsgi.py                       # WSGI config
│
└── tasks/                             # Main application
    ├── migrations/                    # Database migrations
    ├── templates/                     # HTML templates
    │   ├── base.html                 # Base layout template
    │   ├── auth/
    │   │   ├── login.html            # Login page
    │   │   └── register.html         # Registration page
    │   └── tasks/
    │       ├── dashboard.html        # Dashboard overview
    │       ├── task_list.html        # Task list view
    │       ├── task_form.html        # Create/edit task form
    │       ├── task_confirm_delete.html # Delete confirmation
    │       └── profile.html          # User profile page
    │
    ├── static/                        # Static files
    │   ├── css/
    │   │   └── style.css             # Main stylesheet (1500+ lines)
    │   └── js/
    │       └── main.js               # Main JavaScript (700+ lines)
    │
    ├── __init__.py
    ├── admin.py                       # Django admin customization
    ├── apps.py                        # App configuration
    ├── models.py                      # Data models (Task, UserProfile)
    ├── forms.py                       # Form definitions
    ├── views.py                       # View logic (850+ lines)
    ├── urls.py                        # App URL routing
    ├── signals.py                     # Django signals
    └── tests.py                       # Unit tests
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone or create the project directory**
```bash
cd todo_project
```

2. **Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create migrations**
```bash
python manage.py makemigrations
```

5. **Apply migrations**
```bash
python manage.py migrate
```

6. **Create superuser (admin account)**
```bash
python manage.py createsuperuser
# Follow the prompts to create an admin account
```

7. **Run development server**
```bash
python manage.py runserver
```

8. **Access the application**
- Main app: `http://127.0.0.1:8000/`
- Admin panel: `http://127.0.0.1:8000/admin/`

## 📖 Usage Guide

### First Time Setup
1. Visit `http://127.0.0.1:8000/` to see the login page
2. Click "Sign up here" to create a new account
3. After registration, log in with your credentials
4. You'll be redirected to the dashboard

### Creating Tasks
1. Click "Create Task" button or go to Tasks menu
2. Fill in the task details:
   - **Title** (required): What you need to do
   - **Description**: Additional details
   - **Due Date**: When it's due
   - **Priority**: Low, Medium, or High
3. Click "Create Task" to save

### Managing Tasks
- **Mark Complete**: Click the checkbox next to the task
- **Edit Task**: Click the ✏️ button
- **Delete Task**: Click the 🗑️ button
- **Filter Tasks**: Use the filter controls to find specific tasks
- **Search Tasks**: Use the search bar to find by title or description

### Managing Your Account
1. Click on your username in the navigation bar
2. Select "My Profile"
3. Update your information:
   - Account Information: username, email, name
   - Bio: About yourself
   - Password: Change your password
   - Danger Zone: Delete your account

## 🔐 Security Features

- ✅ CSRF Protection (Cross-Site Request Forgery)
- ✅ Password hashing with Django's authentication system
- ✅ SQL Injection prevention via ORM
- ✅ XSS Protection with template escaping
- ✅ User isolation - users can only see their own tasks
- ✅ LoginRequiredMixin for protected views
- ✅ Secure password change and deletion flows

## 📱 Responsive Design

The application is fully responsive and works on:
- **Desktop**: Full-featured interface with multi-column layouts
- **Tablet**: Adapted grid layouts and touch-friendly buttons
- **Mobile**: Single column layout with optimized spacing and font sizes

## 🎯 API Endpoints

### Authentication
- `POST /register/` - User registration
- `POST /login/` - User login
- `GET /logout/` - User logout

### Dashboard
- `GET /` - Dashboard overview

### Tasks
- `GET /tasks/` - Task list view
- `GET /tasks/create/` - Create task form
- `POST /tasks/create/` - Create new task
- `GET /tasks/<id>/edit/` - Edit task form
- `POST /tasks/<id>/edit/` - Update task
- `GET /tasks/<id>/delete/` - Delete confirmation
- `POST /tasks/<id>/delete/` - Delete task

### AJAX Endpoints
- `POST /api/tasks/<id>/toggle/` - Toggle task completion
- `POST /api/tasks/quick-add/` - Quick add task
- `POST /api/tasks/<id>/delete/` - Delete task via AJAX
- `GET /api/tasks/<id>/detail/` - Get task details

### Profile
- `GET /profile/` - View profile
- `POST /profile/edit/` - Update profile
- `POST /profile/edit-bio/` - Update bio
- `POST /profile/change-password/` - Change password
- `POST /profile/delete-account/` - Delete account

## 🗄️ Database Models

### Task Model
```python
- user (ForeignKey to User)
- title (CharField, max 255)
- description (TextField, optional)
- due_date (DateField, optional)
- priority (Choice: low/medium/high)
- completed (BooleanField)
- created_at (DateTimeField, auto_add)
- updated_at (DateTimeField, auto_update)
```

### UserProfile Model
```python
- user (OneToOneField to User)
- bio (TextField, max 500)
- updated_at (DateTimeField, auto_update)
```

## 🧪 Testing

### Run tests
```bash
python manage.py test
```

### Test coverage
- Model validation tests
- View permission tests
- Form validation tests
- AJAX endpoint tests

## 🛠 Customization

### Change Colors
Edit the CSS variables in `tasks/static/css/style.css`:
```css
:root {
    --primary-color: #4F46E5;
    --secondary-color: #14B8A6;
    /* ... other colors ... */
}
```

### Add More Task Fields
1. Update the Task model in `tasks/models.py`
2. Create a migration: `python manage.py makemigrations`
3. Apply migration: `python manage.py migrate`
4. Update `TaskForm` in `tasks/forms.py`
5. Update templates to display new fields

### Extend User Profile
Add fields to the `UserProfile` model in `tasks/models.py` and update the profile template.

## 📦 Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings.py
- [ ] Set a strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up HTTPS
- [ ] Configure static files collection
- [ ] Set up proper database (PostgreSQL recommended)
- [ ] Configure email backend
- [ ] Set up environment variables using python-decouple
- [ ] Run `collectstatic` command

### Deploy to Heroku
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Deploy to PythonAnywhere
1. Upload files to your account
2. Set up virtual environment
3. Configure Web app
4. Run migrations
5. Set up static files

## 🐛 Troubleshooting

### Issues with Migrations
```bash
# Reset database (development only)
python manage.py migrate tasks zero
python manage.py makemigrations
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

## 📝 Code Quality

The project follows:
- **PEP 8** Python style guide
- **Django best practices** for structure and security
- **DRY (Don't Repeat Yourself)** principle
- **SOLID** principles where applicable
- **Atomic Design** methodology for UI components

## 🤝 Contributing

To contribute to this project:
1. Follow the existing code style
2. Add comments to complex logic
3. Update tests when adding features
4. Test thoroughly before submitting

## 📄 License

This project is provided as-is for educational and commercial use.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Django documentation at https://docs.djangoproject.com/
3. Check the code comments for implementation details

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django for Beginners](https://djangoforbeginners.com/)
- [Mozilla MDN Web Docs](https://developer.mozilla.org/)
- [CSS-Tricks](https://css-tricks.com/)

---

**Built with ❤️ using Django | Ready for Production**

Version 1.0.0 | Last Updated: February 2026
