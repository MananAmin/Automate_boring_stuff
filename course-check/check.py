import schedule
import requests
import time

import telegram_send
from bs4 import BeautifulSoup

# To use change course CRN number and number of seats 
# set telegram bot for notification

def check():
    keyword1 = "30619" # course CRN number
    seats1 = "150" # seats 
    keyword2 = "30633"
    seats2 = "125"

    urllink = "https://dalonline.dal.ca/PROD/fysktime.P_DisplaySchedule?s_term=202230&s_crn=&s_subj=CSCI&s_numb=&n=21&s_district=100D"

    r = requests.get(urllink)

    soup = BeautifulSoup(r.text,features="html.parser")
    sub1 = soup.find("b",string=keyword1)
    sub2 = soup.find("b",string=keyword2)


    tr1 = sub1.parent.parent if sub1 else None
    tr2 = sub2.parent.parent if sub2 else None

    flag = False
    ans = True
    for tag in tr1:
        if flag and seats1 in tag.text:
            ans =False
            break

        if seats1 in tag.text:
            flag = True

    if ans:
        print("Notifies 1")
        telegram_send.send(messages=["Hello Brother.  course.  "])

    flag = False
    ans2 = True
    for tag in tr2:
        if flag and seats2 in tag.text:
            ans2 =False
            break

        if seats2 in tag.text:
            flag = True

    if ans2:
        print("Notifies 2")
        telegram_send.send(messages=["Hello Brother.  course.  "])


if __name__=="__main__":
    schedule.every(1).minutes.do(check)
    while True:
        schedule.run_pending()
        time.sleep(1)

# https://dalonline.dal.ca/PROD/fysktime.P_DisplaySchedule?s_term=202230&s_crn=&s_subj=CSCI&s_numb=&n=21&s_district=100D