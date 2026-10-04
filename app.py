import os
from flask import Flask, flash, redirect, render_template, request, url_for
import requests

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key_12345')

# =========================================================
# THÔNG TIN CẤU HÌNH FACEBOOK MESSENGER API
# =========================================================
# Dán mã Page Access Token lấy từ Graph API Explorer vào đây:
FB_PAGE_ACCESS_TOKEN = 'EAAgtKvdEvLABSjc74X2cLNZAZBQXJ6Ob17nqGg1ArKLkslH9qa0iJ5fJZAZCeQpHzLYgqumNVh2q1fdFRaNdtZBP8PdxyDPCvWoX9rgk7vN72gTVE3VuxajEh3GgN19UGM1atI7GYtHjjUlY3HsrZByuCjcMiOuXWLZBsXTttak4r6ZCdzSOHdnKmyCWtNMDpz4LCgFUXLgjk13MPJiZBPJQzBNVvvPSW6QC9'

# Dán dãy số Facebook ID cá nhân của bạn vào đây (Lấy từ lookup-id.com):
FB_RECIPIENT_ID = '61576796062680'


def send_facebook_message(message_text):
  """Hàm gửi tin nhắn tự động đến Facebook Messenger cá nhân qua Graph API."""
  url = f'https://graph.facebook.com/v19.0/me/messages?access_token={FB_PAGE_ACCESS_TOKEN}'
  payload = {
      'recipient': {'id': FB_RECIPIENT_ID},
      'message': {'text': message_text},
  }
  headers = {'Content-Type': 'application/json'}

  try:
    response = requests.post(url, json=payload, headers=headers)
    res_data = response.json()
    if response.status_code == 200:
      print('✅ Đã gửi thông báo đến Messenger thành công!')
    else:
      print('❌ Lỗi khi gửi tin nhắn Facebook:', res_data)
    return res_data
  except Exception as e:
    print('❌ Ngoại lệ xảy ra khi gửi tin nhắn:', e)
    return None


# =========================================================
# CÁC ROUTE CỦA ỨNG DỤNG FLASK
# =========================================================


@app.route('/')
def home():
  """Trang chủ hiển thị form góp ý dành cho học sinh."""
  return render_template('index.html')


@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
  """Xử lý dữ liệu form góp ý và gửi thông báo qua Messenger."""
  student_name = request.form.get('name', 'Ẩn danh').strip()
  student_class = request.form.get('student_class', 'Không rõ').strip()
  feedback_content = request.form.get('feedback', '').strip()

  if not feedback_content:
    flash('Vui lòng nhập nội dung góp ý!', 'danger')
    return redirect(url_for('home'))

  # Tạo nội dung tin nhắn gửi về Facebook Messenger
  notification_msg = (
      f"📩 CÓ GÓP Ý MỚI TỪ HỌC SINH!\n"
      f"-------------------------------\n"
      f"👤 Họ và tên: {student_name}\n"
      f"🏫 Lớp: {student_class}\n"
      f"💬 Nội dung: {feedback_content}\n"
      f"-------------------------------"
  )

  # Gửi tin nhắn đến Messenger của bạn
  send_facebook_message(notification_msg)

  flash('Cảm ơn bạn đã gửi góp ý! Ý kiến của bạn đã được ghi nhận.', 'success')
  return redirect(url_for('home'))


if __name__ == '__main__':
  # Chạy ứng dụng Flask ở chế độ Debug khi kiểm tra ở máy cục bộ
  app.run(host='0.0.0.0', port=5000, debug=True)
