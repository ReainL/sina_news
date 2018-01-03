#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 18-1-3

@author: Xu
"""
import requests
import pandas
import re
from bs4 import BeautifulSoup

def get_article(url):
    res1 = requests.get(url)
    res1.encoding = 'utf-8'
    soup1 = BeautifulSoup(res1.text, 'html.parser')
    dic = {}
    dic['title'] = soup1.select('.page-header #artibodyTitle')[0].text
    dic['content'] = ''.join([ele.text for ele in soup1.select('.article_16 p')])
    dic['source'] = soup1.select('#navtimeSource')[0].text
    dic['keyword'] = soup1.select('.article-info .article-keywords')[0].text
    return dic

def get_all_news():
    res = requests.get('http://news.sina.com.cn/china/')
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    newsary = []
    for link in soup.select('.news-item'):
        if len(link.select('h2 a')) > 0:
            newsary.append(get_article(link.select('h2 a')[0]['href']))
    df = pandas.DataFrame(newsary)
    # 进行数据清理
    df['keyword'] = df['keyword'].map(lambda e: e.split('：')[1].split())
    # df['source'] = df['source'].map(lambda e: e.split())
    df[['datetime', 'from']] = df['source'].str.extract('(\d+年\d+月\d+日\d+:\d+)[\t|\n]+?(\w+)', expand=False)
    print(df[['datetime', 'from']])
    # 因为df['datetime']是object格式,为了后期的取值,例：取年df['datetime'].map(lambda e : e.year) 我们需要把格式转换为时间格式
    df['datetime'] = pandas.to_datetime(df['datetime'], format = '%Y年%m月%d日%H:%M')
    del df['source']
    # 对即将保存的格式进行调整
    df = df[['from', 'title', 'content', 'keyword', 'datetime']]
    # 将整理好的数据储存Excel
    df.to_excel('news.xlsx')


if __name__ == '__main__':
    get_all_news()