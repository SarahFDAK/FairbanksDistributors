@ -1,90 +0,0 @@
import imaplib
import smtplib
from smtplib import SMTP
import logging
import email
import email.utils
from email.contentmanager import ContentManager
from email.message import EmailMessage
from datetime import datetime, timezone
from pathlib import Path
import configparser
import os
import time



def get_imap_config():
    config = configparser.ConfigParser()
    config.read('credentials.cfg')
    return config


def get_server():
    config = get_imap_config()
    server = imaplib.IMAP4_SSL('imap.gmail.com')
    typ, login_message = server.login(config['CREDS']['email'],
                                      config['CREDS']['pass'])
    if typ.lower() != 'ok':
        raise Exception("Exception")

    return server


def scrape_inbox():
    server = get_server()
    server.select('inbox')
    emails = server.search(None, '(FROM "fdist.smtp@gmail.com" NOT SUBJECT "Test")')
    ids = emails[1][0]
    ids = list((ids.decode()).split(' '))
    if ids == ['']:
        return

    content_manager = ContentManager()

    for id in ids:
        typ, data = server.fetch(id, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        timestamp = email.utils.parsedate_to_datetime(msg['Date'])
        current = datetime.now(timezone.utc)
        timeDiff = (current - timestamp).total_seconds()
        print (timeDiff)
        if timeDiff > 60:
            config = get_imap_config()
            s = smtplib.SMTP_SSL('smtp.gmail.com')
            s.connect("smtp.gmail.com")
            s.ehlo()
            s.login(config['CREDS']['email'],
                    config['CREDS']['pass'])
            s.sendmail('orders.fbxdist@gmail.com','sarah.c@fdak.net', 'Subject: Inbox scrape hanging')
            {}
            s.quit()


def make_log_dir(log_dir):
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)


def log_error(error, log_dir):
    log_file = f"{log_dir}\\{datetime.now().strftime('%x_%H')}.log"
    log_file = log_file.replace('/', '-')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fileh = logging.FileHandler(log_file, 'a')
    formatter = logging.Formatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s')
    fileh.setFormatter(formatter)
    logger.handlers = [fileh]
    logger.exception(error)


if __name__ == "__main__":
    log_dir = ".\\logs"
    make_log_dir(log_dir)
    while(True):
        try:
            scrape_inbox()
        except Exception as e:
            log_error(e, log_dir)
        time.sleep(60)
