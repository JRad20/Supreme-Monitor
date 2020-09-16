import requests
from bs4 import BeautifulSoup
import time
import threading
from discord_webhook import DiscordWebhook, DiscordEmbed
from flask import Flask
import json
global product_title

URLS = []


file_open = open('products.txt').readlines()
for url in file_open:
    prod_url = url.strip()
    URLS.append(prod_url)

hook = ''
DELAY = 1.25


hooks_sent = []
def main_function(x):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    r = requests.get(x, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    #find_atc = soup.find(id="add-remove-buttons")
    for title in soup.find_all(['h2']):
        product_title = title.text
    check_if_in_stock = requests.get(x+'.json')
    data = json.loads(check_if_in_stock.content.decode('utf-8'))
    temp = data['styles']
    for y in temp:
        sizes_list = y['sizes']
        for stock_level in sizes_list:
            in_stock = stock_level['stock_level']
            break
    if int(in_stock) == 0:
        print('Product is out of stock '+x)
        if x in hooks_sent:
            hooks_sent.remove(x)
    else:
        if x in hooks_sent:
            print('Product in stock but webhook has already bent sent!')
        else:
            webhook = DiscordWebhook(url=hook)
            embed = DiscordEmbed(title=product_title, description=r.url, color=000)
            webhook.add_embed(embed)
            response = webhook.execute()
            print('Product restocked '+x)
            hooks_sent.append(x)
def run():

    while True:
        time.sleep(DELAY)
        runningThreads = []
        for x in URLS:
            thread = threading.Thread(target=main_function, args=(x,))
            thread.start()
            runningThreads.append(thread)

        for y in runningThreads:
            y.join()

if __name__ == '__main__':
    run()
