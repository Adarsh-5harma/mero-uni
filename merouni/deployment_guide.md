# CSAI Resources - Deployment Guide

## Application Overview
A comprehensive notes and resource sharing web application built with Django, MySQL, Bootstrap, HTML, CSS, and JavaScript.

## Features
- Admin functionality for resource uploads
- User navigation with responsive design
- Resource browsing and filtering
- Search functionality
- Mobile-responsive interface
- Secure authentication system

## Local Development Setup

### Prerequisites
- Python 3.11+
- MySQL Server
- pip package manager

### Installation Steps

1. **Clone/Copy the project files**
   ```bash
   # Navigate to project directory
   cd csai_resources
   ```

2. **Install dependencies**
   ```bash
   pip install django mysqlclient pillow
   ```

3. **Database Setup**
   ```bash
   # Start MySQL service
   sudo service mysql start
   
   # Create database and user
   sudo mysql -e "CREATE DATABASE csai_resources; CREATE USER 'csai_user'@'localhost' IDENTIFIED BY 'csai_password'; GRANT ALL PRIVILEGES ON csai_resources.* TO 'csai_user'@'localhost'; FLUSH PRIVILEGES;"
   ```

4. **Run migrations**
   ```bash
   python3.11 manage.py migrate
   ```

5. **Create sample data**
   ```bash
   python3.11 create_sample_data.py
   ```

6. **Create superuser**
   ```bash
   echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python3.11 manage.py shell
   ```

7. **Run development server**
   ```bash
   python3.11 manage.py runserver 0.0.0.0:8000
   ```

## Production Deployment

### Using Gunicorn + Nginx

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Update settings for production**
   ```python
   # In csit_resources/settings.py
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com', 'your-server-ip']
   
   # Static files
   STATIC_ROOT = '/var/www/csai_resources/static/'
   MEDIA_ROOT = '/var/www/csai_resources/media/'
   ```

3. **Collect static files**
   ```bash
   python3.11 manage.py collectstatic
   ```

4. **Run with Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:8000 csai_resources.wsgi:application
   ```

5. **Configure Nginx** (example configuration)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location /static/ {
           alias /var/www/csai_resources/static/;
       }
       
       location /media/ {
           alias /var/www/csai_resources/media/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## Application URLs

- **Homepage**: `/`
- **Admin Panel**: `/admin/` (admin/admin123)
- **Semester Pages**: `/semester/<number>/`
- **Subject Pages**: `/subject/<id>/`
- **Resource Detail**: `/resource/<id>/`
- **Search**: `/search/?q=<query>`
- **Resource Types**: `/type/<type-slug>/`
- **User Login**: `/accounts/login/`
- **User Registration**: `/accounts/register/`

## Database Models

### Semester
- number (unique)
- name
- description

### Subject
- name
- code (unique)
- semester (foreign key)
- description

### ResourceType
- name (unique)
- description

### Resource
- title
- description
- subject (foreign key)
- resource_type (foreign key)
- file (upload)
- uploaded_by (foreign key to User)
- uploaded_at
- updated_at
- is_active
- download_count

### UserProfile
- user (one-to-one with User)
- semester (foreign key)
- bio
- avatar
- created_at
- updated_at

## Admin Features

### Resource Management
- Upload files (PDF, DOC, etc.)
- Organize by semester and subject
- Categorize by type (Notes, Question Banks, Lab Solutions, Assignments, Previous Papers)
- Track download counts
- Activate/deactivate resources

### User Management
- View user profiles
- Manage user permissions
- Track user activity

## Security Features

- CSRF protection
- User authentication
- Admin-only resource uploads
- Secure file handling
- SQL injection prevention

## File Structure
```
csai_resources/
├── csai_resources/          # Main project directory
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── resources/              # Resources app
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # App URLs
│   ├── admin.py            # Admin configuration
│   └── migrations/         # Database migrations
├── accounts/               # User accounts app
│   ├── models.py           # User profile model
│   ├── views.py            # Account views
│   ├── urls.py             # Account URLs
│   └── admin.py            # Account admin
├── templates/              # HTML templates
│   ├── base/
│   ├── resources/
│   └── accounts/
├── static/                 # Static files (CSS, JS, images)
├── media/                  # Uploaded files
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── create_sample_data.py   # Sample data script
```

## Troubleshooting

### Common Issues

1. **MySQL Connection Error**
   - Ensure MySQL service is running
   - Check database credentials in settings.py
   - Verify user permissions

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_URL and STATIC_ROOT settings
   - Ensure web server serves static files

3. **File Upload Issues**
   - Check MEDIA_URL and MEDIA_ROOT settings
   - Ensure upload directory has write permissions
   - Verify file size limits

4. **Admin Panel Access**
   - Create superuser: `python manage.py createsuperuser`
   - Check user permissions
   - Verify admin URLs are included

## Support

For issues or questions:
1. Check Django documentation
2. Review error logs
3. Verify database connections
4. Check file permissions

## License
This project is built for educational purposes using Django framework.

