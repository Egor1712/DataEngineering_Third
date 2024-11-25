from os import listdir
from os.path import join

from bs4 import BeautifulSoup

from common_data_processor import process_and_save_data

processors = {
    'radius': lambda s: int(s),
    'rotation': lambda s: float(s.split()[0]),
    'age': lambda s: float(s.split()[0]),
    'distance': lambda s: float(s.split()[0]),
    'absolute-magnitude': lambda s: float(s.split()[0])
}


def parse_file(filename):
    with open(filename, encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, "xml")
    star = soup.find('star')
    item = {}
    for child in star.findChildren():
        if child.name in processors:
            item[child.name] = processors[child.name](child.get_text().strip())
        else:
            item[child.name] = child.get_text().strip()
    return item


data = [parse_file(join('./58/3', f)) for f in listdir('./58/3')]
process_and_save_data(data, 'third', 'name', 'constellation', 'distance')
