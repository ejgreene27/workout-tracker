from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = 'userdata.db'

# Create table if not exists
def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS workouts (
                    id INTEGER PRIMARY KEY,
                    day TEXT,
                    exercise TEXT,
                    sets INTEGER,
                    reps INTEGER,
                    weight INTEGER
                )''')
    conn.commit()
    conn.close()

create_table()

@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/add_workout', methods=['POST'])
def add_workout():
    if request.method == 'POST':
        day = request.form['day']
        exercise = request.form['exercise']
        sets = request.form['sets']
        reps = request.form['reps']
        weight = request.form['weight']

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO workouts (day, exercise, sets, reps, weight) VALUES (?, ?, ?, ?, ?)", (day, exercise, sets, reps, weight))
        conn.commit()
        conn.close()

        return redirect(url_for('workouts'))

@app.route('/workouts')
def workouts():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM workouts ORDER BY id DESC")  # Fetch workouts in descending order of id (latest first)
    workouts = c.fetchall()
    conn.close()

    return render_template('workouts.html', workouts=workouts)

if __name__ == '__main__':
    app.run(debug=True)

