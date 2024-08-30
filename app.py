from flask import Flask, render_template, request, flash, redirect
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import os

app = Flask(__name__)
app.secret_key = '9923-shdsadh-12i3uiuasd-dasdas'  # Change this to a secure secret key


# Helper function to send email
def send_email(sender_email, password, recipients, cc, bcc, subject, body, attachments):
    try:
        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ','.join(recipients)
        msg['Cc'] = ','.join(cc)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach files
        for file in attachments:
            part = MIMEApplication(file.read(), Name=file.filename)
            part['Content-Disposition'] = f'attachment; filename="{file.filename}"'
            msg.attach(part)

        # Combine To, Cc, and Bcc recipients
        all_recipients = recipients + cc + bcc
        server.sendmail(sender_email, all_recipients, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(e)
        return False


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sender_email = request.form['sender_email']
        password = request.form['password']
        recipients = request.form['to'].split(',')
        cc = request.form['cc'].split(',') if request.form['cc'] else []
        bcc = request.form['bcc'].split(',') if request.form['bcc'] else []
        subject = request.form['subject']
        body = request.form['body']
        attachments = request.files.getlist('attachments')

        success = send_email(sender_email, password, recipients, cc, bcc, subject, body, attachments)

        if success:
            flash('Emails sent successfully!', 'success')
        else:
            flash('Failed to send emails.', 'danger')

        return redirect('/')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
