import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

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

# 2. Bảng lưu ý kiến học sinh
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

# Tự động tạo bảng database
with app.app_context():
    db.create_all()

# --- CÁC ROUTE ---

# Trang chủ cho học sinh gửi ý kiến
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

# Trang đăng nhập Admin
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lấy mật khẩu từ ô nhập duy nhất trong form
        password = request.form.get('password')
        
        # Sửa mật khẩu ở dòng này nếu muốn đổi mật khẩu khác
        if password == '123456':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Mật khẩu không đúng!')
            
    return render_template('login.html')

# Trang xem danh sách ý kiến (Bảo vệ bằng Session)
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    feedbacks = Feedback.query.all()
    return render_template('dashboard.html', feedbacks=feedbacks)

# Đăng xuất
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
