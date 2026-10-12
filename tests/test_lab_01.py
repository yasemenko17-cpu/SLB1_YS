"""Відкриті тести задачі 1: Розбір елементів моделі Structurizr DSL.

Запуск: pytest tests/test_lab_01.py
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


T01 = [('S1',
  'parse_elements',
  ('u = person "Користувач" "Купує товари"',),
  [{'id': 'u',
    'kind': 'person',
    'name': 'Користувач',
    'description': 'Купує товари',
    'technology': '',
    'tags': [],
    'parent': None}]),
 ('S1',
  'parse_elements',
  ('a = softwareSystem "Сайт"',),
  [{'id': 'a',
    'kind': 'softwareSystem',
    'name': 'Сайт',
    'description': '',
    'technology': '',
    'tags': [],
    'parent': None}]),
 ('S1',
  'parse_elements',
  ('\n  u = person "U" "d1"\n\n    s = softwareSystem "S" "d2"\n',),
  [{'id': 'u', 'kind': 'person', 'name': 'U', 'description': 'd1', 'technology': '', 'tags': [], 'parent': None},
   {'id': 's',
    'kind': 'softwareSystem',
    'name': 'S',
    'description': 'd2',
    'technology': '',
    'tags': [],
    'parent': None}]),
 ('S2',
  'parse_elements',
  ('s = softwareSystem "Сайт" "d" {\n'
   '    w = container "Веб" "d" "React"\n'
   '    a = container "API" "d" "Python" "Core"\n'
   '}',),
  [{'id': 's',
    'kind': 'softwareSystem',
    'name': 'Сайт',
    'description': 'd',
    'technology': '',
    'tags': [],
    'parent': None},
   {'id': 'w',
    'kind': 'container',
    'name': 'Веб',
    'description': 'd',
    'technology': 'React',
    'tags': [],
    'parent': 's'},
   {'id': 'a',
    'kind': 'container',
    'name': 'API',
    'description': 'd',
    'technology': 'Python',
    'tags': ['Core'],
    'parent': 's'}]),
 ('S2',
  'parse_elements',
  ('s = softwareSystem "S" {\n  c = container "X"\n}',),
  [{'id': 's',
    'kind': 'softwareSystem',
    'name': 'S',
    'description': '',
    'technology': '',
    'tags': [],
    'parent': None},
   {'id': 'c', 'kind': 'container', 'name': 'X', 'description': '', 'technology': '', 'tags': [], 'parent': 's'}]),
 ('S2',
  'parse_elements',
  ('s = softwareSystem "S" {\n  a = container "A" "d" "Py" {\n    k = component "K" "d" "Py"\n  }\n}',),
  [{'id': 's',
    'kind': 'softwareSystem',
    'name': 'S',
    'description': '',
    'technology': '',
    'tags': [],
    'parent': None},
   {'id': 'a', 'kind': 'container', 'name': 'A', 'description': 'd', 'technology': 'Py', 'tags': [], 'parent': 's'},
   {'id': 'k', 'kind': 'component', 'name': 'K', 'description': 'd', 'technology': 'Py', 'tags': [], 'parent': 'a'}]),
 ('S3', 'parse_elements', ('x = database "DB"',), ValueError('Невідомий тип елемента: database')),
 ('S3', 'parse_elements', ('person "U"',), ValueError('Елемент без ідентифікатора: person "U"')),
 ('S3', 'parse_elements', ('u = person',), ValueError('Елемент без назви: u = person'))]


@pytest.mark.parametrize("tag,fn,args,expected", T01, ids=_ids(T01, "T01"))
def test_task_01(tag, fn, args, expected):
    run(1, fn, args, expected)
