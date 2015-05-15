# A testing program to send a dummy email.

import argparse
import smtplib
from email.mime.text import MIMEText

def real_main():
    parser = argparse.ArgumentParser(description='Send an email.')
    parser.add_argument('--u', dest='username', type=str, help='Username.')
    parser.add_argument('--p', dest='password', type=str, help='Password.')
    parser.add_argument('--r', dest='receiver', type=str, help='Receiver.')

    args = parser.parse_args()

    # Create a text/plain message
    msg = MIMEText('EOM')

    msg['Subject'] = 'This is your cron mail, Sir!'
    msg['From'] = args.username
    msg['To'] = args.receiver

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(args.username, args.password)
    server.sendmail(args.username, [args.receiver], msg.as_string())
    server.quit()


if __name__ == '__main__':
    real_main()
