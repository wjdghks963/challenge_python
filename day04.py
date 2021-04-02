import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"
re_url = requests.get(url)
soup = BeautifulSoup(re_url.text, "html.parser")

contrys = soup.select("tbody>tr>td:nth-of-type(1)")
codes = soup.select("tbody>tr>td:nth-of-type(3)")
con_arr = []
code_arr = []



print("Hello! Please choose select a country by number: ")
for con in contrys:
    a = con.string
    con_arr.append(a)
    continue

for i in range(len(con_arr)):
    print(f"# {i} {con_arr[i]}")

for code in codes:
   b = code.string
   code_arr.append(b)
   continue


def req():
    res = input("#: ")

    try:
        if res.isdigit():
            res = int(res)
            key = con_arr[res]
            value = code_arr[res]
            print(f"You Choose {key}")
            print(f"The currency code is {value}?")
        elif res.isalpha():
            print("That wasn't a number.")
    except:
        print("Choose a number from the list")

    req()



req()