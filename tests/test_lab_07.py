"""Відкриті тести задачі 7: Аналіз залежностей між контейнерами.

Запуск: pytest tests/test_lab_07.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import copy
import signal

import pytest
from conftest import load


def _same(a, b):
    """Рівність із допуском для дробових чисел; список і кортеж вважаються однаковими послідовностями."""
    if isinstance(a, float) or isinstance(b, float):
        return isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) < 1e-9
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_same(a[k], b[k]) for k in a)
    return a == b


def run(task, fn, args, expected):
    """Викликає функцію задачі на копії аргументів і порівнює результат; вхідні дані змінювати не можна."""
    func = getattr(load(task), fn)
    given = copy.deepcopy(args)
    if isinstance(expected, ValueError):
        with pytest.raises(ValueError) as info:
            func(*given)
        assert str(info.value) == str(expected)
    else:
        got = func(*given)
        assert _same(got, expected), f"отримано {got!r}, очікувалось {expected!r}"
    assert given == args, "функція не повинна змінювати вхідні дані"


def _ids(cases, prefix):
    return [f"{prefix}-{c[0]}-{i}" for i, c in enumerate(cases)]


@pytest.fixture(autouse=True)
def _watchdog():
    """Тест, що завис (нескінченний цикл), завершується за 10 с."""
    def boom(signum, frame):
        raise TimeoutError("тест завис довше 10 с: перевірте умови завершення циклів")
    old = signal.signal(signal.SIGALRM, boom)
    signal.alarm(10)
    yield
    signal.alarm(0)
    signal.signal(signal.SIGALRM, old)


T07 = [('S1',
  'fan_in_out',
  ([('web', 'api'), ('api', 'db'), ('api', 'pay')],),
  {'api': (1, 2), 'db': (1, 0), 'pay': (1, 0), 'web': (0, 1)}),
 ('S1', 'fan_in_out', ([],), {}),
 ('S1', 'fan_in_out', ([('a', 'b'), ('a', 'b')],), {'a': (0, 1), 'b': (1, 0)}),
 ('S2', 'find_cycles', ([('a', 'b'), ('b', 'c')],), []),
 ('S2', 'find_cycles', ([('a', 'b'), ('b', 'a')],), [['a', 'b']]),
 ('S2', 'find_cycles', ([('a', 'a')],), [['a']]),
 ('S3', 'layers', ([('web', 'api'), ('api', 'db')],), [['web'], ['api'], ['db']]),
 ('S3', 'layers', ([],), []),
 ('S3', 'layers', ([('a', 'c'), ('b', 'c')],), [['a', 'b'], ['c']])]


@pytest.mark.parametrize("tag,fn,args,expected", T07, ids=_ids(T07, "T07"))
def test_task_07(tag, fn, args, expected):
    run(7, fn, args, expected)
