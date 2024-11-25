import json
import re
import sys
from os import listdir
from os.path import join
from bs4 import BeautifulSoup

from common_data_processor import process_and_save_data


def parse_file(filename):
    with open(filename, encoding='utf-8') as file:
        content = file.read()
    item = {}
    soup = BeautifulSoup(content, "html.parser")
    product_wrapper = soup.find("div", attrs={'class': 'product-wrapper'})
    article_and_availability = product_wrapper.findNext().findNext().get_text()
    index = article_and_availability.index('Наличие')
    item['article'] = article_and_availability[:index].split(':')[1].strip()
    item['availability'] = article_and_availability[index:].split(':')[1].strip().lower() == 'Да'
    item['name'] = product_wrapper.find_all('h1', attrs={'class': ['title']})[0].get_text().split(':')[1].strip()
    address_and_price = product_wrapper.find_all('p', attrs={'class': ['address-price']})[0].get_text()
    price_index = address_and_price.index('Цена')
    item['city'] = address_and_price[:price_index].split(':')[1].strip()
    item['price'] = int(address_and_price[price_index:].split()[1])
    item['color'] = product_wrapper.find_all('span', attrs={'class': ['color']})[0].get_text().split(':')[1].strip()
    item['amount'] = int(
        product_wrapper.find_all('span', attrs={'class': ['quantity']})[0].get_text().split()[1].strip())
    all_spans = product_wrapper.find_all('span')
    item['size'] = all_spans[3].get_text().split(':')[1].strip()
    item['rating'] = float(all_spans[4].get_text().split(':')[1].strip())
    item['views'] = int(all_spans[5].get_text().split(':')[1].strip())
    return item


data = [parse_file(join('./58/1', f)) for f in listdir('./58/1')]

process_and_save_data(data, 'first', 'name', 'city', 'price')