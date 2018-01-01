import requests
import json
from datetime import datetime
import time

while True:
    url = 'http://www.btc38.com/trade/getCoinHold.php?coinname=INF&n=0.3432717926410971'
    headers = {
        'Referer': 'http://www.btc38.com/altcoin/application_info.html?id=2606',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }

    response = requests.get(url, headers=headers).text
    response = json.loads(response)
    text = "{}  {}    {}  {}  {}  {}  {}  {}  {}  {}  {}  {}  {}\n".format(datetime.now(), response['holders'],
                                                                           response['totalCoins'],
                                                                           response['coinsPerHolders'],
                                                                           response['inflow24H'],
                                                                           response['outflow24H'], response['change24H'],
                                                                           response['inflowWeek'], response['outflowWeek'],
                                                                           response['changeWeek'], response['updateTime'],
                                                                           response['top10'], response['updateTime2']
                                                                           )
    file = open(r'I:\讯链.txt', 'a')
    file.write(text)
    file.close()
    time.sleep(60)
