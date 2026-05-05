from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, email TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM students')
    students = cur.fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    age = request.form.get('age')
    email = request.form.get('email')
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO students (name, age, email) VALUES (?, ?, ?)', (name, age, email))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM students WHERE id=?', (id,))
    student = cur.fetchone()
    conn.close()
    return render_template('edit.html', student=student)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form.get('name')
    age = request.form.get('age')
    email = request.form.get('email')
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('UPDATE students SET name=?, age=?, email=? WHERE id=?', (name, age, email, id))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM students WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)