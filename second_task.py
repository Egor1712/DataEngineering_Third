import json
import re
import sys
from os import listdir
from os.path import join
from bs4 import BeautifulSoup

from common_data_processor import process_and_save_data

name_regex = re.compile('(\d*\.\d*)" (.*) (\d*)GB')

value_processors = {
    'processor': lambda s: {'cpu_count': int(s.split(' ')[0].split('x')[0]), 'cpu_frequency': float(s.split(' ')[0].split('x')[1])},
    'camera': lambda s: {'megapixels_count': int(s.split()[0])},
    'sim': lambda s: {'sim_count': int(s.split()[0])},
    'acc': lambda s: {'acc': int(s.split()[0])}
}

def parse_file(filename):
    with open(filename, encoding='utf-8') as file:
        content = file.read()
    items = []
    soup = BeautifulSoup(content, "html.parser")
    pads = soup.find_all('div', attrs={'class': 'product-item'})
    for pad in pads:
        item = {}
        name = pad.find_next('span').get_text().strip()
        result = name_regex.findall(name)[0]
        item['diagonal'] = float(result[0].strip())
        item['firm'] = result[1].strip()
        item['space'] = int(result[2])
        item['price'] =  int(pad.find_next('price').get_text().strip().replace('₽', '').replace(' ', ''))
        item['bonus'] =  int(pad.find_next('strong').get_text().strip().split()[2])
        props  = pad.find_next('ul')
        for prop in props.findChildren():
            tag = prop['type']
            if tag in value_processors:
                obj =  value_processors[tag](prop.get_text().strip())
                for key, value in obj.items():
                    item[key] = value
        items.append(item)

    return items


data = []
for f in listdir('./58/2'):
    for item in parse_file(join('./58/2', f)):
        data.append(item)

process_and_save_data(data, 'second', 'firm', 'firm', 'space')