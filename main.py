# !/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
import time
import urllib
from datetime import datetime, timedelta
import re
from newspaper import Article
from gnews import GNews
from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession
from fake_useragent import UserAgent
ua = UserAgent()


class NewsCrawler:
    def __init__(self):
        self.unit = 'hours'
        self.headers = {
            'user-agent': ua.random
        }

    @classmethod
    def get_google_news(cls, keyword):
        '''get google news by GNews library'''
        google_news = GNews(language='zh-Hant', country='TW', period="4h")
        news = google_news.get_news(keyword)
        news_count = len(news)
        results = []
        for i in range(news_count):
            article = Article(news[i]['url'])
            article.download()
            article.parse()
            date_string = news[i]['published date']
            date_format = "%a, %d %b %Y %H:%M:%S GMT"
            published_date = datetime.strptime(date_string, date_format)
            title = news[i]['title']
            url = news[i]['url']
            publisher = news[i]['publisher']['title']
            if keyword in article.text:
                results.append({
                    'title': title,
                    'url': url,
                    'publisher': publisher,
                    'published_date': published_date
                })
        return results


    async def get_udn_news(self, async_session, keyword):
        ''' get udn news by crawling'''
        udn_url = 'https://udn.com/api/more?page=0&id=search:' + \
            urllib.parse.quote_plus(keyword) + '&channelId=2&type=searchword'
        res = await async_session.get(url=udn_url, headers=self.headers)
        news = res.json()['lists']
        results = []
        for value in enumerate(news):
            date_string = news[value[0]]['time']['date']
            date_format = "%Y-%m-%d %H:%M"
            published_date = datetime.strptime(date_string, date_format)
            title = news[value[0]]['title']
            url = news[value[0]]['titleLink']
            publisher = 'udn聯合新聞網'
            #image = news[i]['url']
            expect_time = datetime.today() - timedelta(hours=8)
            if published_date >= expect_time:
                results.append({
                    'title': title,
                    'url': url,
                    'publisher': publisher,
                    'published_date': published_date
                })
            else:
                break
        return results

    async def get_apple_news(self, async_session, keyword):
        ''' get apple news by crawling'''
        apply_url = 'https://tw.appledaily.com/search/' + \
            urllib.parse.quote_plus(keyword)
        res = await async_session.get(url=apply_url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        publish = soup.select('div.timestamp')
        results = []
        for i in range(len(publish)):
            date_string = soup.select('div.timestamp')[i].text
            date_format = "出版時間：%Y/%m/%d %H:%M"
            published_date = datetime.strptime(date_string, date_format)
            expect_time = datetime.today() - timedelta(hours=8)
            if published_date >= expect_time:
                results.append({
                    'title': soup.select('span.headline')[i].text,
                    'url': 'https://tw.appledaily.com/' + \
                        soup.select('a.story-card')[i].get('href'),
                    'publisher': '蘋果新聞網',
                    'published_date': published_date
                })
            else:
                break
        return results

    async def get_setn_news(self, async_session, keyword):
        ''' get setn news by crawling'''
        url = 'https://www.setn.com/search.aspx?q=' + \
            urllib.parse.quote_plus(keyword) + '&r=0'
        res = await async_session.get(url=url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('div.newsimg-area-text-2')
        url_tag = soup.select("div.newsimg-area-info >  a.gt ")
        dates = soup.select('div.newsimg-date')
        #images = soup.select('img.lazy')
        results = []
        for value in enumerate(titles):
            date_string = dates[value[0]].text
            #image = images[i].get('data-original').replace('-L','-PH')
            date_format = "%Y/%m/%d %H:%M"
            published_date = datetime.strptime(date_string, date_format)
            expect_time = datetime.today() - timedelta(hours=8)
            if published_date >= expect_time:
                results.append({
                    'title': titles[value[0]].text,
                    'url': 'https://www.setn.com/' + \
                        url_tag[value[0]].get('href').replace('&From=Search', ''),
                    'publisher': '三立新聞網',
                    'published_date': published_date
                })
            else:
                break
        return results

    async def get_ettoday_news(self, async_session, keyword):
        ''' get udn ettoday by crawling'''
        url = 'https://www.ettoday.net/news_search/doSearch.php?search_term_string=' + \
            urllib.parse.quote_plus(keyword)
        res = await async_session.get(url=url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('h2 > a')
        date = soup.select('span.date')
        # images = soup.select('img')
        results = []
        for value in enumerate(titles):
            publish = date[value[0]].text.split('/')[1].replace(' ', '')
            #image = 'https:' + images[i].get('src').replace('/b','/d')
            date_format = "%Y-%m-%d%H:%M)"
            published_date = datetime.strptime(publish, date_format)
            expect_time = datetime.today() - timedelta(hours=8)
            if published_date >= expect_time:
                results.append({
                    'title': titles[value[0]].text,
                    'url': titles[value[0]].get('href'),
                    'publisher': 'ETtoday新聞雲',
                    'published_date': published_date
                })
            else:
                break
        return results

    async def get_tvbs_news(self, async_session, keyword):
        ''' get TVBS news by crawling'''
        url = 'https://news.tvbs.com.tw/news/searchresult/' + \
            urllib.parse.quote_plus(keyword) + '/news'
        res = await async_session.get(url=url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('h2')
        results = []
        for value in enumerate(titles):
            each_url = titles[value[0]].find_parents("a")[0].get('href')
            res = await async_session.get(url=each_url, headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            sult = r"發佈時間：\d\d\d\d\/\d\d\/\d\d \d\d:\d\d"
            match = re.search(sult, soup.select('div.author')[0].text)
            date_format = "發佈時間：%Y/%m/%d %H:%M"
            published_date = datetime.strptime(match.group(), date_format)
            expect_time = datetime.today() - timedelta(hours=8)
            if published_date >= expect_time:
                results.append({
                    'title': titles[value[0]].text,
                    'url': each_url,
                    'publisher': 'TVBS新聞網',
                    'published_date': published_date
                })
            else:
                break
        return results

    async def get_china_news(self, async_session, keyword):
        ''' get chinatime news by crawling'''
        url = 'https://www.chinatimes.com/search/' + \
            urllib.parse.quote_plus(keyword) + '?chdtv'
        res = await async_session.get(url=url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('h3 > a')
        dates = soup.select('time')
        # images = soup.select('img.photo')
        results = []
        for value in enumerate(titles):
            # image = images[value[0]].get('src')
            date_string = dates[value[0]].get('datetime')
            date_format = "%Y-%m-%d %H:%M"
            published_date = datetime.strptime(date_string, date_format)
            expect_time = datetime.today() - timedelta(hours=8)
            if published_date >= expect_time:
                results.append({
                    'title': titles[value[0]].text,
                    'url': titles[value[0]].get('href'),
                    'publisher': '中時新聞網',
                    'published_date': published_date
                })
            else:
                break
        return results

    async def get_storm_news(self, async_session, keyword):
        ''' get 風傳媒 news by crawling'''
        url = 'https://www.storm.mg/site-search/result?q=' + \
            urllib.parse.quote_plus(keyword) + '&order=none&format=week'
        res = await async_session.get(url=url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('p.card_title')
        urls = soup.select('a.card_substance')
        publish_dates = soup.select('span.info_time')
        # images = soup.select('img.card_img')
        results = []
        for value in enumerate(titles):
            # image = images[i].get('src').replace('150x150','800x533')
            publish_date = publish_dates[value[0]].text
            date_format = "%Y-%m-%d %H:%M"
            published_date = datetime.strptime(publish_date, date_format)
            expect_time = datetime.today() - timedelta(hours=8)
            if published_date >= expect_time:
                results.append({
                    'title': titles[value[0]].text,
                    'url': 'https://www.storm.mg' + urls[value[0]].get('href'),
                    'publisher': '風傳媒',
                    'published_date': published_date
                })
            else:
                break
        return results

    async def get_ttv_news(self, async_session, keyword):
        ''' get 台視 news by crawling'''
        url = 'https://news.ttv.com.tw/search/' + \
            urllib.parse.quote_plus(keyword)
        res = await async_session.get(url=url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('ul > li > a.clearfix > div.content > div.title')
        urls = soup.select('ul > li > a.clearfix')
        publishes = soup.select(
            'ul > li > a.clearfix > div.content > div.time')
        # images = soup.select('img[alt=""]')
        results = []
        for value in enumerate(urls):
            publish = publishes[value[0]].text
            # image = images[i].get('src')
            date_format = "%Y/%m/%d %H:%M:%S"
            published_date = datetime.strptime(publish, date_format)
            expect_time = datetime.today() - timedelta(hours=8)
            if published_date >= expect_time:
                results.append({
                    'title':  titles[value[0]].text.replace('\u3000', ' '),  # 將全形space取代為半形space
                    'url': 'https://news.ttv.com.tw/' + urls[value[0]].get('href'),
                    'publisher': '台視新聞網',
                    'published_date': published_date
                })
            else:
                break
        return results

    async def get_ftv_news(self, async_session, keyword):
        ''' get 民視 news by crawling'''
        url = 'https://www.ftvnews.com.tw/search/' + \
            urllib.parse.quote_plus(keyword)
        res = await async_session.get(url=url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.select('div.title')
        urls = soup.select('ul > li > a.clearfix')
        publishes = soup.select('div.time')
        # images = soup.select('img[loading]')
        results = []
        for value in enumerate(urls):
            publish = publishes[value[0]].text
            # image = images[i].get('src')
            date_format = "%Y/%m/%d %H:%M:%S"
            published_date = datetime.strptime(publish, date_format)
            expect_time = datetime.today() - timedelta(hours=8)
            if published_date >= expect_time:
                results.append({
                    'title': titles[value[0]].text,
                    'url': 'https://www.ftvnews.com.tw/'+urls[value[0]].get('href'),
                    'publisher': '民視新聞網',
                    'published_date': published_date
                })
            else:
                break
        return results

    async def get_cna_news(self, async_session, keyword):
        ''' get 中央社 news by crawling'''
        url = 'https://www.cna.com.tw/search/hysearchws.aspx?q=' + \
            urllib.parse.quote_plus(keyword)
        res = await async_session.get(url=url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        urls = soup.select('ul.mainList > li > a')
        titles = soup.select('div.listInfo > h2')
        dates = soup.select('div.date')
        results = []
        for value in enumerate(urls):
            publish = dates[value[0]].text
            # image_url = urls[value[0]].img
            # if image_url != None:
            #   image = image_url['data-src'].replace('/200/','/400/')
            # else:
            #   image = None
            date_format = "%Y/%m/%d %H:%M"
            published_date = datetime.strptime(publish, date_format)
            expect_time = datetime.today() - timedelta(hours=8)
            if published_date >= expect_time:
                results.append({
                    'title': titles[value[0]].text,
                    'url': urls[value[0]].get('href'),
                    'publisher': 'CNA中央社',
                    'published_date': published_date
                })
            else:
                break
        return results

    async def get_ltn_news(self, async_session, keyword):
        ''' get 自由時報 news by crawling'''
        url = 'https://search.ltn.com.tw/list?keyword=' + \
            urllib.parse.quote_plus(keyword)
        res = await async_session.get(url=url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        tit_tag = soup.find_all("a", class_="tit")
        results = []
        for value in tit_tag:
            each_url = value.get('href')
            res = await async_session.get(url=each_url, headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            if 'health.ltn' in each_url or 'sports.ltn' in each_url or 'ec.ltn' in each_url:
                publish = soup.select('span.time')[1].text.replace(
                    '\n    ', '').replace('\r', '')
            elif 'ent.ltn' in each_url:
                publish = soup.select('time.time')[1].text.replace(
                    '\n    ', '').replace('\r', '')
            elif 'istyle' in each_url:
                publish = soup.select('span.time')[0].text.split('\n')[0].replace(
                    '\n    ', '').replace('\r', '').replace('  ', '')
            else:
                publish = soup.select('span.time')[0].text.replace(
                    '\n    ', '').replace('\r', '')
            date_format = "%Y/%m/%d %H:%M"
            published_date = datetime.strptime(publish, date_format)
            expect_time = datetime.today() - timedelta(hours=8)
            if published_date >= expect_time:
                results.append({
                    'title': value.text,
                    'url': each_url,
                    'publisher': '自由時報電子報',
                    'published_date': published_date
                })
            else:
                break
        return results


async def main(*keywords):
    ''' using async_session to run all functions'''
    async_session = AsyncHTMLSession()
    udn_task = (NewsCrawler().get_udn_news(async_session, keyword)
                for keyword in keywords)
    apple_task = (NewsCrawler().get_apple_news(async_session, keyword)
                  for keyword in keywords)
    setn_task = (NewsCrawler().get_setn_news(async_session, keyword)
                 for keyword in keywords)
    ettoday_task = (NewsCrawler().get_ettoday_news(async_session, keyword)
                    for keyword in keywords)
    tvbs_task = (NewsCrawler().get_tvbs_news(async_session, keyword)
                 for keyword in keywords)
    china_task = (NewsCrawler().get_china_news(async_session, keyword)
                  for keyword in keywords)
    storm_task = (NewsCrawler().get_storm_news(async_session, keyword)
                  for keyword in keywords)
    ttv_task = (NewsCrawler().get_ttv_news(async_session, keyword)
                for keyword in keywords)
    ftv_task = (NewsCrawler().get_ftv_news(async_session, keyword)
                for keyword in keywords)
    ltn_task = (NewsCrawler().get_ltn_news(async_session, keyword)
                for keyword in keywords)
    cna_task = (NewsCrawler().get_cna_news(async_session, keyword)
                for keyword in keywords)
    gather = await asyncio.gather(*udn_task, *apple_task, *setn_task, *ettoday_task
            ,*tvbs_task,*china_task, *storm_task, *ttv_task, *ftv_task, *ltn_task, *cna_task)
    return gather

if __name__ == "__main__":
    start = time.perf_counter()
    result = asyncio.run(main('日本'))
    print(result)
    end = time.perf_counter() - start
    print(end)
