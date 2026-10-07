import os
from flask import Flask, flash, redirect, render_template, request, url_for
import requests

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'mat_khau_bao_mat_app_123')

# Danh sách bộ nhớ tạm lưu các góp ý gửi về
FEEDBACK_LIST = []

# =========================================================
# CẤU HÌNH DISCORD WEBHOOK (DÁN LINK MỚI VÀO DÒNG DƯỚI)
# =========================================================
DISCORD_WEBHOOK_URL = 'DÁN_LINK_WEBHOOK_MỚI_CỦA_BẠN_VÀO_ĐÂY'


def send_discord_notification(student_name, student_class, feedback_content):
    """Hàm gửi thông báo trực tiếp về Discord qua Webhook."""
    if not DISCORD_WEBHOOK_URL or 'DÁN_LINK' in DISCORD_WEBHOOK_URL:
        print('⚠️ CHƯA DÁN LINK WEBHOOK DISCORD THẬT!')
        return False

    payload = {
        'embeds': [{
            'title': '📩 GÓP Ý MỚI TỪ HỌC SINH',
            'color': 3447003,
            'fields': [
                {'name': '👤 Họ và tên', 'value': student_name, 'inline': True},
                {'name': '🏫 Lớp', 'value': student_class, 'inline': True},
                {
                    'name': '📝 Nội dung góp ý',
                    'value': feedback_content,
                    'inline': False,
                },
            ],
            'footer': {'text': 'Hệ thống phản hồi WedHocSinh'},
        }]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        print(f'➡️ Discord API Status Code: {response.status_code}')
        if response.status_code not in [200, 204]:
            print(f'❌ Discord Response Error: {response.text}')
        return response.status_code in [200, 204]
    except Exception as e:
        print(f'❌ Ngoại lệ khi gửi Discord: {e}')
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
    student_class = request.form.get('student_class', 'Không rõ').strip() or 'Không rõ'
    feedback_content = request.form.get('feedback', '').strip()

    if not feedback_content:
        flash('Vui lòng nhập nội dung góp ý!', 'danger')
        return redirect(url_for('home'))

    # Lưu vào danh sách Dashboard
    FEEDBACK_LIST.append({
        'name': student_name,
        'student_class': student_class,
        'content': feedback_content
    })

    # Gửi tin nhắn sang Discord
    send_discord_notification(student_name, student_class, feedback_content)

    flash('Cảm ơn bạn đã gửi góp ý! Ý kiến của bạn đã được ghi nhận.', 'success')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == 'admin123':
            return redirect(url_for('dashboard'))
        else:
            flash('Mật khẩu không đúng!', 'danger')

    return render_template('login.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', feedbacks=FEEDBACK_LIST)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
