from django.conf import settings
from django.core.mail import send_mail


def send_email(subject, message, to_email):
    to_email = to_email if isinstance(to_email, list) else [to_email, ]

    send_mail(
        subject,
        message,  # ✅ 일반 텍스트 메시지로 전송
        settings.EMAIL_HOST_USER,  # ✅ 네이버 이메일 계정 사용
        to_email,
        fail_silently=False,
        html_message=None  # ✅ HTML 메시지 비활성화
    )