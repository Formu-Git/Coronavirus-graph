from bs4 import BeautifulSoup
import requests
from datetime import date
import time
from pylab import *

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

thirty_one_months = ["01", "03", "05", "07","08", "10", "12"]


def interface():
    for i in countries:
        if i != 'Covid-19 (en)' and i != 'Coronavirus statistics (en)' and i != 'Israël' and i != 'Séléctionner':
            print(i)
    print(">>Choose a country between those.")
    country = input(">>")
    if country in countries:
        url = url_countries[country]
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        print("\n01 02 03 04 05 06 07 08 09 10 11 12")
        print(">>Choose a month between those.")
        month = input(">>")
        if int(month) < 12 and int(month) <= int(date.today().month):
            if month in thirty_one_months:
                graph(month, 31, country)
            else:
                graph(month, 30, country)
        else:
            print("\n>>None data found.")
            time.sleep(1)
            interface()
    else:
        print("\n>>None data found.")
        time.sleep(1)
        interface()

url_countries = {}
countries = []
def get_countries():
    url = "https://www.coronavirus-statistiques.com/stats-pays/coronavirus-nombre-de-cas-maroc#"
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    for i in soup.find_all('option'):
        url_countries[i.text] = i.get('value')
        countries.append(i.text)



def graph(month,i,country):
    url = url_countries[country]
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    days = []
    contamined = []
    dead = []
    a = i
    for data in soup.find_all('td'):
        splited_days = str(data).split('/')
        if splited_days[1] == f"{month}<" and i > 0:
            contamined.append(int(
                str(soup.find_all('td')[soup.find_all('td').index(data) + 1]).split("<strong>")[1].split(" <font")[
                    0].replace(" ", "")))
            dead.append(int(
                str(soup.find_all('td')[soup.find_all('td').index(data) + 2]).split("right;\">")[1].split(" <font")[
                    0].replace(" ", "")))
            days.append(i)
            i = i - 1
    x = asarray(days, dtype=int)
    y = asarray(contamined, dtype=int)
    plt.plot(x, y, label="*")
    plt.title("Coronavirus stats between 01/{}/2022 and {}/{} in {}.".format(month, a, month,country))
    plt.savefig(f"corona-{country}-{month}.png", dpi=300)


get_countries()
interface()
