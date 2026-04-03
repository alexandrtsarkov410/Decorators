import os
from datetime import datetime


def logger(old_function):
    """
    Декоратор для логирования вызовов функции.
    Записывает значение в файл "main.log" и возвращает следующие значения:
    - дату и время вызова;
    - имя;
    - аргументы;
    - возвращаемое значение.
    """
    def new_function(*args, **kwargs):
        # Текущее время
        current_time = datetime.now().strftime('Время вызова: %Y-%m-%d %H:%M:%S')

        # Имя функции
        func_name = old_function.__name__

        # Формирование аргументов
        args_str = ', '.join([str(arg) for arg in args])
        kwargs_str = ', '.join([f'{k}={v}' for k, v in kwargs.items()])
        if args_str and kwargs_str:
            all_args = f"{args_str}, {kwargs_str}"
        else:
            all_args = args_str or kwargs_str

        # Вызов функции
        result = old_function(*args, **kwargs)

        # Форма записи лога
        log_1 = f"{current_time} функции '{func_name}' c аргументами: ({all_args}) -> {result}\n"

        with open('main.log', 'a', encoding='utf-8') as file:
            file.write(log_1)

        return result

    return new_function


def test_1():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()