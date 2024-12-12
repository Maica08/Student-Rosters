from flask import Flask, render_template, jsonify, request, make_response
from flask_mysqldb import MySQL

app = Flask("__name__")
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
    data = cur.fetchall()
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
    return "Home"

@app.route("/students", methods=["GET"])
def get_books():
    query = """SELECT * FROM students"""
    data = execute(query)
    
    if not data:
        return make_response(jsonify({"message": "data not found"}), 404)
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)
