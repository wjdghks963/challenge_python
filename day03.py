import os as os
import requests


def again():
    yes_or_no = input("Do you want to start over? y/n  ")
    if yes_or_no == 'y':
        return os.system('clear'), find_URL()
    elif yes_or_no == 'n':
        print("Bye!")


def find_URL():
    print("Welcome to IsItDown.py!")
    print("Please Write a URL or URLs you want to check. (seperated by comma) ")

    urls = input().split(',')
    for url in urls:
        if "http" not in url:
            url = "http://" + url
        elif ".com" not in url:
            url = url + ".com"
        elif ".com" and "http" not in url:
            url = "http://" + url + ".com"
        try:
            res = requests.get(url)
            if res.status_code == 200:
                print(f"{url} is up!")
            else:
                print(f"{url} is down!")
        except:
            print(f"{url} is not valid url")
    again()


find_URL()
