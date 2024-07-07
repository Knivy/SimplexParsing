# -*- coding: utf-8 -*-
import time

from bs4 import BeautifulSoup  # type: ignore
from enum import Enum
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import Select


class Sign(Enum):
    """Виды знаков."""

    LE = '<='
    EQ = '='
    GE = '>='


def get_number_variables(left):
    """Получение количества переменных."""
    if not left or not len(left):
        raise ValueError('left не должен быть пустым.')
    if type(left) not in (list, tuple):
        raise TypeError('left должен быть списком или кортежем.')
    row_len = len(left[0])
    if not 2 <= row_len <= 10:
        raise ValueError('Количество переменных должно быть от 2 до 10.')
    for row in left:
        if type(row) not in (list, tuple):
            raise TypeError('Элементы left должны быть списком или кортежем.')
        if len(row) != row_len:
            raise ValueError('Строки left должны быть одинаковой длины.')
    return row_len


def get_number_rows(left):
    """Получение количества строк."""
    number_rows = len(left)
    if not 1 <= number_rows <= 10:
        raise ValueError('Количество строк в left должно быть от 1 до 10.')
    return number_rows


def open_browser(wait=5):
    """Открыть браузер Firefox."""
    driver = webdriver.Firefox(
        service=Service(executable_path=GeckoDriverManager().install()))
    driver.implicitly_wait(wait)
    return driver


def parse_first_page(driver, number_variables, number_rows, page_height=1080):
    """Парсинг первой страницы."""
    driver.execute_script(f'window.scrollTo(0, {page_height})')
    (driver.find_element(
        'xpath',
        f'//select[@name="kolPR"]/option[text()={str(number_variables)}]')
        .click())
    time.sleep(1)
    (driver.find_element(
        'xpath',
        f'//select[@name="kolSTR"]/option[text()={str(number_rows)}]')
        .click())
    time.sleep(1)
    driver.execute_script(f'window.scrollTo(0, {page_height})')
    (driver.find_element(
        'css selector', '.btn-lg.btn-primary')
        .click())
    time.sleep(3)


def get_usl_value(signs_value):
    """Конвертировать значение знака."""
    if signs_value == '>=':
        return '1'
    elif signs_value == '<=':
        return '2'
    else:
        return '0'


def change_value(element, value):
    """Изменить значение."""
    element.clear()
    element.send_keys(value)


def parse_second_page(driver, left, right, signs, number_variables,
                      number_rows, func, is_max, page_height=1080):
    """Парсинг второй страницы."""
    driver.execute_script(f'window.scrollTo(0, {0.7 * page_height})')
    for row in range(1, number_rows + 1):
        for element in range(1, number_variables + 1):
            name = 'm' + str(row) + str(element)
            input_element = (driver.find_element(
                             'xpath', f'//input[@name="{name}"]'))
            change_value(input_element,
                         str(left[row - 1][element - 1]))
            driver.execute_script(f'window.scrollTo(0, {0.7 * page_height})')
        input_element = Select(driver.find_element(
                         'css selector', f'#usl{row}'))
        input_element.select_by_value(get_usl_value(signs[row - 1].value))
        input_element = (driver.find_element(
                         'xpath', f'//input[@name="r{row}"]'))
        change_value(input_element, str(right[row - 1]))
    for element in range(1, number_variables + 1):
        input_element = (driver.find_element(
                         'xpath', f'//input[@name="fx{element}"]'))
        change_value(input_element, str(func[element - 1]))
    if len(func) > number_variables:
        input_element = (driver.find_element(
                         'xpath',
                         f'//input[@name="fx{number_variables + 1}"]'))
        change_value(input_element, str(func[number_variables]))
    if is_max:
        (driver.find_element(
            'xpath', '//select[@name="vid"]/option[text()="max"]')
            .click())
    else:
        (driver.find_element(
            'xpath', '//select[@name="vid"]/option[text()="min"]')
            .click())
    time.sleep(1)
    driver.execute_script(f'window.scrollTo('
                          f'{2 * page_height}, {4 * page_height})')
    (driver.find_element(
        'css selector', '#stepprev')
        .click())
    time.sleep(5)
    return driver.page_source


def check_variables(func, number_variables, number_rows,
                    right, signs, is_max):
    """Проверить входные данные."""
    # func
    if not func or not len(func):
        raise ValueError('func не должен быть пустым.')
    if type(func) not in (list, tuple):
        raise TypeError('func должен быть списком или кортежем.')
    if len(func) not in (number_variables, number_variables + 1):
        raise ValueError('Количество элементов в func должно быть '
                         'равно количеству переменных.')
    for element in func:
        if not isinstance(element, int):
            raise TypeError('Элемент func должен быть int.')
    # right
    if not right or not len(right):
        raise ValueError('right не должен быть пустым.')
    if type(right) not in (list, tuple):
        raise TypeError('right должен быть списком или кортежем.')
    if len(right) != number_rows:
        raise ValueError('Количество элементов в right должно быть '
                         'равно количеству строк.')
    for element in right:
        if not isinstance(element, int):
            raise TypeError('Элемент right должен быть int.')
    # signs
    if not signs or not len(signs):
        raise ValueError('signs не должен быть пустым.')
    if type(signs) not in (list, tuple):
        raise TypeError('signs должен быть списком или кортежем.')
    if len(signs) != number_rows:
        raise ValueError('Количество элементов в signs должно быть '
                         'равно количеству строк.')
    for element in signs:
        if not isinstance(element, Sign):
            raise TypeError('Элемент signs должен быть Sign.')
    # is_max
    if not isinstance(is_max, bool):
        raise TypeError('is_max должен быть bool.')


def parse_data(func, left, right, signs, is_max):
    """Парсинг."""
    try:
        # Количество переменных.
        number_variables = get_number_variables(left)

        # Количество строк (количество ограничений).
        number_rows = get_number_rows(left)

        # Проверить входные данные.
        check_variables(func, number_variables, number_rows,
                        right, signs, is_max)

        # Открыть браузер.
        driver = open_browser()

        # Открыть страницу сайта.
        url = 'https://math.semestr.ru/simplex/simplex.php'
        driver.get(url)
        time.sleep(3)

        # Парсинг.
        parse_first_page(driver, number_variables, number_rows)
        page_source = parse_second_page(driver, left, right, signs,
                                        number_variables, number_rows, func,
                                        is_max)
        soup = BeautifulSoup(page_source, 'html.parser')
        return soup.find_all('article', {'class': 'ref_cat'})[0]

    except Exception as error:
        print(f'Ошибка: {error}')
        return

    finally:
        # Ожидание, чтобы визуально оценить результаты прохождения скрипта.
        time.sleep(5)
        # Закрываем браузер.
        driver.quit()


def main():
    """Основная функция."""

    # Значения функции
    func = [7, 8]

    # Задача на максимум или минимум
    is_max = True

    # Значения по левую сторону неравенства
    left = [
        [10, 2],
        [35, 4],
    ]

    # Значения по правую сторону неравенства
    right = [
        5,
        6,
    ]

    # Знаки неравенств
    signs = [
        Sign.LE,
        Sign.GE,
    ]

    html = parse_data(func, left, right, signs, is_max)

    print(html)


if __name__ == '__main__':
    main()
