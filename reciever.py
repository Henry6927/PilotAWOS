import imaplib
import email
import time
from bs4 import BeautifulSoup
import scraperab
import sender
import os

def latest():
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        mail.login(os.environ['WeatherEmail'], os.environ['WeatherPassword']) #logs in
        mail.select('inbox')
        _, data = mail.search(None, 'FROM ' + str(os.environ['WeatherPhone'])) #gets all mail ids that are from email using "weatherphone" --> inorder to get text feature working you must put text email, ie. +19803585198@tmomail.com 
        mail_ids = data[0].split()
        latest_email_id = mail_ids[-1] #gets most recent mail id
        _, msg_data = mail.fetch(latest_email_id, '(RFC822)') 
        return msg_data

def process(msg_data):
    for response_part in msg_data: #used for incase I want to add feature to run multiple messages at once
            if isinstance(response_part, tuple) and isinstance(response_part[1], bytes):
                msg = email.message_from_bytes(response_part[1]) 
                if msg.is_multipart():
                        for part in msg.walk():
                            if part.get('Content-Disposition'):
                                body = part.get_payload(decode=True)
                                body = body.decode('utf-8', 'ignore')
                                if 'ICAO:' in body:
                                    return BeautifulSoup(body, 'lxml').get_text()[-15:-11]
latestprocessed_data=None
latesttext=None
while True:
    msgdata=latest()
    processed_data=process(msg_data=msgdata)
    text=scraperab.scraperX(processed_data)
    if processed_data != latestprocessed_data or text != latesttext:
        latestprocessed_data=processed_data
        latesttext=text
        sender.msgsender(text)
        time.sleep(180)