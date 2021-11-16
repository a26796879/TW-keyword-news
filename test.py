from gnews import GNews
from newspaper import Article
from datetime import datetime,timedelta
import requests, json
from GoogleNews import GoogleNews
from bs4 import BeautifulSoup
apple_url = 'https://tw.appledaily.com/pf/api/v3/content/fetch/search-query?query=%7B%22searchTerm%22%3A%22'+ '基進' +'%22%2C%22start%22%3A0%7D&d=264&_website=tw-appledaily'
url = 'https://tw.appledaily.com/pf/api/v3/content/fetch/search-query?query=%7B%22searchTerm%22%3A%22%22%2C%22start%22%3A20%7D&d=264&_website=tw-appledaily'
headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-TW,zh;q=0.9',
    'if-none-match': 'W/"989a-QvaRHTovk4mLrItkm2o2tDX3w/4"',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}
res = requests.get(url=apple_url,headers=headers)
print(res.text)
#news = res.json()['content']
'''
results = []
for i in range(len(news)):
    article = Article(news[i]['sharing']['url'])
    article.download()
    article.parse()
    dateString = news[i]['pubDate']
    published_date = (datetime.fromtimestamp(int(dateString)))
    title = news[i]['title']
    url = news[i]['sharing']['url']
    publisher = news[i]['brandName']
    results.append({
'title':title,
'url':url,
'publisher':publisher,
'published_date':published_date
    })
'''