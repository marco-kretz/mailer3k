mailer3k
========

CLI-Mailer written in Python3

With mailer3k you can send e-mails from the command-line through a given smtp-server.
I tried to keep the usage as simple as possible and I'm still fixing bugs, if you find any
please report it to me!

## Features

* Based on Python3
* No external libs are needed
* Sending blank testmail without specifying subject or body
* Accounting: You can save account data in accounts.ini

## Usage

### Basic

Simple testmail: `mailer3k.py testmail -u username -p password -s smtp.exmaple.com -P 25 --to target@example.com`
Testmail with SSL: `mailer3k.py testmail -u username -p password -s smtp.exmaple.com -P 465 --ssl --to target@example.com`

### Using accounts

Create a file called `accounts.ini` in the script's dir. The file syntax is:
`[accoutname]
User = myuser
Password = mypass
Server = smtp.myserver.com
Port = 465
SSL = On`

Saved accounts can be used like this: `mailer3k.py testmail -a accountname --to target@example.com`
