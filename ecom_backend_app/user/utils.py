# utils.py
import random
import traceback
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):
  try:
    subject = "Your Verification Code"

    text_content = f"Your OTP is {otp}. It expires in 10 minutes."

    html_content = f"""
<div style="font-family:Arial, sans-serif;background:#0b1220;padding:40px;">

  <div style="max-width:520px;margin:auto;background:#111827;
              padding:30px;border-radius:16px;
              border:1px solid #1f2937;">

    <!-- Header -->
    <div style="text-align:center;margin-bottom:25px;">
      <h2 style="color:#22d3ee;margin:0;font-size:22px;">
        Security Verification
      </h2>
      <p style="color:#9ca3af;font-size:13px;margin-top:6px;">
        Password Reset OTP
      </p>
    </div>

    <!-- Body -->
    <p style="color:#e5e7eb;font-size:14px;line-height:1.6;">
      Hi there,
    </p>

    <p style="color:#d1d5db;font-size:14px;line-height:1.6;">
      We received a request to reset your password. Use the verification code below to proceed.
    </p>

    <!-- OTP Box -->
    <div style="text-align:center;margin:30px 0;">
      <div style="display:inline-block;
                  padding:16px 28px;
                  font-size:26px;
                  letter-spacing:8px;
                  font-weight:bold;
                  background:#0f172a;
                  border:1px solid #334155;
                  border-radius:12px;
                  color:#22d3ee;">
        {otp}
      </div>
    </div>

    <!-- Warning -->
    <div style="background:#1f2937;
                padding:12px 14px;
                border-radius:10px;
                margin-bottom:20px;">
      <p style="color:#fbbf24;font-size:13px;margin:0;">
        ⚠ This code will expire in <b>5 minutes</b>
      </p>
    </div>

    <!-- Safety Note -->
    <p style="color:#9ca3af;font-size:12px;line-height:1.5;">
      If you did not request this, you can safely ignore this email.
      Do not share this code with anyone.
    </p>

    <!-- Footer -->
    <hr style="border:0;border-top:1px solid #1f2937;margin:25px 0;"/>

    <p style="color:#6b7280;font-size:12px;text-align:center;">
      © Your App Team • Secure Authentication System
    </p>

  </div>
</div>
"""

    email_msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )

    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()
    
  except Exception as e:
        print(" OTP EMAIL ERROR:", str(e))
        print(traceback.format_exc())
        raise e