from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Connect to RDS MySQL (you’ll fill this later)
conn = mysql.connector.connect(
    host="ajeet-assignment-1.c8p82wauy4rx.us-east-1.rds.amazonaws.com",
    user="admin",
    password="q1w2e3r4",
    database="studentdb"
)
cursor = conn.cursor(dictionary=True)

@app.route("/students", methods=["GET"])
def get_students():
    cursor.execute("SELECT * FROM students")
    return jsonify(cursor.fetchall())

@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    cursor.execute("INSERT INTO students (name, age, grade) VALUES (%s,%s,%s)", 
                   (data['name'], data['age'], data['grade']))
    conn.commit()
    return jsonify({"message": "Student added"})

@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json()
    cursor.execute("UPDATE students SET name=%s, age=%s, grade=%s WHERE id=%s",
                   (data['name'], data['age'], data['grade'], id))
    conn.commit()
    return jsonify({"message": "Student updated"})

@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    return jsonify({"message": "Student deleted"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

