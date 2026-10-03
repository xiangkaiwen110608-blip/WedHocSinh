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

# 2. Bảng lưu thông tin ý kiến (Bao gồm Tên và Lớp)
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)          # Tên học sinh
    student_class = db.Column(db.String(50), nullable=True) # Lớp
    content = db.Column(db.Text, nullable=False)            # Nội dung

with app.app_context():
    db.create_all()

# --- CÁC ROUTE ---

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        student_class = request.form.get('student_class')
        content = request.form.get('content')
        
        if content and content.strip():
            new_feedback = Feedback(
                name=name.strip() if name else "Ẩn danh",
                student_class=student_class.strip() if student_class else "Không rõ",
                content=content.strip()
            )
            db.session.add(new_feedback)
            db.session.commit()
            return render_template('index.html', success=True)
            
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == '123456':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Mật khẩu không đúng!')
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    feedbacks = Feedback.query.order_by(Feedback.id.desc()).all()
    return render_template('dashboard.html', feedbacks=feedbacks)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)