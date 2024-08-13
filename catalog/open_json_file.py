import json


def open_json_file():
    """
    Возвращает список недопустимых слов для последующей проверки в ProductForm (clean_product_name, clean_description)
    """
    with open('catalog/clean_words.json', 'r', encoding='utf-8') as clean_words:
        str_data = json.load(clean_words)
        list_data = str_data.split(", ")
        return list_data
