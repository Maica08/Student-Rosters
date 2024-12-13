from flask import Flask, render_template, jsonify, request, make_response
from flask_mysqldb import MySQL
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "student_roster_db"
mysql = MySQL(app)

def execute_json(query, *args):
    cur = mysql.connection.cursor()
    try:
        cur.execute(query, args if args else ())
        data = cur.fetchall()
    except Exception as e:
        return make_response(jsonify({"error": "Database error", "message": str(e)}), 500)
    finally:
        cur.close()
    return data

def execute_template(query, *args):
    cur = mysql.connection.cursor()
    try:
        cur.execute(query, args if args else ())
        columns = [col[0] for col in cur.description]
        data = [dict(zip(columns, row)) for row in cur.fetchall()]
    except Exception as e:
        return make_response(jsonify({"error": "Database error", "message": str(e)}), 500)
    finally:
        cur.close()
    return data

def commit(query, *args):
    cur = mysql.connection.cursor()
    try:
        cur.execute(query, args)
        mysql.connection.commit()
        rows_affected = cur.rowcount
    except Exception as e:
        mysql.connection.rollback()
        return make_response(jsonify({"error": "Commit failed", "message": str(e)}), 500)
    finally:
        cur.close()
    return rows_affected

def validate_request_data(required_fields):
    if not request.is_json:
        raise BadRequest("Request must be JSON")
    data = request.get_json()
    for field in required_fields:
        if field not in data:
            raise BadRequest(f"'{field}' is required")
    return data

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return make_response(jsonify({"error": "Bad Request", "message": str(e)}), 400)

@app.errorhandler(404)
def handle_not_found(e):
    return make_response(jsonify({"error": "Not Found", "message": str(e)}), 404)


@app.route("/")
def home():
    query = """
        SELECT 
            classes.description AS class,
            class_period AS period,
            courses.name AS course,
            CONCAT(teachers.firstname, ' ', teachers.lastname) AS teacher,
            rooms.location AS room
        FROM classes
        INNER JOIN rooms ON idrooms = idroom
        INNER JOIN courses ON idcourses = idcourse
        INNER JOIN roster ON idclasses = idclass
        INNER JOIN teachers ON idteachers = idteacher
        GROUP BY classes.description, class_period, courses.name, rooms.location, teacher
        ORDER BY classes.description;
    """
    
    results = execute_template(query)
    return render_template('index.html', results=results)

# Students CRUD

@app.route("/students", methods=["GET"])
def get_students():
    query = """SELECT * FROM students ORDER BY firstname"""
    results = execute_template(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return render_template('students.html', results=results)

@app.route("/api/students", methods=["GET"])
def get_students_api():
    query = """SELECT * FROM students """
    results = execute_json(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return make_response(jsonify(results), 200)

@app.route("/api/students", methods=["POST"])
def add_students():
    data = request.get_json()
    firstname = data["firstname"]
    middlename = data.get("middlename")
    lastname = data["lastname"]
    birthdate = data["birthdate"]
    gender = data["gender"]
    
    query = """INSERT INTO students (firstname, middlename, lastname, birthdate, gender) VALUES (%s, %s, %s, %s, %s)"""
    rows = commit(query, firstname, middlename, lastname, birthdate, gender)

    return make_response(jsonify(
        {"message": "data created successfully", "rows_affected": rows}
        ), 201)

@app.route("/api/students/<int:idstudents>", methods=["PUT"])
def update_students(idstudents):
    data = request.get_json()
    firstname = data["firstname"]
    middlename = data.get("middlename")
    lastname = data["lastname"]
    birthdate = data["birthdate"]
    gender = data["gender"]
    
    query = """UPDATE students SET firstname=%s, middlename=%s, lastname=%s, birthdate=%s, gender=%s WHERE idstudents=%s"""
    rows = commit(query, firstname, middlename, lastname, birthdate, gender, idstudents)
                
    return make_response(jsonify(
        {"message": "data updated successfully", "rows_affected": rows}
        ), 200)
    
@app.route("/students/<int:idstudents>", methods=["DELETE"])
def delete_student(idstudents):
    query = """DELETE FROM students WHERE idstudents=%s"""
    rows = commit(query, idstudents)
        
    return make_response(jsonify(
        {"message": "data deleted successfully", "rows_affected": rows}
        ), 200)   
    

# Teachers CRUD

@app.route("/teachers", methods=["GET"])
def get_teachers():
    query = """SELECT * FROM teachers ORDER BY firstname"""
    results = execute_template(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return render_template('teachers.html', results=results)

@app.route("/api/teachers", methods=["GET"])
def get_teachers_api():
    query = """SELECT * FROM teachers """
    results = execute_json(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return make_response(jsonify(results), 200)

@app.route("/api/teachers", methods=["POST"])
def add_teachers():
    data = request.get_json()
    firstname = data["firstname"]
    middlename = data.get("middlename")
    lastname = data["lastname"]
    birthdate = data["birthdate"]
    gender = data["gender"]
    
    query = """INSERT INTO teachers (firstname, middlename, lastname, birthdate, gender) VALUES (%s, %s, %s, %s, %s)"""
    rows = commit(query, firstname, middlename, lastname, birthdate, gender)

    return make_response(jsonify(
        {"message": "data created successfully", "rows_affected": rows}
        ), 201)

@app.route("/api/teachers/<int:idteachers>", methods=["PUT"])
def update_teachers(idteachers):
    data = request.get_json()
    firstname = data["firstname"]
    middlename = data.get("middlename")
    lastname = data["lastname"]
    birthdate = data["birthdate"]
    gender = data["gender"]
    
    query = """UPDATE teachers SET firstname=%s, middlename=%s, lastname=%s, birthdate=%s, gender=%s WHERE idteachers=%s"""
    rows = commit(query, firstname, middlename, lastname, birthdate, gender, idteachers)
        
    return make_response(jsonify(
        {"message": "data updated successfully", "rows_affected": rows}
        ), 200)
    
@app.route("/api/teachers/<int:idteachers>", methods=["DELETE"])
def delete_teacher(idteachers):
    query = """DELETE FROM teachers WHERE idteachers=%s"""
    rows = commit(query, idteachers)
        
    return make_response(jsonify(
        {"message": "data deleted successfully", "rows_affected": rows}
        ), 200)   

# Classes CRUD

@app.route("/classes", methods=["GET"])
def get_classes():
    query = """
    SELECT 
        idclasses, 
        classes.description AS 'class description',
        rooms.location AS location,
        courses.name AS course,
        courses.code AS code
    FROM classes
    INNER JOIN rooms
    ON idrooms = idroom
    INNER JOIN courses
    ON idcourses = idcourse
    ORDER BY classes.description
    """
    results = execute_template(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return render_template('classes.html', results=results)

@app.route("/api/classes", methods=["GET"])
def get_classes_api():
    query = """SELECT * FROM classes """
    results = execute_json(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return make_response(jsonify(results), 200)

@app.route("/api/classes/<int:idclasses>", methods=["GET"])
def get_class(idclasses):
    query = """
    SELECT 
        idclasses, 
        classes.description AS 'class description',
        CONCAT(firstname, ' ', lastname) as student
    FROM classes
    INNER JOIN roster
    ON idclasses = idclass
    INNER JOIN students
    ON idstudents = idstudent
    WHERE idclasses = %s
    ORDER BY students.firstname
    """
    results = execute_template(query, idclasses)
    
    query1 = """
        SELECT 
            idclasses, 
            classes.description AS 'class description'
        FROM classes
        WHERE idclasses = %s
    """
    cur_class = execute_template(query1, idclasses)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return render_template('class.html', results=jsonify(results), cur_class=cur_class)

@app.route("/api/classes", methods=["POST"])
def add_classes():
    data = request.get_json()
    description = data["description"]
    idroom = data.get("idroom")  
    idcourse = data.get("idcourse")    
    query = """INSERT INTO classes (description, idroom, idcourse) VALUES (%s, %s, %s)"""
    rows = commit(query, description, idroom, idcourse)
    
    return make_response(jsonify(
        {"message": "data created successfully", "rows_affected": rows}
        ), 201)

@app.route("/api/classes/<int:idclasses>", methods=["PUT"])
def update_classes(idclasses):
    data = request.get_json()
    description = data["description"]
    idroom = data.get("idroom")  
    idcourse = data.get("idcourse")    
    
    query = """UPDATE classes SET description=%s, idroom=%s, idcourse=%s WHERE idclasses=%s"""
    rows = commit(query, description, idroom, idcourse, idclasses)
        
    return make_response(jsonify(
        {"message": "data updated successfully", "rows_affected": rows}
        ), 200)
    
@app.route("/api/classes/<int:idclasses>", methods=["DELETE"])
def delete_class(idclasses):
    query = """DELETE FROM classes WHERE idclasses=%s"""
    rows = commit(query, idclasses)
        
    return make_response(jsonify(
        {"message": "data deleted successfully", "rows_affected": rows}
        ), 200)   
    

# Rooms CRUD

@app.route("/rooms", methods=["GET"])
def get_rooms():
    query = """
    SELECT 
        idrooms, 
        description,
        location
    FROM rooms
    ORDER BY location
    """
    results = execute_template(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return render_template('rooms.html', results=results)

@app.route("/api/rooms", methods=["GET"])
def get_rooms_api():
    query = """SELECT * FROM rooms """
    results = execute_json(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return make_response(jsonify(results), 200)

@app.route("/api/rooms", methods=["POST"])
def add_rooms():
    data = request.get_json()
    location = data["location"]
    description = data.get("description")
    query = """INSERT INTO rooms (location, description) VALUES (%s, %s)"""
    rows = commit(query, location, description)
    
    return make_response(jsonify(
        {"message": "data created successfully", "rows_affected": rows}
        ), 201)

@app.route("/api/rooms/<int:idrooms>", methods=["PUT"])
def update_rooms(idrooms):
    data = request.get_json()
    location = data["location"]
    description = data.get("description")
    
    query = """UPDATE rooms SET location=%s, description=%s WHERE idrooms=%s"""
    rows = commit(query, location, description, idrooms)
        
    return make_response(jsonify(
        {"message": "data updated successfully", "rows_affected": rows}
        ), 200)
    
@app.route("/api/rooms/<int:idrooms>", methods=["DELETE"])
def delete_room(idrooms):
    query = """DELETE FROM rooms WHERE idrooms=%s"""
    rows = commit(query, idrooms)
        
    return make_response(jsonify(
        {"message": "data deleted successfully", "rows_affected": rows}
        ), 200)   
    
# Courses CRUD

@app.route("/courses", methods=["GET"])
def get_courses():
    query = """
    SELECT 
        idcourses, 
        name,
        code
    FROM courses
    ORDER BY name
    """
    results = execute_template(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return render_template('courses.html', results=results)

@app.route("/api/courses", methods=["GET"])
def get_courses_api():
    query = """SELECT * FROM courses """
    results = execute_json(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return make_response(jsonify(results), 200)

@app.route("/api/courses", methods=["POST"])
def add_courses():
    data = request.get_json()
    name = data["name"]
    code = data["code"]
    query = """INSERT INTO courses (name, code) VALUES (%s, %s)"""
    rows = commit(query, name, code)
    
    return make_response(jsonify(
        {"message": "data created successfully", "rows_affected": rows}
        ), 201)

@app.route("/api/courses/<int:idcourses>", methods=["PUT"])
def update_courses(idcourses):
    data = request.get_json()
    name = data["name"]
    code = data["code"]
    
    query = """UPDATE courses SET name=%s, code=%s WHERE idcourses=%s"""
    rows = commit(query, name, code, idcourses)
        
    return make_response(jsonify(
        {"message": "data updated successfully", "rows_affected": rows}
        ), 200)
    
@app.route("/api/courses/<int:idcourses>", methods=["DELETE"])
def delete_course(idcourses):
    query = """DELETE FROM courses WHERE idcourses=%s"""
    rows = commit(query, idcourses)
        
    return make_response(jsonify(
        {"message": "data deleted successfully", "rows_affected": rows}
        ), 200)   

# Roster CRUD

@app.route("/roster", methods=["GET"])
def get_roster():
    query = """SELECT 
                idroster, idclass, idstudent, idteacher, class_period,
                CONCAT(teachers.firstname, ' ', teachers.lastname) AS teacher,
                CONCAT(students.firstname, ' ', students.lastname) AS student,
                classes.description AS description
                FROM roster
                INNER JOIN classes
                ON idclasses = idclass
                INNER JOIN students
                ON idstudents = idstudent
                INNER JOIN teachers
                ON idteachers = idteacher
                """
    results = execute_template(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return render_template('roster.html', results=results)

@app.route("/api/roster", methods=["GET"])
def get_roster_api():
    query = """SELECT * FROM roster """
    results = execute_json(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return make_response(jsonify(results), 200)

@app.route("/api/roster", methods=["POST"])
def add_roster():
    data = request.get_json()
    idclass = data.get("idclass")
    idstudent = data.get("idstudent")
    idteacher = data.get("idteacher")
    class_period = data["class_period"]
    
    query = """INSERT INTO roster (idclass, idstudent, idteacher, class_period) VALUES (%s, %s, %s, %s)"""
    rows = commit(query, idclass, idstudent, idteacher, class_period)

    return make_response(jsonify(
        {"message": "data created successfully", "rows_affected": rows}
        ), 201)

@app.route("/api/roster/<int:idroster>", methods=["PUT"])
def update_roster(idroster):
    data = request.get_json()
    idclass = data.get("idclass")
    idstudent = data.get("idstudent")
    idteacher = data.get("idteacher")
    class_period = data["class_period"]
    
    query = """UPDATE roster SET idclass=%s, idstudent=%s, idteacher=%s WHERE idroster=%s"""
    rows = commit(query, idclass, idstudent, idteacher, class_period, idroster)
        
    return make_response(jsonify(
        {"message": "data updated successfully", "rows_affected": rows}
        ), 200)
    
@app.route("/api/roster/<int:idroster>", methods=["DELETE"])
def delete_roster(idroster):
    query = """DELETE FROM roster WHERE idroster=%s"""
    rows = commit(query, idroster)
        
    return make_response(jsonify(
        {"message": "data deleted successfully", "rows_affected": rows}
        ), 200)   
    
    
@app.route("/api")
def api():
    return render_template('api.html')


if __name__ == "__main__":
    app.run(debug=True)
