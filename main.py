import os
import csv
from utils import *

BASE_DIR = os.getcwd()
CITY_CODE_FILE = os.path.join(BASE_DIR, "CITY_CODE.csv")

try:
    city_code_df = city_code_file_reading(BASE_DIR, CITY_CODE_FILE)
    city_code_dict = city_code_df_in_dict(city_code_df)
except Exception:
    sleep_sep_print('ОШИБКА: файл CITY_CODE.csv не читается по неизвестной причине :(')
    terminate()

# фильтрация .xlsx и .xls файлов в директории
try:
    excell_files = list(filter(lambda x: '.xlsx' in x or '.xls' in x, os.listdir()))
    sleep_sep_print(excell_files, under='=')
except Exception:
    sleep_sep_print('ОШИБКА: файлы .lsx и .xlsx не читаются по неизвестной причине :(')

new_file_ctr = 0
for file in excell_files:

    sleep_sep_print(file, sec=0, under='',above='-')

    # file reading validation
    try:
        file_path = os.path.join(BASE_DIR, file)
        file_df = pd.read_excel(file_path)
        file_df = file_df.round(decimals=3)
    except Exception:
        sleep_sep_print(
            f'ОШИБКА: файл {file} не читаются по неизвестной причине :('
        )
        continue

    # required_columns validation
    required_columns = ['Город', 'Станция', 'Дата']
    try:
        file_df_required = file_df[required_columns]
    except KeyError:
        sleep_sep_print(
            f"ОШИБКА: файл {file} не имеет одного или несколько нужных полей ('Дата', 'Город', 'Станция')."
        )
        continue
    except Exception:
        sleep_sep_print(
            f'ОШИБКА: файл {file} имеет нечитабельные поля по неизвестным причинам :('
        )
        continue

    # city validation
    city = file_df['Город'][0]
    try:
        citycode = city_code_dict[city]
    except KeyError:
        print(f'ОШИБКА: город {city} не найден в файле CITY_CODE.csv.')
        continue

    # date validation
    file_df_date = file_df['Дата'][0]
    try:
        pd_file_df_date = pd.to_datetime(file_df_date)
        year = str(pd_file_df_date.year)[-2:]
        month = str(pd_file_df_date.month).zfill(2)
    except pd._libs.tslibs.parsing.DateParseError:
        print(f'ОШИБКА: в первой строке файла {file} дата представлена в непонятном формате: {file_df_date} .')
        continue
    except Exception:
        sleep_sep_print(
            f'ОШИБКА: в первой строке файла {file} дата не читается по неизвестным причинам :('
        )
        continue

    # station validation
    station = str(file_df['Станция'][0]).zfill(2)
    try:
        station = str(file_df['Станция'][0]).zfill(2)
    except Exception:
        sleep_sep_print(
            f'ОШИБКА: в первой строке файла {file} станция не читается по неизвестным причинам :('
        )
        continue

    try:
        # new file
        filename = f'{citycode}{station}{year}{month}.csv'
        filename_path = os.path.join(BASE_DIR, filename)
        
        file_df.to_csv(
            filename_path,
            decimal=',',
            sep=';',
            encoding='cp1251',
            index=False
            )

        new_file_ctr += 1

    except Exception:
        sleep_sep_print(
            f'ОШИБКА: файл {file} не может сохраниться по неизвестным причинам :('
        )
        continue

sleep_sep_print(
    f'Программа завершена: В CSV-формат переведено {new_file_ctr} файлов.',
    above='=', under='='
)
terminate()
