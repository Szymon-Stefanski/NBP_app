import smtplib
import ssl


def send_email(subject, message):
    host = "smtp.gmail.com"
    port = 465

    username = "python.email12025@gmail.com"
    password = "gsse dvli ihmn lsco"

    receiver = "szymonstefanski1@gmail.com"
    context = ssl.create_default_context()

    email_message = f"Subject: {subject}\nFrom: {username}\nTo: {receiver}\n\n{message}"

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, email_message.encode("utf-8"))
