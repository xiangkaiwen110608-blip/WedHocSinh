from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mat_khau_bi_mat_cua_ban_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ykien.db'
db = SQLAlchemy(app)

# Cấu hình Quản lý Đăng nhập Admin
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- 1. TẠO BẢNG DỮ LIỆU ---
class YKien(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ho_ten = db.Column(db.String(100), nullable=False)
    lop = db.Column(db.String(50), nullable=False)
    chu_de = db.Column(db.String(100), nullable=False)
    noi_dung = db.Column(db.Text, nullable=False)
    ngay_gui = db.Column(db.DateTime, default=datetime.now)

class AdminUser(UserMixin):
    id = 1

@login_manager.user_loader
def load_user(user_id):
    if user_id == "1":
        return AdminUser()
    return None

# --- 2. CÁC ĐƯỜNG DẪN (ROUTES) ---

# Trang cho học sinh gửi ý kiến
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ho_ten = request.form.get('ho_ten', 'Ẩn danh')
        lop = request.form.get('lop', 'Không rõ')
        chu_de = request.form.get('chu_de', 'Chung')
        noi_dung = request.form.get('noi_dung')

        new_ykien = YKien(ho_ten=ho_ten, lop=lop, chu_de=chu_de, noi_dung=noi_dung)
        db.session.add(new_ykien)
        db.session.commit()
        
        flash('Cảm ơn bạn! Ý kiến đóng góp đã được gửi thành công.', 'success')
        return redirect(url_for('index'))
    
    return render_template('index.html')

# Trang đăng nhập Admin dành cho bạn
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        # BẠN CÓ THỂ ĐỔI MẬT KHẨU ADMIN Ở DÒNG DƯỚI NÀY (VD: admin123)
        if password == 'admin123':
            user = AdminUser()
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Mật khẩu không chính xác!', 'danger')
    return render_template('login.html')

# Trang Dashboard quản lý ý kiến (Chỉ truy cập được sau khi Đăng nhập)
@app.route('/dashboard')
@login_required
def dashboard():
    danh_sach_y_kien = YKien.query.order_by(YKien.ngay_gui.desc()).all()
    return render_template('dashboard.html', ykien_list=danh_sach_y_kien)

# Lệnh xóa ý kiến
@app.route('/delete/<int:id>')
@login_required
def delete_ykien(id):
    ykien = YKien.query.get_or_404(id)
    db.session.delete(ykien)
    db.session.commit()
    flash('Đã xóa ý kiến!', 'info')
    return redirect(url_for('dashboard'))

# Đăng xuất Admin
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tự tạo file cơ sở dữ liệu ykien.db
    app.run(debug=True, port=5000)