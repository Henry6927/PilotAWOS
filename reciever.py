import imaplib
import email
import time
from bs4 import BeautifulSoup
import scraperab
import sender
import os

def latest():
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        mail.login(os.environ['WeatherEmail'], os.environ['WeatherPassword'])
        mail.select("inbox")
        _, data = mail.search(None, "FROM " + str(os.environ['WeatherPhone']))
        mail_ids = data[0].split()
        latest_email_id = mail_ids[-1]
        _, msg_data = mail.fetch(latest_email_id, '(RFC822)')
        return msg_data

def ica(msg_data):
    for response_part in msg_data:
            msg = email.message_from_bytes(response_part[1])
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition'):
                        body = part.get_payload(decode=True)
                        body = body.decode('utf-8', 'ignore')
                        if "ICAO:" in body:
                            return BeautifulSoup(body, 'lxml').get_text()[-15:-11]
ICO=""
ICAO="-"
ICOw = ""
ICAOw = "-"
while True:
    msg_data = latest()
    if msg_data:
        ICO = ica(msg_data)
        ICOw = scraperab.scraperX(ica(msg_data))
        if ICOw and ICOw != ICAOw or ICO!=ICAO:
            ICAO = ICO
            ICAOw = ICOw
            print("ICAO code: "+ ica(msg_data))
            weather=scraperab.scraperX(ica(msg_data))
            sender.msgsender(weather)
    else:
        print("No new email")
    
    time.sleep(2)