import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


class EmailNotifier:
    def __init__(self, smtp_host, smtp_port, email_address, app_password, default_to=None, default_cc=None):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.email_address = email_address
        self.app_password = app_password
        self.default_to = default_to or [email_address]
        self.default_cc = default_cc or []

    def send(self, subject, text_body, html_body=None, to=None, cc=None):
        to = to or self.default_to or []
        cc = cc or []
        if isinstance(to, str):
            to = [to]
        if isinstance(cc, str):
            cc = [cc]

        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = self.email_address
        msg['To'] = ", ".join(to)
        if cc:
            msg['Cc'] = ", ".join(cc)

        msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
        if html_body:
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))

        recipients = to + cc

        with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
            server.login(self.email_address, self.app_password)
            server.sendmail(self.email_address, recipients, msg.as_string())

    def send_link_notification(self, filename, base_url="https://podvi.ru/n8n/", to=None, cc=None):
        subject = f"{filename} обработан"
        link = f"{base_url}{filename}"

        html_body = f"""
        <html>
        <body>
            <p>Файл обработан:</p>
            <p><a href="{link}">{link}</a></p>
        </body>
        </html>
        """

        self.send(
            subject=subject,
            text_body=link,
            html_body=html_body,
            to=to,
            cc=cc
        )