import os
import requests
from bs4 import BeautifulSoup
import re
import smtplib, ssl


response = requests.get("https://www.policybazaar.com/gold-rate-hyderabad/")
soup = BeautifulSoup(response.text,"lxml")
mydivs = soup.findAll("div")

def check_mcx(str_):
    '''Checks if class="mcx" is in the contents of the string'''
    pattern = re.compile(r'(.*)(class="mcx")(.*)')
    search = pattern.search(str_)
    if search:
        return True
    else:
        False

def return_price(str_):
    '''Returns the gold price in Hyderabad if check is matched'''
    pattern = re.compile(r'(.*)Today gold price in Hyderabad is (\d+)(.*)')
    search = pattern.search(str_)
    if search:
        return int(search.group(2))
    else:
        return None

def send_email(price):
    '''Hardcoded send email functionality'''
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "arjundarbhadev@gmail.com"  # Enter your address
    receiver_email = "mecarjun2006@gmail.com"  # Enter receiver address
    password = "challenge927"
    message = """\
    Subject: TIME TO SELL GOLD

    The current gold price is {}
    This message is sent from Python.""".format(price)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)





if __name__ == '__main__':

    price_to_return = set()

    for div in mydivs:
        if check_mcx(str(div)):
            price_to_return.add(return_price(str(div)))

    price_to_alert = 32000

    if list(price_to_return)[0] > price_to_alert:
        send_email(price_to_return)



        
