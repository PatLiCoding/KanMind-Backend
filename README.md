# KanMind – Project Management Backend (Django REST API)

KanMind is a backend API for a project management tool built with Django and Django REST Framework.
The frontend is provided by the course — this backend is responsible for handling all data, business logic, and API functionality.

<hr>

## Table of Contents
- [Project Overview](#project-overview)
- [Installation & Setup](#installation--setup)
- [Environment Variables](#environment-variables)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [User System](#user-system)
- [Boards](#boards)
- [Tasks](#tasks)
- [Comments](#comments)
- [Authentication & Permissions](#authentication--permissions)
- [API Features](#api-features)
- [Serializer Design](#serializer-design)
- [Key Features & Highlights](#key-features--highlights)
- [API Authentication](#api-authentication)
- [Example API Endpoints](#example-api-endpoints)
- [Project Goal](#project-goal)
- [Author](#author)

<hr>

## Project Overview
KanMind provides a structured backend system for managing projects, tasks, and team collaboration.

It includes:
- User authentication with token-based login
- Board management (projects)
- Task management within boards
- Comments on tasks
- Role-based access via board membership
- Validation of user permissions for task assignment

The goal is to build a clean, scalable API that integrates seamlessly with a frontend application.

<hr>

## Installation & Setup

### Clone repository
```
git clone <repo-url>
```

### Create virtual environment
```
python -m venv venv
```
```
source venv/bin/activate  # Linux/Mac
```
```
venv\Scripts\activate     # Windows
```

### Install dependencies
```
pip install -r requirements.txt
```

### Run migrations
```
python manage.py migrate
```

## Environment Variables

For security reasons, the Django `SECRET_KEY` is managed via environment variables. Before starting the server, you need to set up your local `.env` file.

#### 1. Create the `.env` file
Copy the provided template file to create your local configuration:
```shell
cp .env.template .env
```

#### 2. Configure the variables
Open the newly created .env file in the root directory and add your personal configuration.

Example:
```env
SECRET_KEY=your_secret_django_key
```

### Start development server
```
python manage.py runserver
```

<hr>

## Tech Stack
- Python
- Django
- Django REST Framework (DRF)
- Token Authentication (rest_framework.authtoken)
- SQLite (development database)

<hr>

## Project Structure
```
├── auth_app/       # User management & authentication
├── boards_app/     # Board & project spaces
└── tasks_app/      # Tasks, workflows & comments
```



<hr>
 
## User System
A custom user model is used based on AbstractUser.

Features:
- Email-based authentication
- Token authentication for API access
- User registration & login
- Minimal user representation for nested relations

<hr>

## Boards
Boards represent the main project container.

Features:
- Create and manage boards
- Board owner assignment
- Add/remove members (ManyToMany relationship)
- Statistics:
  -  Member count
  -  Task count
  -  Filtered task metrics (e.g. To Do, High Priority)

<hr>

## Tasks
Tasks belong to a board and represent work items.

Features:
- Create, update, delete tasks
- Status options:
  - To Do
  - In Progress
  - Review
  - Done
- Priority levels:
  - Low / Medium / High
  - Assign users:
  - Assignee
  - Reviewer
  - Due date management
  - Automatic creator assignment
- Validation rules:
  - Assignee and reviewer must be members of the board (or board owner)

<hr>

## Comments
Comments are linked to tasks.

Features:
- Add comments to tasks
- Display:
  - Author (fullname)
  - Timestamp
  - Content

<hr>

## Authentication & Permissions
- Token-based authentication required for all protected routes
- Users can only interact with boards they belong to
- Task assignment is validated against board membership
- Secure access control across all resources

<hr>

## API Features
- Full CRUD operations for:
  - Users
  - Boards
  - Tasks
  - Comments

### Relationships:
- Board → Tasks
- Task → Comments
- User → Boards / Tasks

<hr>

## Serializer Design

The project follows a consistent serializer strategy:
- Uses ModelSerializer for all CRUD operations
- Explicit field declarations (no __all__)
- Clear and structured field ordering
- Separation of read/write fields:
  - e.g. assignee (read-only) + assignee_id (write-only)
- Validation via:
  - validate_<field>()
  - validate() for cross-field validation

<hr>

## Key Features & Highlights
- Custom validation ensures only board members can be assigned to tasks
- Clean separation of responsibilities (views, serializers, models)
- Token authentication automatically generated on user creation
- Efficient use of Django related names for reverse queries
- Nested serialization for user-friendly API responses

<hr>

## API Authentication

All requests require authentication:
`Authorization: Token <your_token>`

<hr>

## Example API Endpoints

Users
- POST /api/register/
- POST /api/login/

Boards
- GET /api/boards/
- POST /api/boards/

Tasks
- GET /api/tasks/
- POST /api/tasks/

Comments
- GET /api/comments/
- POST /api/comments/

<hr>

 ## Project Goal

This project was built to practice:
- REST API design with Django
- Clean backend architecture
- Authentication & permissions handling
- Data validation and business logic separation
- Frontend-backend integration readiness

<hr>

## Author

Developed by  Patricia Linne
