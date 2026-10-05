import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Mã khóa session
app.config['SECRET_KEY'] = 'mat-khau-bao-mat-123'

# 1. Cấu hình cơ sở dữ liệu SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)

db_path = os.path.join(instance_path, 'feedback.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 2. Bảng lưu ý kiến đóng góp của học sinh
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

# Tự động tạo cơ sở dữ liệu khi khởi chạy
with app.app_context():
    db.create_all()

# --- CÁC ROUTE XỬ LÝ ---

# Trang chủ: Học sinh gửi ý kiến
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Lấy nội dung từ ô nhập liệu có name="content"
        content = request.form.get('content')
        if content and content.strip():
            new_feedback = Feedback(content=content.strip())
            db.session.add(new_feedback)
            db.session.commit()
            return render_template('index.html', success=True)
    return render_template('index.html')

# Trang Đăng nhập Admin
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lấy mật khẩu nhập vào
        password = request.form.get('password')
        
        # Mật khẩu đăng nhập mặc định là 123456
        if password == '110608':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Mật khẩu không đúng!')
            
    return render_template('login.html')

# Trang Dashboard: Xem danh sách ý kiến
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    feedbacks = Feedback.query.order_by(Feedback.id.desc()).all()
    return render_template('dashboard.html', feedbacks=feedbacks)

# Đăng xuất Quản trị viên
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
