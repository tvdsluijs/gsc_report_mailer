import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_email(html_content, attachment_path, config, receiver_email):
    msg = MIMEMultipart()
    msg['From'] = config["SENDER_EMAIL"]
    msg['To'] = receiver_email
    msg['Subject'] = 'Google Search Console Rapport'

    msg.attach(MIMEText(html_content, 'html'))

    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename="comparison_chart.png"'
        )
        msg.attach(part)

    with smtplib.SMTP(config["SMTP_SERVER"], config["SMTP_PORT"]) as server:
        server.starttls()
        server.login(config["SENDER_EMAIL"], config["SENDER_PASSWORD"])
        server.sendmail(config["SENDER_EMAIL"], receiver_email, msg.as_string())
