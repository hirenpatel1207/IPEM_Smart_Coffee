"""
Date: 18/01/2020
Brief:The file handles email utilities.
      Which can be used to send an email when coffee is about to get empty
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendEmail(outputPrediction):

    if outputPrediction == 2:
        # Send email as coffee full
        mail_content = '''Hello,
            This is an update of your coffee machine.
            The coffee in your coffee machine is full. 
            Thank You
            '''

    elif outputPrediction == 1:
        # Send email as coffee level ok
        mail_content = '''Hello,
            This is an update of your coffee machine. 
            The coffee in your coffee machine is ok. 
            Thank You
            '''
    else:
        # Send email as coffee level critical
        mail_content = '''Hello,
            This is an update of your coffee machine. 
            The coffee in your coffee machine is almost empty.
            You have about 5 coffees left until empty.
            Thank You
            '''

    # !!!!!!!! The mail addresses and password !!!!!!!!!!
    sender_address = 'hirenpatel0794@gmail.com'
    sender_pass = 'Ra@9594252463'
    receiver_address = 'hirenpatel1207@gmail.com'

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Status of Coffee Machine'  # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent to  ' + receiver_address + '  from '+sender_address)

    pass
