import os
import requests
from bs4 import BeautifulSoup

os.system("clear")

url = "https://www.iban.com/currency-codes"

countries = []

request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")

table = soup.find("table")
rows = table.find_all("tr")[1:]

for row in rows:
    items = row.find_all("td")
    name = items[0].text
    code = items[2].text
    if name and code:
        if name != "No universal currency":
            country = {
                'name': name.capitalize(),
                'code': code
            }
            countries.append(country)


def format_currency():
    print("Where are you from? Choose a country by number")
    res = input(f"# ")

    if res.isdigit():
        res = int(res)
        con = countries[res].get('name')
        cod = countries[res].get('code')
        print(f"{con}\n\nNow Choose another country\n")
    elif res.isalpha():
        print("that x")
        res = input(f"# ")
        res = int(res)
        con = countries[res].get('name')
        cod = countries[res].get('code')
        print(f"{con}\n\nNow Choose another country\n")

    res_1 = input(f"# ")

    if res_1.isdigit():
        res_1 = int(res_1)
        con_1 = countries[res_1].get('name')
        cod_1 = countries[res_1].get('code')
        print(f"{con_1}\n\nHow many {cod} do you want to {cod_1}")
    elif res_1.isalpha():
        print("That wasn't a number.")
        res_1 = input(f"# ")
        res_1 = int(res_1)
        con_1 = countries[res_1].get('name')
        cod_1 = countries[res_1].get('code')
        print(f"{con_1}\n\nHow many {cod} do you want to {cod_1}")

    mount = float(input())

    cod_l = str(cod).lower()
    cod_1_l = str(cod_1).lower()
    convert_url = f"https://wise.com/gb/currency-converter/{cod_l}-to-{cod_1_l}-rate?amount={mount}"
    request_con = requests.get(convert_url)
    soup_con = BeautifulSoup(request_con.text, "html.parser")
    one_for_other = soup_con.find("div", {"class": "col-lg-6 text-xs-center text-lg-left"})
    h3 = one_for_other.find("h3", {"class": "cc__source-to-target"})
    other = h3.find("span", {"class": "text-success"})
    cc = float(other.getText())
    done = cc * mount
    print(f"{cod}  {mount} is {cod_1} {done}")


format_currency()
