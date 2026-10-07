import os
from flask import Flask, flash, redirect, render_template, request, url_for
import requests

app = Flask(__name__)
# Secret key cho Flask flash messages
app.secret_key = os.environ.get('SECRET_KEY', 'mat_khau_bao_mat_app_123')

# Danh sách bộ nhớ tạm lưu các góp ý để hiển thị trên Dashboard
FEEDBACK_LIST = []

# =========================================================
# CẤU HÌNH DISCORD WEBHOOK
# =========================================================
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1557372196828221510/pRZ3RH_agMZYf4zLoTss8Dzo4ekEkZ5c7WM6A_yfj0Rhxu-OrC6lktqwxCz2V90Q2e8q'


def send_discord_notification(student_name, student_class, feedback_content):
    """Hàm gửi thông báo trực tiếp về Discord qua Webhook."""
    if not DISCORD_WEBHOOK_URL:
        print('⚠️ Chưa cấu hình link DISCORD_WEBHOOK_URL!')
        return False

    # Khung nội dung gửi sang Discord
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

    # Bổ sung Headers chống bị Discord chặn lỗi 429 (Rate Limit)
    headers = {
        'Content-Type': 'application/
