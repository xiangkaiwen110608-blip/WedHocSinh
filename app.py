import os
from flask import Flask, flash, redirect, render_template, request, url_for
import requests

app = Flask(__name__)
# Secret key bảo mật cho Flask Flash Messages
app.secret_key = os.environ.get('SECRET_KEY', 'mat_khau_bao_mat_app_123')

# Danh sách bộ nhớ tạm hỗ trợ hiển thị ngay trên Dashboard
FEEDBACK_LIST = []

# =========================================================
# CẤU HÌNH GOOGLE SHEETS WEBHOOK
# =========================================================
GOOGLE_SHEET_WEBHOOK_URL = (
    'https://script.google.com/macros/s/AKfycbxWpKLsWWEkneSd1pMNeqFXAyKGpb1Y6UT9S2Utrc7mJUBuiau6rhB-uU3bGulY5fXD/exec'
)


def send_to_google_sheets(student_name, student_class, feedback_content):
    """Hàm tự động ghi dữ liệu góp ý vào Google Sheets vĩnh viễn."""
    if not GOOGLE_SHEET_WEBHOOK_URL or 'DÁN_LINK' in GOOGLE_SHEET_WEBHOOK_URL:
        print('⚠️ Chưa cấu hình GOOGLE_SHEET_WEBHOOK_URL!')
        return False

    payload = {
        'name': student_name,
        'student_class': student_class,
        'content': feedback_content,
    }

    try:
        # Gửi dữ liệu dạng JSON sang Google Apps Script
        response = requests.post(GOOGLE_SHEET_WEBHOOK_URL, json=payload, timeout=8)
        print(f'➡️ Google Sheets API Status Code: {response.status_code}')
        if response.status_code == 200:
            print('✅ Đã ghi thành công vào Google Sheets!')
            return True
        else:
            print(f'❌ Lỗi từ Google Sheets API: {response.text}')
            return False
    except Exception as e:
        print(f'❌ Lỗi kết nối Google Sheets: {e}')
        return False


# =========================================================
# CÁC ROUTE TRANG WEB
# =========================================================


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    student_name = request.form.get('name', 'Ẩn danh').strip() or 'Ẩn danh'
    student_class = (
        request.form.get('student_class', 'Không rõ').strip() or 'Không rõ'
    )
    feedback_content = request.form.get('feedback', '').strip()

    if not feedback_content:
        flash('Vui lòng nhập nội dung góp ý!', 'danger')
        return redirect(url_for('home'))

    # 1. Lưu tạm thời để xem ngay trên Dashboard hiện tại
    FEEDBACK_LIST.append({
        'name': student_name,
        'student_class': student_class,
        'content': feedback_content,
    })

    # 2. Ghi vĩnh viễn vào Google Sheets
    send_to_google_sheets(student_name, student_class, feedback_content)

    # 3. Chuyển hướng sang giao diện thông báo gửi thành công
    return render_template('success.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == '11060811@':
            return redirect(url_for('dashboard'))
        else:
            flash('Mật khẩu không đúng!', 'danger')

    return render_template('login.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', feedbacks=FEEDBACK_LIST)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
