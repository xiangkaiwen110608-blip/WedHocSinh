import os
from flask import Flask, flash, redirect, render_template, request, url_for
import requests

app = Flask(__name__)
# Secret key cho Flask flash messages
app.secret_key = os.environ.get('SECRET_KEY', 'bi_mat_khong_the_bat_mi_12345')

# =========================================================
# CẤU HÌNH DISCORD WEBHOOK
# (Dán link Webhook bạn lấy từ Cài đặt kênh Discord vào đây)
# =========================================================
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1557372196828221510/pRZ3RH_agMZYf4zLoTss8Dzo4ekEkZ5c7WM6A_yfj0Rhxu-OrC6lktqwxCz2V90Q2e8q'


def send_discord_notification(student_name, student_class, feedback_content):
  """Hàm gửi thông báo góp ý trực tiếp về kênh Discord qua Webhook."""
  if (
      not DISCORD_WEBHOOK_URL
      or DISCORD_WEBHOOK_URL == 'https://discord.com/api/webhooks/1557372196828221510/pRZ3RH_agMZYf4zLoTss8Dzo4ekEkZ5c7WM6A_yfj0Rhxu-OrC6lktqwxCz2V90Q2e8q'
  ):
    print('⚠️ Chưa cấu hình link DISCORD_WEBHOOK_URL!')
    return False

  # Tạo khung nội dung tin nhắn gửi sang Discord
  payload = {
      'embeds': [{
          'title': '📩 GÓP Ý MỚI TỪ HỌC SINH',
          'color': 3447003,  # Màu xanh lam
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
    if response.status_code in [200, 204]:
      print('✅ Đã gửi thành công nhóa')
      return True
    else:
      print(
          f'❌ Lỗi gửi Discord. Status: {response.status_code}, Response:'
          f' {response.text}'
      )
      return False
  except Exception as e:
    print(f'❌ Ngoại lệ khi gửi Discord: {e}')
    return False


# =========================================================
# CÁC ROUTE XỬ LÝ CỦA FLASK
# =========================================================


@app.route('/', methods=['GET'])
def home():
  return render_template('index.html')


@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
  # Lấy thông tin từ form HTML (Lấy linh hoạt các tên biến khác nhau)
  student_name = request.form.get('name', 'Ẩn danh').strip()
  if not student_name:
    student_name = 'Ẩn danh'

  student_class = request.form.get('student_class', 'Không rõ').strip()
  if not student_class:
    student_class = 'Không rõ'

  # Nhận nội dung góp ý từ ô 'feedback' hoặc 'content'
  feedback_content = request.form.get('feedback') or request.form.get(
      'content', ''
  )

  # Kiểm tra nội dung rỗng
  if not feedback_content.strip():
    flash('Vui lòng nhập nội dung góp ý!', 'danger')
    return redirect(url_for('home'))

  # Gửi tin nhắn sang Discord
  send_discord_notification(student_name, student_class, feedback_content)

  # Thông báo thành công và chuyển hướng về trang chủ
  flash('Cảm ơn bạn đã gửi góp ý! Ý kiến của bạn đã được ghi nhận.', 'success')
  return redirect(url_for('home'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
