# !/usr/bin/python
# -*- coding: utf-8 -*-

from gnews import GNews
from newspaper import Article
from datetime import datetime,timedelta
import requests, json
from bs4 import BeautifulSoup

class news:
    def __init__(self):
        self.unit = 'hours'
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
    def get_google_news(self,keyword):
        google_news = GNews(language='zh-Hant', country='TW', period="4h")
        news = google_news.get_news(keyword)
        news_count = len(news)
        # title,publisher,url,published date
        results = []
        for i in range(news_count):
            article = Article(news[i]['url'])
            article.download()
            article.parse()
            dateString = news[i]['published date']
            dateFormatter = "%a, %d %b %Y %H:%M:%S GMT"
            published_date = datetime.strptime(dateString, dateFormatter)
            title = news[i]['title']
            url = news[i]['url']
            publisher = news[i]['publisher']['title']
            if keyword in article.text:
                results.append({
                    'title':title,
                    'url':url,
                    'publisher':publisher,
                    'published_date':published_date
                })
        return results
    def get_udn_news(self,keyword):
        udn_url = 'https://udn.com/api/more?page=0&id=search:'+ keyword +'&channelId=2&type=searchword'
        res = requests.get(url=udn_url,headers=self.headers)
        news = res.json()['lists']
        results = []
        for i in range(len(news)):
            dateString = news[i]['time']['date']
            dateFormatter = "%Y-%m-%d %H:%M:%S"
            published_date = datetime.strptime(dateString, dateFormatter)
            title = news[i]['title']
            url = news[i]['titleLink']
            publisher = 'udn聯合新聞網'
            image = news[i]['url']
            expect_time = datetime.today() - timedelta(hours=4)
            if published_date >= expect_time:
                results.append({
                    'title':title,
                    'url':url,
                    'publisher':publisher,
                    'published_date':published_date
                })
            else:
                break
        return results
    def get_apple_news(self,keyword):
        apple_url = 'https://tw.appledaily.com/pf/api/v3/content/fetch/search-query?query=%7B%22searchTerm%22%3A%22'+ keyword +'%22%2C%22start%22%3A0%7D&_website=tw-appledaily'
        res = requests.get(url=apple_url,headers=self.headers)
        news = res.json()['content']
        results = []
        for i in range(len(news)):
            dateString = news[i]['pubDate']
            published_date = (datetime.fromtimestamp(int(dateString)))
            title = news[i]['title']
            url = news[i]['sharing']['url']
            publisher = news[i]['brandName']
            image = news[i]['sharing']['image']
            expect_time = datetime.today() - timedelta(hours=4)
            if published_date >= expect_time:
                results.append({
                    'title':title,
                    'url':url,
                    'publisher':publisher,
                    'published_date':published_date
                })
            else:
                break
        return results
    def get_setn_news(self,keyword):
        url = 'https://www.setn.com/search.aspx?q='+ keyword +'&r=0'
        res = requests.get(url=url,headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('div.newsimg-area-text-2')
        url_tag = soup.select("div.newsimg-area-info >  a.gt ")
        dates = soup.select('div.newsimg-date')
        images = soup.select('img.lazy')
        results = []
        publisher = '三立新聞網'
        for i in range(len(titles)):
            title = titles[i].text
            dateString = dates[i].text
            url = 'https://www.setn.com/' + url_tag[i].get('href').replace('&From=Search','')
            image = images[i].get('data-original').replace('-L','-PH')
            dateFormatter = "%Y/%m/%d %H:%M"
            published_date = datetime.strptime(dateString, dateFormatter)
            expect_time = datetime.today() - timedelta(hours=4)
            if published_date >= expect_time:
                results.append({
                    'title':title,
                    'url':url,
                    'publisher':publisher,
                    'published_date':published_date
                })
            else:
                break
        return results
    def get_ettoday_news(self,keyword):
        url = 'https://www.ettoday.net/news_search/doSearch.php?search_term_string='+ keyword
        res = requests.get(url=url,headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('h2 > a')
        date = soup.select('span.date')
        images = soup.select('img')
        publisher = 'ETtoday新聞雲'
        results = []
        for i in range(len(titles)):
            title = titles[i].text
            url = titles[i].get('href')
            publish = date[i].text.split('/')[1].replace(' ','')
            image = 'https:' + images[i].get('src').replace('/b','/d')
            dateFormatter = "%Y-%m-%d%H:%M)"
            published_date = datetime.strptime(publish, dateFormatter)
            expect_time = datetime.today() - timedelta(hours=4)
            if published_date >= expect_time:
                results.append({
                    'title':title,
                    'url':url,
                    'publisher':publisher,
                    'published_date':published_date
                })
            else:
                break
        return results
    def get_TVBS_news(self,keyword):
        url = 'https://news.tvbs.com.tw/news/searchresult/'+ keyword +'/news'
        res = requests.get(url=url,headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('h2.search_list_txt')
        urls = soup.select('span.search_list_box > a')
        dates = soup.select('span.publish_date')
        images = soup.select('img.lazyimage')
        publisher = 'TVBS新聞網'
        results = []
        for i in range(len(titles)):
            title = titles[i].text
            url = urls[i].get('href')
            publish = dates[i].text
            image = images[i].get('data-original')
            dateFormatter = "%Y/%m/%d %H:%M"
            published_date = datetime.strptime(publish, dateFormatter)
            expect_time = datetime.today() - timedelta(hours=4)
            if published_date >= expect_time:
                results.append({
                    'title':title,
                    'url':url,
                    'publisher':publisher,
                    'published_date':published_date
                })
            else:
                break
        return results
    def get_china_news(self,keyword):
        url = 'https://www.chinatimes.com/search/'+ keyword +'?chdtv'
        res = requests.get(url=url,headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('h3 > a')
        dates = soup.select('time')
        publisher = '中時新聞網'
        images = soup.select('img.photo')
        results = []
        for i in range(len(titles)):
            title = titles[i].text
            url = titles[i].get('href')
            image = images[i].get('src')
            dateString = dates[i].get('datetime')
            dateFormatter = "%Y-%m-%d %H:%M"
            published_date = datetime.strptime(dateString, dateFormatter)
            print(title,published_date,url)
            expect_time = datetime.today() - timedelta(hours=4)
            if published_date >= expect_time:
                results.append({
                    'title':title,
                    'url':url,
                    'publisher':publisher,
                    'published_date':published_date
                })
            else:
                break
        return results
    def get_storm_news(self,keyword):
        url = 'https://www.storm.mg/site-search/result?q='+ keyword +'&order=none&format=week'
        res = requests.get(url=url,headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('p.card_title')
        urls = soup.select('a.card_substance')
        publish_dates = soup.select('span.info_time')
        images = soup.select('img.card_img')
        publisher = '風傳媒'
        results = []
        for i in range(len(titles)):
            title = titles[i].text
            url = 'https://www.storm.mg' + urls[i].get('href')
            image = images[i].get('src').replace('150x150','800x533')
            publish_date = publish_dates[i].text
            dateFormatter = "%Y-%m-%d %H:%M"
            published_date = datetime.strptime(publish_date, dateFormatter)
            expect_time = datetime.today() - timedelta(hours=4)
            if published_date >= expect_time:
                results.append({
                    'title':title,
                    'url':url,
                    'publisher':publisher,
                    'published_date':published_date
                })
            else:
                break
        return results
    def get_ttv_news(self,keyword):
        url = 'https://news.ttv.com.tw/search/' + keyword
        res = requests.get(url=url,headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('div.title')
        urls = soup.select('ul > li > a.clearfix')
        publishes = soup.select('div.time')
        images = soup.select('img["alt=''"]')
        publisher = '台視新聞網'
        results = []
        for i in range(len(urls)):
            url = 'https://news.ttv.com.tw/'+urls[i].get('href')
            title = titles[i+2].text
            publish = publishes[i].text
            image = images[i].get('src')
            dateFormatter = "%Y/%m/%d %H:%M:%S"
            published_date = datetime.strptime(publish, dateFormatter)
            expect_time = datetime.today() - timedelta(hours=4)
            if published_date >= expect_time:
                results.append({
                    'title':title,
                    'url':url,
                    'publisher':publisher,
                    'published_date':published_date
                })
            else:
                break
        return results
    def get_ftv_news(self,keyword):
        url = 'https://www.ftvnews.com.tw/search/' + keyword
        res = requests.get(url=url,headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('div.title')
        urls = soup.select('ul > li > a.clearfix')
        publishes = soup.select('div.time')
        images = soup.select('img["loading"]')
        publisher = '民視新聞網'
        results = []
        for i in range(len(urls)):
            url = 'https://www.ftvnews.com.tw/'+urls[i].get('href')
            title = titles[i].text
            publish = publishes[i].text
            image = images[0].get('src')
            dateFormatter = "%Y/%m/%d %H:%M:%S"
            published_date = datetime.strptime(publish, dateFormatter)
            expect_time = datetime.today() - timedelta(hours=4)
            if published_date >= expect_time:
                results.append({
                    'title':title,
                    'url':url,
                    'publisher':publisher,
                    'published_date':published_date
                })
            else:
                break
        return results
    def get_cna_news(self,keyword):
        url = 'https://www.cna.com.tw/search/hysearchws.aspx?q=' + keyword
        res = requests.get(url=url,headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        urls = soup.select('ul.mainList > li > a')
        titles = soup.select('div.listInfo > h2')
        dates = soup.select('div.date')
        publisher = 'CNA中央社'
        results = [] 
        for i in range(len(urls)):
            url = urls[i].get('href')
            title = titles[i].text
            publish = dates[i].text
            image_url = urls[i].img
            if image_url != None:
                image = image_url['data-src'].replace('/200/','/400/')
            else:
                image = None
            dateFormatter = "%Y/%m/%d %H:%M"
            published_date = datetime.strptime(publish, dateFormatter)
            expect_time = datetime.today() - timedelta(hours=4)
            if published_date >= expect_time:
                results.append({
                    'title':title,
                    'url':url,
                    'publisher':publisher,
                    'published_date':published_date
                })
            else:
                break
        return results
    def get_ltn_news(self,keyword):
        url = 'https://search.ltn.com.tw/list?keyword=' + keyword
        res = requests.get(url=url,headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        tit_tag = soup.find_all("a", class_="tit")
        images = soup.select('img.lazy_imgs')
        results = []
        publisher = '自由時報電子報'
        for i in range(len(tit_tag)):
            title = tit_tag[i]['title']
            url = tit_tag[i]['href']
            res = requests.get(url=url,headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            publish = soup.select('span.time')[0].text.replace('\n    ','')
            image = images[i].get('data-src')
            dateFormatter = "%Y/%m/%d %H:%M"
            published_date = datetime.strptime(publish, dateFormatter)
            expect_time = datetime.today() - timedelta(hours=4)
            if published_date >= expect_time:
                results.append({
                    'title':title,
                    'url':url,
                    'publisher':publisher,
                    'published_date':published_date
                })
            else:
                break
        return results
if __name__ == '__main__':
    print(news().get_apple_news('基進'))