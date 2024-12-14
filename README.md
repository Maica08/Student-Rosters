# Student  Rosters   

## Description
A simple website demonstrating API using Flask.<br>
This website displays student roster management including:<br>
- Course and room assignments for each class
- Student, teacher, class assignments for each roster

## Installation
```cmd
pip install -r requirements.txt
```
## Configuration
To set_up for the database:
- Import student_roster_db_backup.sql to your local database
- Update database configuration to your Flask App:
    - `MYSQL_HOST` = `Your MySQL host`
    - `MYSQL_USER` = `Your username`
    - `MYSQL_PASSWORD` = `Your database password`
    - `MYSQL_DB` = `Database name`
    - `JWT_SECRET_KEY` = `auth_key_1001`  

## API Endpoints (markdown table)
| Endpoint  | Method    | Description  |
| --------  | -------   |--------------|
| /       | None      | Home template|
| /students| GET     | Students template|
| /teachers| GET     | Teachers template|
| /classes| GET     | Classes template|
| /classes/<int: idclasses>| GET     | Class template|
| /rooms| GET     | Rooms template|
| /courses| GET     | Courses template|
| /roster| GET     | Roster template|
| /api/students| GET     | Retrieve students|
| /api/students| POST     | Add students|
| /api/students/<int: idstudents>| PUT     | Update student|
| /api/students/<int: idstudents>| DELETE     | Delete student|
| /api/teachers| GET     | Retrieve teachers|
| /api/teachers| POST     | Add teachers|
| /api/teachers/<int: idteachers>| PUT     | Update teacher|
| /api/teachers/<int: idteachers>| DELETE     | Delete teacher|
| /api/classes| GET     | Retrieve classes|
| /api/classes| POST     | Add classes|
| /api/classes/<int: idclasses>| PUT     | Update classe|
| /api/classes/<int: idclasses>| DELETE     | Delete classe|
| /api/rooms| GET     | Retrieve rooms|
| /api/rooms| POST     | Add rooms|
| /api/rooms/<int: idrooms>| PUT     | Update room|
| /api/rooms/<int: idrooms>| DELETE     | Delete room|
| /api/courses| GET     | Retrieve courses|
| /api/courses| POST     | Add courses|
| /api/courses/<int: idcourses>| PUT     | Update course|
| /api/courses/<int: idcourses>| DELETE     | Delete course|
| /api/rosters| GET     | Retrieve rosters|
| /api/rosters| POST     | Add rosters|
| /api/rosters/<int: idrosters>| PUT     | Update roster|
| /api/rosters/<int: idrosters>| DELETE     | Delete roster|
| /auth/login| POST     | User Authorization Log In|

## Testing
 For testing app.py
 ```cmd
 pytest tests\test_app.py
 ```
 For testing auth.py
 ```cmd
 pytest tests\test_auth.py
 ```
 For test coverage
 ```cmd
 pytest --cov
 ```
