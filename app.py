from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta
from temp_share import TempFileShare

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize TempFileShare
temp_share = TempFileShare(
    base_url='https://file-sharing-app-9pbo.onrender.com',
    upload_folder=app.config['UPLOAD_FOLDER']
)

# Mock user database (replace with real database in production)
users = {}
files = []

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username

@login_manager.user_loader
def load_user(username):
    if username not in users:
        return None
    return User(username)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            flash('Username already exists')
            return redirect(url_for('register'))
        
        users[username] = generate_password_hash(password)
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and check_password_hash(users[username], password):
            login_user(User(username))
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', files=files)

def calculate_expiry_time(value, unit):
    if unit == 'never':
        return None
    
    value = int(value)
    if unit == 'minutes':
        return datetime.now() + timedelta(minutes=value)
    elif unit == 'hours':
        return datetime.now() + timedelta(hours=value)
    elif unit == 'days':
        return datetime.now() + timedelta(days=value)
    return datetime.now() + timedelta(minutes=10)  # default 10 minutes

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('dashboard'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('dashboard'))
    
    if file:
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        unique_filename = timestamp + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
        
        # Get expiration time from form
        expiry_value = request.form.get('expiry_value', '10')
        expiry_unit = request.form.get('expiry_unit', 'minutes')
        expiry_time = calculate_expiry_time(expiry_value, expiry_unit)
        
        # Generate temporary share with custom expiration
        share_info = temp_share.generate_share(filename, unique_filename, expiry_time)
        
        files.append({
            'filename': filename,
            'unique_filename': unique_filename,
            'uploaded_by': current_user.username,
            'uploaded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'share_url': share_info['share_url'],
            'qr_path': os.path.basename(share_info['qr_path']),
            'expiry_time': 'Never' if expiry_time is None else expiry_time.strftime('%Y-%m-%d %H:%M:%S')
        })
        
        flash('File uploaded successfully!')
        return redirect(url_for('dashboard'))

@app.route('/download/<unique_filename>')
@login_required
def download_file(unique_filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], unique_filename)

@app.route('/delete/<unique_filename>', methods=['POST'])
@login_required
def delete_file(unique_filename):
    for file in files:
        if file['unique_filename'] == unique_filename:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file['qr_path']))
                files.remove(file)
                flash('File deleted successfully!')
                break
            except OSError:
                flash('Error deleting file')
    return redirect(url_for('dashboard'))

@app.route('/share/<share_id>')
def share_file(share_id):
    file_info = temp_share.get_file_info(share_id)
    if not file_info:
        abort(404)
    
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        os.path.basename(file_info['file_path']),
        download_name=file_info['original_filename']
    )

@app.route('/qr/<filename>')
def serve_qr(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
