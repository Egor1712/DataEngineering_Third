import json
import sys


def process_and_save_data(data, task_name, sorted_fild_name, frequency_field_name, numerical_filed_name):
    with open(f'./results/{task_name}_task_all_data.json', 'w+', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

    with open(f'./results/{task_name}_task_sorted_data.json', 'w+', encoding='utf-8') as file:
        json.dump(list(sorted(data, key=lambda p: p[sorted_fild_name])), file, ensure_ascii=False)

    properties = {
        'max': 0,
        'min': sys.maxsize,
        'sum': 0,
    }
    frequency = {
    }

    for item in data:
        item_numerical = item[numerical_filed_name]
        item_frequency = item[frequency_field_name].lower()
        if item_frequency in frequency:
            frequency[item_frequency] += 1
        else:
            frequency[item_frequency] = 1
        properties["sum"] += item_numerical
        if item_numerical > properties['max']:
            properties['max'] = item_numerical
        if item_numerical < properties['min']:
            properties['min'] = item_numerical

    properties['avg'] = properties['sum'] / len(data)
    with open(f'./results/{task_name}_task_characteristics.json', 'w+', encoding='utf-8') as file:
        json.dump(properties, file, ensure_ascii=False)

    with open(f'./results/{task_name}_task_{frequency_field_name}_frequency.json', 'w+', encoding='utf-8') as file:
        json.dump(frequency, file, ensure_ascii=False)
