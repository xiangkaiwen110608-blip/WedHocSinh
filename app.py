import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mat-khau-bao-mat-123'

# 1. Cấu hình cơ sở dữ liệu SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)

db_path = os.path.join(instance_path, 'feedback.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 2. Cấu hình Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 3. Định nghĩa các bảng Database
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 4. Tự động tạo cơ sở dữ liệu & Tài khoản Admin mặc định
with app.app_context():
    db.create_all()
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        new_admin = User(username='admin', password='123456')
        db.session.add(new_admin)
        db.session.commit()

# --- CÁC ĐƯỜNG DẪN (ROUTES) ---

# Trang chủ gửi ý kiến
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            new_feedback = Feedback(content=content)
            db.session.add(new_feedback)
            db.session.commit()
            return render_template('index.html', success=True)
    return render_template('index.html')

# Trang đăng nhập Quản trị viên
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lấy mật khẩu từ ô duy nhất trong form
        password = request.form.get('password')
        
        if password == '123456':
            # Đúng mật khẩu -> chuyển sang trang dashboard
            return redirect(url_for('dashboard'))
        else:
            flash('Tài khoản hoặc mật khẩu không đúng!')
            
    return render_template('login.html')

# Trang quản trị xem ý kiến
@app.route('/dashboard')
@login_required
def dashboard():
    feedbacks = Feedback.query.all()
    return render_template('dashboard.html', feedbacks=feedbacks)

# Đăng xuất
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)