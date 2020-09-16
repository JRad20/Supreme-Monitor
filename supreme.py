import requests
from bs4 import BeautifulSoup
import time
import threading
from discord_webhook import DiscordWebhook


URLS = []
hook = ''
DELAY = 1.25


hooks_sent = []

def main_function(x):

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    r = requests.get(x, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    find_atc = soup.find(id="add-remove-buttons")
    if str(find_atc) == "None":
        print('Product is out of stock '+x)
        if x in hooks_sent:
            hooks_sent.remove(x)
    else:
        if x in hooks_sent:
            print('Product in stock but webhook has already bent sent!')
        else:
            webhook = DiscordWebhook(url=hook, content=x+' Has restocked')
            response = webhook.execute()
            print('Product restocked '+x)
            hooks_sent.append(x)

if __name__ == '__main__':
    while True:
        time.sleep(DELAY)
        runningThreads = []
        for x in URLS:
            thread = threading.Thread(target=main_function, args=(x,))
            thread.start()
            runningThreads.append(thread)
        for y in runningThreads:
            y.join()
