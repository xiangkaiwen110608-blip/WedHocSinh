import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-123'

# Cấu hình đường dẫn Database SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'feedback.db')
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Định nghĩa bảng lưu ý kiến
# 1. Bảng lưu Ý kiến học sinh
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

# 2. Bảng lưu Tài khoản Admin
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# 3. Khởi tạo dữ liệu & Tài khoản Admin mặc định
with app.app_context():
    db.create_all()
    # Kiểm tra xem tài khoản admin đã tồn tại chưa
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        new_admin = User(username='admin', password='110608wen@')
        db.session.add(new_admin)
        db.session.commit()
    db.create_all()

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

if __name__ == '__main__':
    app.run(debug=True)