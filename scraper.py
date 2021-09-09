from bs4 import BeautifulSoup
import requests     # To acess URL
import smtplib
import re
import time


URL = "https://www.amazon.in/Puma-Unisex-C-Skate-Sneaker-10-37490105/dp/B08TQPDVWZ/ref=sr_1_31?dchild=1&keywords=puma%2Bshoes%2Bmen%2Bsneakers&qid=1631174285&sr=8-31&th=1&psc=1"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}    # Type on Browser -> My user agent


def check_price():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    
    price = re.sub("[^\d.]","", price) 
    converted_price = float(price[0:6])
    # p_price = price.replace(',',"")
    # converted_price = float(p_price[1:6])

    if converted_price < 1800.0:
        send_mail()

    print(converted_price)
    print(title.strip())

    if converted_price > 1800.0:
        send_mail()


def send_mail():
    # 587 is the connection number
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(
        'GMAIL', 
        'PASSWORD'
        )
    
    subject = "Price Fell down"
    body = f'Check the link {URL}'

    msg = f'Subject: {subject}\n\n{body}'
    server.sendmail(
        'FROM_GMAIL',
        'To_GMAIL',
        msg
    )
    
    server.quit()
    print("Mail Sent")


check_price()

# # Exteneded HELO (EHLO) is an Extended Simple Mail Transfer Protocol (ESMTP) command sent by an email server to identidy itself when it is connecting to another email server to start the process of sending an email.
# # It is followed with the sending email server's domain name.
