import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
from datetime import datetime 
import os

def msgsender(weather):
    now=datetime.now()
    today=date.today()
    x="Weather forcast for: "+ str(now)[11:19] + ", " + today.strftime(' %B, %d, %Y, ')
    
    sender = os.environ['WeatherEmail']
    receiver = os.environ['WeatherReciever']
    password = os.environ['WeatherPassword']
    
    body = MIMEText(weather, _subtype='plain', _charset=None)
    
    msg = MIMEMultipart()
    msg['Subject'] = x 
    msg.attach(body)
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()
    
    print("sent to:", receiver)
    print("message:", body)
    print("subject: ", x)