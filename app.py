from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
import sqlite3

app = Flask(__name__, template_folder='templates')
app.secret_key = 'secretkey'  # Insecure, for learning only

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- Database Setup ---
def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                email TEXT,
                password TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                content TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                filename TEXT
            )
        ''')
        conn.commit()

init_db()

# --- Routes ---

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('profile'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                      (username, email, password))
            conn.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
            user = c.fetchone()
            if user:
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['email'] = user[2]
                return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html', username=session['username'], email=session['email'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_password = request.form['new_password']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('UPDATE users SET password=? WHERE id=?', (new_password, session['user_id']))
            conn.commit()
        return redirect(url_for('profile'))
    return render_template('change_password.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    file = request.files['file']
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO uploads (user_id, filename) VALUES (?, ?)',
                      (session['user_id'], file.filename))
            conn.commit()
    return redirect(url_for('gallery'))

@app.route('/gallery')
def gallery():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT filename FROM uploads WHERE user_id=?', (session['user_id'],))
        files = c.fetchall()
    return render_template('gallery.html', files=files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        content = request.form['content']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO posts (user_id, content) VALUES (?, ?)',
                      (session['user_id'], content))
            conn.commit()
        return redirect(url_for('profile'))
    return render_template('create_post.html')

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('profile'))
    return render_template('index.html')
