import os
import csv
import requests
from bs4 import BeautifulSoup
import re

os.system("clear")
alba_url = "http://www.alba.co.kr"
request_alba = requests.get(alba_url)
soup = BeautifulSoup(request_alba.text, "html.parser")

super_box = soup.find("div", {"id": "MainSuperBrand"})
super_item = super_box.find("ul", {"class": "goodsBox"})
links = super_item.find_all("a", {"class": "goodsBox-info"})
company = super_item.find('span', {"class": "company"}).getText()


def extract_jobs():
    for link in links:
        a = link.get('href')
        request_jobs = requests.get(a)
        soup = BeautifulSoup(request_jobs.text, "html.parser")
        table = soup.find("table")
        tbody = table.find("tbody")
        trs = tbody.find_all('tr', {"class": ["", "divide "]})
        diction = {'location': [],
                   'title': [],
                   'time': [],
                   'pay': [],
                   'date': []
                   }
        for tr in trs:
            locs = tr.find_all('td', {'class': 'local'})
            titles = tr.find_all('span', {'class': 'company'})
            times = tr.find_all('td', {'class': 'data'})
            pays = tr.find_all('td', {'class': 'pay'})
            dates = tr.find_all('td', {'class': 'regDate last'})
            for loc in locs:
                loc_txt = loc.getText()
                loc_txt = re.sub("\xa0", "", loc_txt)
                diction['location'].append(loc_txt)
            for tit in titles:
                title_txt = tit.getText()
                diction['title'].append(title_txt)
            for time in times:
                time_txt = time.getText()
                diction['time'].append(time_txt)
            for pay in pays:
                pay_txt = pay.getText()
                diction['pay'].append(pay_txt)
            for date in dates:
                date_text = date.getText()
                diction['date'].append(date_text)

            field_names = ['location', 'title', 'time', 'pay', 'date']
            with open(f'{company}.csv', 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=field_names, extrasaction='ignore')
                writer.writeheader()
                writer.writerow(diction)



extract_jobs()
