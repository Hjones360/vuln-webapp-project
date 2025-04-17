from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

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
    error = None
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']

        # Empty field check
        if not username or not email or not password:
            error = "All fields are required."
            return render_template('register.html', error=error)

        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            # Check if user already exists
            c.execute('SELECT * FROM users WHERE username=? OR email=?', (username, email))
            existing_user = c.fetchone()
            if existing_user:
                error = "Username or email already exists."
                return render_template('register.html', error=error)

            # If all is good, hash password and create account
            from werkzeug.security import generate_password_hash
            password = generate_password_hash(password)
            c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                      (username, email, password))
            conn.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        # Blank input check
        if not username or not password:
            error = "Username and password are required."
            return render_template('login.html', error=error)

        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE username=?', (username,))
            user = c.fetchone()

            from werkzeug.security import check_password_hash
            if user and check_password_hash(user[3], password):
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['email'] = user[2]
                return redirect(url_for('profile'))
            else:
                error = "Invalid username or password."
    return render_template('login.html', error=error)


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
        new_password = generate_password_hash(request.form['new_password'])
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

    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    file = request.files['file']
    error = None

    if not file:
        error = "No file uploaded."
    else:
        filename = file.filename
        # Check for allowed file extensions
        if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            error = "Invalid file type. Only images are allowed."
        else:
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                c.execute('INSERT INTO uploads (user_id, filename) VALUES (?, ?)',
                          (session['user_id'], filename))
                conn.commit()
            return redirect(url_for('gallery'))

    return render_template('profile.html', username=session['username'], email=session['email'], error=error)

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

