import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import datetime
import time


email_subject = "商品上架提醒"
sender = "1119494837@qq.com"
password = "ehpcjmkkaodfhfbb"
recipients = ["414422927@qq.com", "574059378@qq.com"]
# recipient = "11610728@mail.sustech.edu.cn"
url = "https://www.sephora.com/product/le-rouge-deep-velvet-lipstick-P448881?skuId=2236099&keyword=2236099"

with open("check_in_stock_log.txt", "a") as log_file:
    log_file.write(f"loop starts at {datetime.datetime.now()}\n")
stop = False
while True:
    r = requests.get(url, proxies={"https": "socks5://127.0.0.1:1080"})
    soup = BeautifulSoup(r.text, 'html.parser')
    for button in soup.find_all("button", {"class": "css-1j1jwa4"}):
        if "37" in button['aria-label']:
            if not "Out of stock" in button['aria-label']:
                log_file = open("check_in_stock_log.txt", "a")
                log_file.write(
                    f"found in stock at {datetime.datetime.now()}\n")
                email_content = f"您关注的商品已上架，检测时间为: {datetime.datetime.now()}\n商品链接：{url}\n"
                for recipient in recipients:
                    msg = EmailMessage()
                    msg.set_content(email_content)
                    msg['Subject'] = email_subject
                    msg['From'] = sender
                    msg['To'] = recipient
                    try:
                        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
                        s.login(sender, password)
                        s.sendmail(sender, recipient, msg.as_string())
                        log_file.write(f"邮件发送成功, 收件人{recipient}\n")
                        stop = True
                        s.quit()
                    except smtplib.SMTPException as e:
                        log_file.write("邮件发送失败\n")
                        log_file.write(e)
                        log_file.write("\n")
                log_file.close()
            break
    if not stop:
        time.sleep(30)
        with open("check_in_stock.log", "a") as log_file:
            log_file.write(f"Out of stock at {datetime.datetime.now()}\n")
    else:
        break
