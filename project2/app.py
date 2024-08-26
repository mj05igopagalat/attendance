from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="lab_attendance"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    student_number = request.form['student_number']

    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT id FROM students WHERE student_number = %s", (student_number,))
    student = cursor.fetchone()
    
    if student:
        student_id = student['id']
        
        cursor.execute(
            "INSERT INTO attendance (student_id, attendance_date) VALUES (%s, %s)",
            (student_id, datetime.now().date())
        )
        db.commit()

        return "Attendance recorded!"
    else:
        return "Student not found!", 404

if __name__ == "__main__":
    app.run(debug=True)

