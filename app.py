from flask import Flask, render_template, jsonify, request, make_response
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "student_roster_db"
mysql = MySQL(app)

def execute(query, *args):
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
    
    results = execute(query)
    return render_template('index.html', results=results)

@app.route("/students", methods=["GET"])
def get_students():
    query = """SELECT * FROM students ORDER BY firstname"""
    results = execute(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return render_template('students.html', results=results)

@app.route("/teachers", methods=["GET"])
def get_teachers():
    query = """SELECT * FROM teachers ORDER BY firstname"""
    results = execute(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return render_template('teachers.html', results=results)

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
    results = execute(query)
    
    if not results:
        return make_response(jsonify({"message": "data not found"}), 404)
    return render_template('classes.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
