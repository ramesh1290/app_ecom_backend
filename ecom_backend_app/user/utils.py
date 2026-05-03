import os
import random
import traceback
import resend


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):
    try:
        resend.api_key = os.getenv("RESEND_API_KEY")

        if not resend.api_key:
            raise Exception("RESEND_API_KEY is missing")

        html_content = f"""
        <div style="font-family:Arial,sans-serif;background:#0b1220;padding:40px;">
          <div style="max-width:520px;margin:auto;background:#111827;
                      padding:30px;border-radius:16px;border:1px solid #1f2937;">
            <h2 style="color:#22d3ee;text-align:center;">Security Verification</h2>
            <p style="color:#e5e7eb;">Your OTP is:</p>

            <div style="text-align:center;margin:20px 0;
                        font-size:28px;letter-spacing:8px;color:#22d3ee;">
              {otp}
            </div>

            <p style="color:#9ca3af;font-size:12px;text-align:center;">
              This code expires in 5 minutes
            </p>
          </div>
        </div>
        """

        response = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": [email],
            "subject": "Your OTP Code",
            "html": html_content,
        })

        print("RESEND SUCCESS:", response)

    except Exception as e:
        print("OTP EMAIL ERROR:", str(e))
        print(traceback.format_exc())
        raise e