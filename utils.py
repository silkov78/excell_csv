import sys
import os
import pandas as pd
import logging
from time import sleep


# Common function
def sleep_sep_print(message, sec=0.75, under='-', above=None):
    """
    function prints text with time gap (sec parameter)
    and underline
    """
    sleep(0.5)
    if above:
        print(above * 50)
    print(message)
    if under:
        print(under * 50)


def terminate():
    # function stoping file execution
    print()
    input('Введите Enter для выхода: ')
    sys.exit()


# Executing flow
def city_code_file_reading(base_dir: str, city_code_file: str) -> pd.DataFrame:
    sleep_sep_print('Начало программы:', under=None)
    sleep_sep_print('Поиск файла CITY_CODE.csv', under='=')

    try:
        city_code_df = pd.read_csv(city_code_file, encoding='utf-8', header=None)
        return city_code_df

    except FileNotFoundError:
        print('Файл CITY_CODE.csv не найден в текущей папке.')
        terminate()

    except pd.errors.ParserError:
        print('Неправильный формат CITY_CODE.csv файла.')
        terminate()


def city_code_df_in_dict(city_code_df: pd.DataFrame) -> dict:
    city_code_dict = {}
    for city, code in zip(city_code_df.iloc[:, 0], city_code_df.iloc[:, 1]):
        city_code_dict[city] = code

    sleep_sep_print(city_code_dict, under='')
    return city_code_dict
