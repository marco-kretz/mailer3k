#!/usr/bin/env python3

import smtplib
import argparse


class Mailer():

    def __init__(self, username, password, server, port=25, ssl=False):
        self.username = username
        self.password = password
        self.server = server
        self.port = port
        self.ssl = ssl

    def send_mail(self, recipient, subject, body):
        header = "From: {}\r\n".format(self.username) + \
                 "To: {}\r\n".format(recipient) + \
                 "Subject: {}\r\n".format(subject) + \
                 body

        try:
            if self.ssl:
                smtp_server = smtplib.SMTP_SSL(self.server, self.port)
            else:
                smtp_server = smtplib.SMTP(self.server, self.port)
            smtp_server.login(self.username, self.password)
            smtp_server.sendmail(self.username, recipient, header)
        except Exception as e:
            print('ERROR: {}'.format(e))
        else:
            print('Mail has successfully been sent.')

    def print_info(self):
        print('SERVER INFORMATION')
        print('------------------')
        print('Server: {}'.format(self.server))
        print('Port: {}'.format(self.port))
        print('Username: {}'.format(self.username))
        print('Password: {}'.format(self.password))
        if self.ssl: print('SSL: On')
        else: print('SSL: Off')


if __name__ == '__main__':
    desc = "Mailer3k by Marco <zantekk> K."
    p = argparse.ArgumentParser(description=desc,
                                formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('action', help="testmail: Send a test mail\n" + \
                                  "mail: Send mail with custom subject & body")
    p.add_argument('-u', '--user', required=True,
                        help="Username for the SMTP server")
    p.add_argument('-p', '--password', required=True,
                        help="Password for the SMTP server")
    p.add_argument('-s', '--server', required=True,
                        help="SMTP server address")
    p.add_argument('-P', '--port', required=False, type=int, default=25,
                        help="SMTP server port (default: 25)")
    p.add_argument('--ssl', required=False, action="store_true",
                        help="Turn SSL on (default: off)", default=False)
    p.add_argument('-t', '--to', required=True,
                        help="The recipient's address")
    p.add_argument('--subject', default='',
                   help="Subject for action: mail (default: empty)")
    p.add_argument('--body', default='',
                        help="Body for action: mail (default: empty)")
    p.add_argument('-v', '--verbosity', action="count", default=0,
                   help="Set verbosity-level [1-2]")

    args = p.parse_args()

    mailer = Mailer(args.user, args.password, args.server, args.port, args.ssl)
    if args.action in ('testmail', 'mail'):
        if args.verbosity >= 1:
            if args.verbosity == 2:
                mailer.print_info()
                print('')
            print('MAIL INFORMATION')
            print('----------------')
            print("Recipient: {}".format(args.to))
            if args.action == 'testmail': print("Subject: Testmail")
            else: print("Subject: {}".format(args.subject))
            print("Body: \n")
        if args.action == 'testmail':
            mailer.send_mail(args.to, subject='Testmail', body='')
        elif args.action == 'mail':
            mailer.send_mail(args.to, subject=args.subject, body=args.body)
    else:
        print("ERR: Invalid action: " + args.action)
