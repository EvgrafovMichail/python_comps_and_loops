import json
import os
import time

from typing import Callable, TypeVar


T = TypeVar("T")

timers: dict[str, Callable[[int], tuple[float, float]]] = {}


def register(
    registry: dict[str, Callable[[int], tuple[float, float]]]
) -> Callable[[T], T]:
    """
    Создает декоратор для регистрации функции в переданный словарь registry.

    Функции будут храниться в словаре в формате:
    {'func_name': func}

    Args:
        registry: словарь, в который будет регистрироваться функция.

    Returns:
        Декоратор для регистрации функции.
    """
    def _register(func):
        registry[func.__name__] = func
        return func

    return _register


@register(timers)
def get_lists_creation_timings(size: int) -> tuple[float, float]:
    """
    Замеряет времена создания списка с помощью цикла и включения.

    Args:
        size: требуемое количество элементов в списке.

    Returns:
        Пару чисел с плавающей точкой:
            - время создания списка с помощью цикла.
            - время создания списка с помощью спискового включения.
    """
    time_start = time.time()
    list_ = []

    for i in range(size):
        list_.append(i)

    timing_loop = time.time() - time_start
    del list_

    time_start = time.time()
    _ = [i for i in range(size)]

    return timing_loop, time.time() - time_start


@register(timers)
def get_dicts_creation_timings(size: int) -> tuple[float, float]:
    """
    Замеряет времена создания словаря с помощью цикла и включения.

    Args:
        size: требуемое количество элементов в словаре.

    Returns:
        Пару чисел с плавающей точкой:
            - время создания словаря с помощью цикла.
            - время создания словаря с помощью словарного включения.
    """
    time_start = time.time()
    dict_ = {}

    for i in range(size):
        dict_[i] = i

    timing_loop = time.time() - time_start
    del dict_

    time_start = time.time()
    _ = {i: i for i in range(size)}

    return timing_loop, time.time() - time_start


@register(timers)
def get_sets_creation_timings(size: int) -> tuple[float, float]:
    """
    Замеряет времена создания множества с помощью цикла и включения.

    Args:
        size: требуемое количество элементов в множестве.

    Returns:
        Пару чисел с плавающей точкой:
            - время создания множества с помощью цикла.
            - время создания множества с помощью множественного включения.
    """
    time_start = time.time()
    set_ = set()

    for i in range(size):
        set_.add(i)

    timing_loop = time.time() - time_start
    del set_

    time_start = time.time()
    _ = {i for i in range(i)}

    return timing_loop, time.time() - time_start


def collect_times(
    timer_id: str,
    range_config: tuple[int, int, int],
    path_to_save_folder: str,
) -> None:
    """
    Собирает зависимость времени создания коллекции от количества элементов.

    Данные собираются в словарь вида:

    {
        'loop': [1., 2., ...],
        'comp': [1., 2., ...],
    }

    Затем этот словарь сохраняется в формате json в папку path_to_save_folder.
    Имя json-файла - имя использованной функции или слово после первого '_'.

    Args:
        timer_id: идентификатор функции для сбора статистик.
            Функция должна быть зарегистрирована в словаре timers.
        range_config: кортеж, содержащий от 1 до 3 целых чисел, которые
            соответствуют параметрам range.
        path_to_save_folder: путь до папки, в которую будет сохранен
            json-файл с собранными временами.

    Raises:
        KeyError, если в словаре timers нет ключа со значением timer_id.
    """
    pid = os.getpid()
    print(
        f"process {pid} start to collect times using "
        f"next timer: {timer_id}"
    )

    if not (timer := timers.get(timer_id)):
        raise KeyError(f"there is no timer with id: {timer_id}")

    times: dict[str, list[float]] = {}

    for size in range(*range_config):
        time_loop, time_comp = timer(size)
        times.setdefault("loop", []).append(time_loop)
        times.setdefault("comp", []).append(time_comp)

    tokens_from_id = timer_id.strip("_").split("_")
    file_name = (
        tokens_from_id[1] if 2 <= len(tokens_from_id) else tokens_from_id[0]
    )
    path_to_file = os.path.join(path_to_save_folder, f"{file_name}.json")

    with open(path_to_file, "w") as file:
        json.dump(times, file, indent=4)

    print(f"process {pid} finished and saved results into: {path_to_file}")
