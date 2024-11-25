from os import listdir
from os.path import join
from bs4 import BeautifulSoup

from common_data_processor import process_and_save_data

processors = {
    'id': lambda s: int(s),
    'price': lambda s: int(s.split()[0]),
    'rating': lambda s: float(s.split()[0]),
    'reviews': lambda s: int(s.split()[0]),
    'new': lambda s: s.lower() == '+',
    'exclusive': lambda s: s.lower() == 'yes',
    'sporty': lambda s: s.lower() == 'yes',
}


def parse_file(filename):
    with open(filename, encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, "xml")
    clothes = soup.find_all('clothing')
    items = []
    for closing in clothes:
        item = {}
        for child in closing.findChildren():
            if child.name in processors:
                item[child.name] = processors[child.name](child.get_text().strip())
            else:
                item[child.name] = child.get_text().strip()
        items.append(item)

    return items


data = []
for f in listdir('./58/4'):
    for item in parse_file(join('./58/4', f)):
        data.append(item)

process_and_save_data(data, 'fourth', 'price', 'size', 'reviews')
