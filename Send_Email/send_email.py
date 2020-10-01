"""
Using this simple script you can send emails to anyone from your email adress.
To start first go to 
https://myaccount.google.com/lesssecureapps
And allow resources. This will let your script interact with gmail.

next run the following in your terminal:
pip install secure-smtplib

"""




import smtplib

import configs


def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(configs.EMAIL_ADDRESS, configs.PASSWORD)
        message = f'Subject: {subject}\n\n{msg}'
        server.sendmail(configs.EMAIL_ADDRESS, configs.EMAIL_ADDRESS, message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")


subject = "Replace with your subject"
msg = "Hello there, how are you today?"

send_email(subject, msg)