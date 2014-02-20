#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import argparse
import configparser


class Mailer():
    """ Simple mailer-object. """

    def __init__(self, user, password, server, port=25, ssl=False):
        self.username = user
        self.password = password
        self.server = server
        self.port = port
        self.ssl = ssl

    def send_mail(self, recipient, subject, body):
        """ Sends a custom mail. """

        # create mail-header
        header = "From: {}\r\n".format(self.username) + \
                 "To: {}\r\n".format(recipient) + \
                 "Subject: {}\r\n".format(subject) + \
                 body.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')

        # try to login onto the smtp-server
        try:
            if self.ssl:
                smtp_server = smtplib.SMTP_SSL(self.server, self.port)
            else:
                smtp_server = smtplib.SMTP(self.server, self.port)
            smtp_server.login(self.username, self.password)
            smtp_server.sendmail(self.username, recipient, header)
        # occurs if connection fails
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
        if self.ssl:
            print('SSL: On')
        else:
            print('SSL: Off')


def create_mailer(data):
    """ Create mailer-object based on user's choice to use account or not."""

    # if using account read accounts.ini
    if data['create_by'] == 'account':
        accounts = configparser.ConfigParser()
        accounts.read('accounts.ini')
        # if account is listed in accounts.ini
        if data['account'] in accounts:
            account = accounts[data['account']]
            if not is_valid_account(account): return False
            if account['TLS'] == 'On':
                ssl = True
            else:
                ssl = False
            try:
                return Mailer(account['Username'], account['Password'],
                              account['Server'], int(account['Port']), ssl)
            # occurs if port value from accounts.ini is invalid
            except ValueError:
                print('ERROR: Invalid port for account: ' + data['account'])
                return None
        # if account is not listed in accounts.ini
        else:
            print("ERROR: Invalid account!")
            return None
    # if using script-params (u, p, s)
    elif data['create_by'] == 'input':
        # if no port was set, use 25
        if data['port'] is None:
            port = 25
        else:
            port = data['port']
        return Mailer(data['username'], data['password'], data['server'],
                      port, data['ssl'])


def is_valid_account(account):
    """Check if requested account is valid."""

    # check if basic params from accounts.ini are set and not empty
    try:
        if (
            account['Username'] is not '' and
            account['Password'] is not '' and
            account['Server'] is not '' and
            account['Port'] is not ''
            ):
            return True
    # occurs if any important option is missing
    except KeyError as ke:
        print('ERROR: {} value is missing'.format(ke))
        return False
    print('ERROR: Invalid account')
    return False


if __name__ == '__main__':
    desc = "Mailer3k by Marco <zantekk> K."
    p = argparse.ArgumentParser(description=desc,
                                formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('action', help="testmail: Send a test mail\n" +
                                  "mail: Send mail with custom subject & body")
    p.add_argument('-u', '--user', default=None,
                   help="Username for the SMTP server")
    p.add_argument('-p', '--password', default=None,
                   help="Password for the SMTP server")
    p.add_argument('-s', '--server', default=None,
                   help="SMTP server address")
    p.add_argument('-P', '--port', required=False, type=int, default=None,
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
    p.add_argument('-a', '--account', default=None,
                   help="specify account-name from accounts.ini")

    args = p.parse_args()
    mailer = None

    # if using account
    if (args.user == args.password == args.server == args.port is not None) \
            and args.account is not None:
        mailer = create_mailer({'create_by': 'account',
                                'account': args.account})
    # if using script params (u, p, s)
    elif (args.user and args.password and args.server) is not None \
            and args.account is None:
        mailer = create_mailer({'create_by': 'input',
                                'username': args.user,
                                'password': args.password,
                                'server': args.server,
                                'port': args.port,
                                'ssl': args.ssl})

    # if 'action' is valid
    if mailer and args.action in ('mail', 'testmail'):
        # send custom mail
        if args.action == 'mail':
            mailer.send_mail(recipient=args.to,
                             subject=args.subject,
                             body=args.body)
        # send test-mail
        elif args.action == 'testmail':
            mailer.send_mail(recipient=args.to,
                             subject="Testmail",
                             body=args.body)
    else:
        print("Only one method allow. Pls use account(-a) or manual(-u,-p,-s)")
