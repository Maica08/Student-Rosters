from flask import Flask, render_template, jsonify, request, make_response
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "student_roster_db"
mysql = MySQL(app)

def execute_json(query, *args):
    cur = mysql.connection.cursor()
    if args:
        cur.execute(query, tuple(args))
    else:
        cur.execute(query)
    data = cur.fetchall()
    cur.close()
    
    return data

def execute_template(query, *args):
    cur = mysql.connection.cursor()
    if args:
        cur.execute(query, tuple(args))
    else:
        cur.execute(query)
    columns = [col[0] for col in cur.description]
    data = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    
    return data

def commit(query, *args):
   cur = mysql.connection.cursor()
   cur.execute(query, tuple(args))
   cur.commit()
   rows_affected = cur.row_count()
   cur.close()
   
   return rows_affected


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


@app.route("/students", methods=["POST"])
def add_students():
    data = request.get_json()
    firstname = data["firstname"]
    middlename = data["middlename"]
    lastname = data["lastname"]
    birthdate = data["birthdate"]
    gender = data["gender"]
    
    if middlename:
        query = """INSERT INTO students (firstname, middlename, lastname, birthdate, gender) VALUES (%s, %s, %s, %s, %s)"""
        rows = commit(query, firstname, middlename, lastname, birthdate, gender)
    else:       
        query = """INSERT INTO students (firstname, lastname, birthdate, gender) VALUES (%s, %s, %s, %s)"""
        rows = commit(query, firstname, lastname, birthdate, gender)
 
    return make_response(jsonify(
        {"message": "data created successfully", "rows_affected": rows}
        ), 201)

@app.route("/students/<int:idstudents>", methods=["PUT"])
def update_students(idstudents):
    data = request.get_json()
    firstname = data["firstname"]
    middlename = data["middlename"]
    lastname = data["lastname"]
    birthdate = data["birthdate"]
    gender = data["gender"]
    
    if middlename:
        query = """UPDATE students SET firstname=%s, middlename=%s, lastname=%s, birthdate=%s, gender=%s WHERE idstudents=%s"""
        rows = commit(query, firstname, middlename, lastname, birthdate, gender, idstudents)
        
    else:
        query = """UPDATE students SET firstname=%s, lastname=%s, birthdate=%s, gender=%s WHERE idstudents=%s"""
        rows = commit(query, firstname, lastname, birthdate, gender, idstudents)
        
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

@app.route("/teachers", methods=["POST"])
def add_teachers():
    data = request.get_json()
    firstname = data["firstname"]
    middlename = data["middlename"]
    lastname = data["lastname"]
    birthdate = data["birthdate"]
    gender = data["gender"]
    
    if middlename:
        query = """INSERT INTO teachers (firstname, middlename, lastname, birthdate, gender) VALUES (%s, %s, %s, %s, %s)"""
        rows = commit(query, firstname, middlename, lastname, birthdate, gender)
    else:       
        query = """INSERT INTO teachers (firstname, lastname, birthdate, gender) VALUES (%s, %s, %s, %s)"""
        rows = commit(query, firstname, lastname, birthdate, gender)
 
    return make_response(jsonify(
        {"message": "data created successfully", "rows_affected": rows}
        ), 201)

@app.route("/teachers/<int:idteachers>", methods=["PUT"])
def update_teachers(idteachers):
    data = request.get_json()
    firstname = data["firstname"]
    middlename = data["middlename"]
    lastname = data["lastname"]
    birthdate = data["birthdate"]
    gender = data["gender"]
    
    if middlename:
        query = """UPDATE teachers SET firstname=%s, middlename=%s, lastname=%s, birthdate=%s, gender=%s WHERE idteachers=%s"""
        rows = commit(query, firstname, middlename, lastname, birthdate, gender, idteachers)
        
    else:
        query = """UPDATE teachers SET firstname=%s, lastname=%s, birthdate=%s, gender=%s WHERE idteachers=%s"""
        rows = commit(query, firstname, lastname, birthdate, gender, idteachers)
        
    return make_response(jsonify(
        {"message": "data updated successfully", "rows_affected": rows}
        ), 200)
    
@app.route("/teachers/<int:idteachers>", methods=["DELETE"])
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
        return make_response(jsonify({"message": "data not found"}), 404)
    return render_template('class.html', results=jsonify(results), cur_class=cur_class)

@app.route("/classes", methods=["POST"])
def add_classes():
    data = request.get_json()
    description = data["description"]
    idroom = data.get("idroom")  
    idcourse = data.get("idcourse")    
    query = """INSERT INTO classes (description, idroom, idcourse) VALUES (%s, %s, %s, %s, %s)"""
    rows = commit(query, description, idroom, idcourse)
    
    return make_response(jsonify(
        {"message": "data created successfully", "rows_affected": rows}
        ), 201)

@app.route("/classes/<int:idclasses>", methods=["PUT"])
def update_classes(idclasses):
    data = request.get_json()
    description = data["description"]
    idroom = data.get("idroom")  
    idcourse = data.get("idcourse")    
    
    query = """UPDATE classes SET description=%s, idroom=%s, idcourse=%s, WHERE idclasses=%s"""
    rows = commit(query, description, idroom, idcourse, idclasses)
        
    return make_response(jsonify(
        {"message": "data updated successfully", "rows_affected": rows}
        ), 200)
    
@app.route("/classes/<int:idclasses>", methods=["DELETE"])
def delete_classe(idclasses):
    query = """DELETE FROM classes WHERE idclasses=%s"""
    rows = commit(query, idclasses)
        
    return make_response(jsonify(
        {"message": "data deleted successfully", "rows_affected": rows}
        ), 200)   

if __name__ == "__main__":
    app.run(debug=True)
