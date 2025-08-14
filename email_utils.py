import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_TO = os.getenv("EMAIL_TO") or SMTP_USER
EMAIL_FROM = os.getenv("EMAIL_FROM") or SMTP_USER

def send_email(subject: str, body_html: str, ics_content: str | None = None, ics_filename: str = "evento.ics"):
    if not (SMTP_HOST and SMTP_PORT and SMTP_USER and SMTP_PASS):
        raise RuntimeError("Faltan variables SMTP_HOST/SMTP_PORT/SMTP_USER/SMTP_PASS")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    msg.attach(MIMEText(body_html, "html", "utf-8"))

    if ics_content:
        part = MIMEApplication(ics_content.encode("utf-8"), Name=ics_filename)
        part["Content-Disposition"] = f'attachment; filename="{ics_filename}"'
        part.add_header("Content-Type", "text/calendar; method=REQUEST; charset=UTF-8")
        msg.attach(part)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
