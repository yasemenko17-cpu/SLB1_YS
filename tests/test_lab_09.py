"""Відкриті тести задачі 9: Сценарії якості.

Запуск: pytest tests/test_lab_09.py
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


T09 = [('S1',
  'parse_scenario',
  ('Джерело: користувач; Стимул: подає запит; Артефакт: API; Середовище: пікове навантаження; Відповідь: повертає '
   'результат; Міра: 95 % запитів за 200 мс',),
  {'source': 'користувач',
   'stimulus': 'подає запит',
   'artifact': 'API',
   'environment': 'пікове навантаження',
   'response': 'повертає результат',
   'measure': '95 % запитів за 200 мс'}),
 ('S1',
  'parse_scenario',
  ('Міра: 1 с; Відповідь: в; Середовище: н; Артефакт: А; Стимул: с; Джерело: д',),
  {'source': 'д', 'stimulus': 'с', 'artifact': 'А', 'environment': 'н', 'response': 'в', 'measure': '1 с'}),
 ('S1',
  'parse_scenario',
  ('Джерело: користувач; Стимул: подає запит; Артефакт: API; Відповідь: повертає результат; Міра: 95 % запитів за '
   '200 мс',),
  ValueError('Немає частини: Середовище')),
 ('S2', 'parse_measure', ('200 мс',), (0.2, 'с')),
 ('S2', 'parse_measure', ('2 с',), (2.0, 'с')),
 ('S2', 'parse_measure', ('5 хв',), (300.0, 'с')),
 ('S3',
  'check_traceability',
  ([{'id': 'Q1', 'artifact': 'API'}, {'id': 'Q2', 'artifact': 'Веб'}],
   [{'id': 'shop',
     'kind': 'softwareSystem',
     'name': 'shop',
     'description': 'd',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'web',
     'kind': 'container',
     'name': 'Веб',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 'shop'},
    {'id': 'api',
     'kind': 'container',
     'name': 'API',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 'shop'},
    {'id': 'db',
     'kind': 'container',
     'name': 'База даних',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 'shop'},
    {'id': 'k',
     'kind': 'component',
     'name': 'Контролер',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 'api'}]),
  {'unknown': [], 'uncovered': ['db']}),
 ('S3',
  'check_traceability',
  ([{'id': 'Q1', 'artifact': 'api'}, {'id': 'Q2', 'artifact': 'web'}, {'id': 'Q3', 'artifact': 'db'}],
   [{'id': 'shop',
     'kind': 'softwareSystem',
     'name': 'shop',
     'description': 'd',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'web',
     'kind': 'container',
     'name': 'Веб',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 'shop'},
    {'id': 'api',
     'kind': 'container',
     'name': 'API',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 'shop'},
    {'id': 'db',
     'kind': 'container',
     'name': 'База даних',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 'shop'},
    {'id': 'k',
     'kind': 'component',
     'name': 'Контролер',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 'api'}]),
  {'unknown': [], 'uncovered': []}),
 ('S3',
  'check_traceability',
  ([{'id': 'Q1', 'artifact': 'Кеш'}],
   [{'id': 'shop',
     'kind': 'softwareSystem',
     'name': 'shop',
     'description': 'd',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'web',
     'kind': 'container',
     'name': 'Веб',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 'shop'},
    {'id': 'api',
     'kind': 'container',
     'name': 'API',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 'shop'},
    {'id': 'db',
     'kind': 'container',
     'name': 'База даних',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 'shop'},
    {'id': 'k',
     'kind': 'component',
     'name': 'Контролер',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 'api'}]),
  {'unknown': ['Q1'], 'uncovered': ['api', 'db', 'web']})]


@pytest.mark.parametrize("tag,fn,args,expected", T09, ids=_ids(T09, "T09"))
def test_task_09(tag, fn, args, expected):
    run(9, fn, args, expected)
