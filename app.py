import os
from flask import Flask, flash, redirect, render_template, request, url_for
import requests

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'mat_khau_bao_mat_app_123')

# =========================================================
# CẤU HÌNH DISCORD WEBHOOK
# =========================================================
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1557380096342495325/jjBk2sjl9JdA85d6bECoFFGrfanCz8bFI6-RA39k5-QJlEvlpnK7lkr59r6-6SriP3tt'


def send_discord_notification(student_name, student_class, feedback_content):
  """Hàm gửi thông báo trực tiếp về Discord qua Webhook."""
  if not DISCORD_WEBHOOK_URL:
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
    return response.status_code in [200, 204]
  except Exception as e:
    print(f'Lỗi Discord: {e}')
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

  # Gửi tin nhắn sang Discord
  send_discord_notification(student_name, student_class, feedback_content)

  flash('Cảm ơn bạn đã gửi góp ý! Ý kiến của bạn đã được ghi nhận.', 'success')
  return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    password = request.form.get('password', '')
    # Mật khẩu admin hiện tại là: admin123
    if password == 'admin123':
      flash('Đăng nhập thành công!', 'success')
      return redirect(url_for('home'))
    else:
      flash('Mật khẩu không đúng!', 'danger')

  return render_template('login.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
