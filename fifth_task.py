import re
import requests
from bs4 import BeautifulSoup

from common_data_processor import process_and_save_data


def parse_page(page_number):
    response = requests.get(f'https://www.e1.ru/text/?page={page_number}')
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', attrs={'data-test': 'archive-record-item'})
    items = []
    for article in articles:
        item = {}
        item['rubric'] = article.find_next('div', attrs={'class': 'Zrw4X'}).get_text().strip()
        item['title'] = article.find_next('h2', attrs={'class': 'h9Jmx'}).get_text().strip()
        item['comment'] = article.find_next('div', attrs={'class': 'TdYOd'}).get_text().strip()
        item['reviews'] = int(
            re.sub("[^0-9]", "", article.find_next('span', attrs={'class': '_3mETe'}).get_text().strip()))
        item['comments'] = int(
            re.sub("[^0-9]", "", article.find_next('span', attrs={'class': '_3mETe'}).get_text().strip()))
        date_time = article.find_next('div', attrs={'class': 'Hiu4B vx3Rq'}).get_text().strip()
        item['date'] = date_time.split(',')[0].strip()
        item['time'] = date_time.split(',')[1].strip()
        item['link'] = article.find_next('h2', attrs={'class': 'h9Jmx'}).next['href']
        print(item)
        items.append(item)
    return items


def parse_news_page(link):
    response = requests.get(f'https://www.e1.ru/{link}')
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    item = {}
    title = soup.find('h1', attrs={'class': 'title_ip27z'})
    if title is not None:
        item['title'] = title.get_text().strip()
    else:
        return None
    description = soup.find('p', attrs={'class': 'leadParagraph_ip27z'})
    if description is not None:
        item['description'] = description.get_text().strip()
    items_count = soup.find('span', attrs={'class': 'counter_sZXgN'})
    item['comments_count'] = 0 if items_count is None else  int(items_count.get_text().strip())

    body  = soup.find('div', attrs={'class': 'articleContent_fefJj'})
    if body is not None:
        item['body'] = body.get_text().strip()
    another_articles = soup.find_all('li', attrs={'class': 'item_Jrapc'})
    if another_articles is not  None:
        item['articles'] = [article.get_text() for article in another_articles]

    author_name = soup.find('a', attrs={'class': 'link_GQmWc'})
    author_profession = soup.find('span', attrs={'class': 'profession_GQmWc'})
    item['author_name'] = "no_author" if author_name is None else author_name.get_text().strip()
    item['author_profession'] = None if author_profession is None else author_profession.get_text().strip()
    print(item)
    return item


news = []
for i in range(0, 20):
    for item in parse_page(i):
        news.append(item)

process_and_save_data(news, "fifth_task_news_from_list", 'date', 'rubric', 'reviews')

news_from_pages = []
for i in range(0, 100):
    link = news[i]['link']
    item = parse_news_page(link)
    if item is not None:
        news_from_pages.append(item)

process_and_save_data(news_from_pages, "fifth_task_news_from_pages", 'title', 'author_name', 'comments_count')


