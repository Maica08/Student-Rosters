from flask import Flask, render_template, jsonify, request, make_response
from flask_mysqldb import MySQL
from auth import auth_bp, role_required
from werkzeug.exceptions import BadRequest
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "student_roster_db"
app.config["JWT_SECRET_KEY"] = "auth_key_1001"  
mysql = MySQL(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')


def execute_json(query, *args):
    cur = mysql.connection.cursor()
    try:
        cur.execute(query, *args if args else ())
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
        return cur.rowcount
    except Exception as e:
        mysql.connection.rollback()
        raise RuntimeError(f"Commit failed: {str(e)}")
    finally:
        cur.close()

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
@role_required(["admin", "teacher"])
def get_students_api():
    query = "SELECT * FROM students"
    results = execute_json(query)
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return make_response(jsonify(results), 200)

@app.route("/api/students", methods=["POST"])
@role_required(["admin"])
def add_students():
    data = validate_request_data(["firstname", "lastname", "birthdate", "gender"])
    query = """INSERT INTO students (firstname, middlename, lastname, birthdate, gender) VALUES (%s, %s, %s, %s, %s)"""
    rows = commit(query, data["firstname"], data.get("middlename"), data["lastname"], data["birthdate"], data["gender"])
    if isinstance(rows, Flask.response_class):
        return rows    
    return make_response(jsonify({"message": "data created successfully", "rows_affected": rows}), 201)

@app.route("/api/students/<int:idstudents>", methods=["PUT"])
@role_required(["admin"])
def update_students(idstudents):
    data = validate_request_data(["firstname", "lastname", "birthdate", "gender"])
    query = """UPDATE students SET firstname=%s, middlename=%s, lastname=%s, birthdate=%s, gender=%s WHERE idstudents=%s"""
    rows = commit(query, data["firstname"], data.get("middlename"), data["lastname"], data["birthdate"], data["gender"], idstudents)
    if isinstance(rows, Flask.response_class):
        return rows    
    return make_response(jsonify({"message": "data updated successfully", "rows_affected": rows}), 200)

@app.route("/api/students/<int:idstudents>", methods=["DELETE"])
@role_required(["admin"])
def delete_student(idstudents):
    query = "DELETE FROM students WHERE idstudents=%s"
    rows = commit(query, idstudents)
    if isinstance(rows, Flask.response_class):
        return rows    
    return make_response(jsonify({"message": "data deleted successfully", "rows_affected": rows}), 200)
    
# Teachers CRUD

@app.route("/teachers", methods=["GET"])
def get_teachers():
    query = """SELECT * FROM teachers ORDER BY firstname"""
    results = execute_template(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return render_template('teachers.html', results=results)

@app.route("/api/teachers", methods=["GET"])
@role_required(["admin"])
def get_teachers_api():
    query = """SELECT * FROM teachers """
    results = execute_json(query)
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return make_response(jsonify(results), 200)


@app.route("/api/teachers", methods=["POST"])
@role_required(["admin"])
def add_teachers():
    data = validate_request_data(["firstname", "lastname", "birthdate", "gender"])    
    query = """INSERT INTO teachers (firstname, middlename, lastname, birthdate, gender) VALUES (%s, %s, %s, %s, %s)"""
    rows = commit(query, data["firstname"], data.get("middlename"), data["lastname"], data["birthdate"], data["gender"])
    
    if isinstance(rows, Flask.response_class):
        return rows    
    return make_response(jsonify(
        {"message": "data created successfully", "rows_affected": rows}
        ), 201)

@app.route("/api/teachers/<int:idteachers>", methods=["PUT"])
@role_required(["admin"])
def update_teachers(idteachers):
    data = validate_request_data(["firstname", "lastname", "birthdate", "gender"])    
    query = """UPDATE teachers SET firstname=%s, middlename=%s, lastname=%s, birthdate=%s, gender=%s WHERE idteachers=%s"""
    rows = commit(query, data["firstname"], data.get("middlename"), data["lastname"], data["birthdate"], data["gender"], idteachers)
        
    if isinstance(rows, Flask.response_class):
        return rows    
    return make_response(jsonify(
        {"message": "data updated successfully", "rows_affected": rows}
        ), 200)
    
@app.route("/api/teachers/<int:idteachers>", methods=["DELETE"])
@role_required(["admin"])
def delete_teacher(idteachers):
    query = """DELETE FROM teachers WHERE idteachers=%s"""
    rows = commit(query, idteachers)
    
    if isinstance(rows, Flask.response_class):
        return rows    
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
        return results
    return render_template('classes.html', results=results)

@app.route("/api/classes", methods=["GET"])
def get_classes_api():
    query = """SELECT * FROM classes"""
    results = execute_json(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return make_response(jsonify(results), 200)

@app.route("/classes/<int:idclasses>", methods=["GET"])
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
        results=False
    return render_template('class.html', results=results, cur_class=cur_class)

@app.route("/api/classes", methods=["POST"])
@role_required(["admin"])
def add_classes():
    data = validate_request_data(["description"])
    query = """INSERT INTO classes (description, idroom, idcourse) VALUES (%s, %s, %s)"""
    rows = commit(query, data["description"], data.get("idroom"), data.get("idcourse"))
    
    if isinstance(rows, Flask.response_class):
        return rows    
    return make_response(jsonify(
        {"message": "data created successfully", "rows_affected": rows}
        ), 201)

@app.route("/api/classes/<int:idclasses>", methods=["PUT"])
@role_required(["admin"])
def update_classes(idclasses):
    data = validate_request_data(["description"])
    query = """UPDATE classes SET description=%s, idroom=%s, idcourse=%s WHERE idclasses=%s"""
    rows = commit(query, data["description"], data.get("idroom"), data.get("idcourse"), idclasses)
    
    if isinstance(rows, Flask.response_class):
        return rows    
        
    return make_response(jsonify(
        {"message": "data updated successfully", "rows_affected": rows}
        ), 200)

@app.route("/api/classes/<int:idclasses>", methods=["DELETE"])
@role_required(["admin"])
def delete_class(idclasses):
    query = """DELETE FROM classes WHERE idclasses=%s"""
    rows = commit(query, idclasses)
    
    if isinstance(rows, Flask.response_class):
        return rows            
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
        return results
    return render_template('rooms.html', results=results)


@app.route("/api/rooms", methods=["GET"])
def get_rooms_api():
    query = """SELECT * FROM rooms """
    results = execute_json(query)
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return make_response(jsonify(results), 200)

@app.route("/api/rooms", methods=["POST"])
@role_required(["admin"])
def add_rooms():
    data = validate_request_data(["location"])
    query = """INSERT INTO rooms (location, description) VALUES (%s, %s)"""
    rows = commit(query, data["location"], data.get("description"))
    
    if isinstance(rows, Flask.response_class):
        return rows    
    return make_response(jsonify(
        {"message": "data created successfully", "rows_affected": rows}
        ), 201)

@app.route("/api/rooms/<int:idrooms>", methods=["PUT"])
@role_required(["admin"])
def update_rooms(idrooms):
    data = validate_request_data(["location"])
    query = """UPDATE rooms SET location=%s, description=%s WHERE idrooms=%s"""
    rows = commit(query, data["location"], data.get("description"), idrooms)
        
    if isinstance(rows, Flask.response_class):
        return rows    
    return make_response(jsonify(
        {"message": "data updated successfully", "rows_affected": rows}
        ), 200)
    
@app.route("/api/rooms/<int:idrooms>", methods=["DELETE"])
@role_required(["admin"])
def delete_room(idrooms):
    query = """DELETE FROM rooms WHERE idrooms=%s"""
    rows = commit(query, idrooms)
    
    if isinstance(rows, Flask.response_class):
        return rows    
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
        return results
    return render_template('courses.html', results=results)

@app.route("/api/courses", methods=["GET"])
def get_courses_api():
    query = """SELECT * FROM courses """
    results = execute_json(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return make_response(jsonify(results), 200)

@app.route("/api/courses", methods=["POST"])
@role_required(["admin", "teacher"])
def add_courses():
    data = validate_request_data(["name", "code"])
    query = """INSERT INTO courses (name, code) VALUES (%s, %s)"""
    rows = commit(query, data["name"], data["code"])
    
    if isinstance(rows, Flask.response_class):
        return rows    
    return make_response(jsonify(
        {"message": "data created successfully", "rows_affected": rows}
        ), 201)
    
@app.route("/api/courses/<int:idcourses>", methods=["PUT"])
@role_required(["admin"])
def update_courses(idcourses):
    data = validate_request_data(["name", "code"])
    query = """UPDATE courses SET name=%s, code=%s WHERE idcourses=%s"""
    rows = commit(query, data["name"], data["code"], idcourses)
        
    if isinstance(rows, Flask.response_class):
        return rows    
    return make_response(jsonify(
        {"message": "data updated successfully", "rows_affected": rows}
        ), 200)
    
@app.route("/api/courses/<int:idcourses>", methods=["DELETE"])
@role_required(["admin"])
def delete_course(idcourses):
    query = """DELETE FROM courses WHERE idcourses=%s"""
    rows = commit(query, idcourses)
        
    if isinstance(rows, Flask.response_class):
        return rows    
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
        return results
    return render_template('roster.html', results=results)

@app.route("/api/roster", methods=["GET"])
def get_roster_api():
    query = """SELECT * FROM roster """
    results = execute_json(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return make_response(jsonify(results), 200)

@app.route("/api/roster", methods=["POST"])
@role_required(["admin"])
def add_roster():
    data = validate_request_data(["class_period"])
    query = """INSERT INTO roster (idclass, idstudent, idteacher, class_period) VALUES (%s, %s, %s, %s)"""
    rows = commit(query, data.get("idclass"), data.get("idstudent"), data.get("idteacher"), data["class_period"])
    
    if isinstance(rows, Flask.response_class):
        return rows    
    return make_response(jsonify(
        {"message": "data created successfully", "rows_affected": rows}
        ), 201)
    

@app.route("/api/roster/<int:idroster>", methods=["PUT"])
@role_required(["admin"])
def update_roster(idroster):
    data = validate_request_data(["class_period"])
    query = """UPDATE roster SET idclass=%s, idstudent=%s, idteacher=%s WHERE idroster=%s"""
    rows = commit(query, data.get("idclass"), data.get("idstudent"), data.get("idteacher"), data["class_period"], idroster)
        
    if isinstance(rows, Flask.response_class):
        return rows    
    return make_response(jsonify(
        {"message": "data updated successfully", "rows_affected": rows}
        ), 200)
    
@app.route("/api/roster/<int:idroster>", methods=["DELETE"])
@role_required(["admin"])
def delete_roster(idroster):
    query = """DELETE FROM roster WHERE idroster=%s"""
    rows = commit(query, idroster)
        
    if isinstance(rows, Flask.response_class):
        return rows    
    return make_response(jsonify(
        {"message": "data deleted successfully", "rows_affected": rows}
        ), 200)   
    
# API Page
    
@app.route("/api")
def api():
    return render_template('api.html')


if __name__ == "__main__":
    app.run(debug=True)
