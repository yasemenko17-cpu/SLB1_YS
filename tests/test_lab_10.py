"""Відкриті тести задачі 10: Порівняння версій моделі.

Запуск: pytest tests/test_lab_10.py
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


T10 = [('S1',
  'diff_elements',
  ([{'id': 'a', 'kind': 'person', 'name': 'a', 'description': 'd', 'technology': '', 'tags': [], 'parent': None},
    {'id': 'b', 'kind': 'person', 'name': 'b', 'description': 'd', 'technology': '', 'tags': [], 'parent': None}],
   [{'id': 'a', 'kind': 'person', 'name': 'a', 'description': 'd', 'technology': '', 'tags': [], 'parent': None},
    {'id': 'b', 'kind': 'person', 'name': 'b', 'description': 'd', 'technology': '', 'tags': [], 'parent': None},
    {'id': 'c', 'kind': 'person', 'name': 'c', 'description': 'd', 'technology': '', 'tags': [], 'parent': None}]),
  {'added': ['c'], 'removed': []}),
 ('S1',
  'diff_elements',
  ([{'id': 'a', 'kind': 'person', 'name': 'a', 'description': 'd', 'technology': '', 'tags': [], 'parent': None},
    {'id': 'b', 'kind': 'person', 'name': 'b', 'description': 'd', 'technology': '', 'tags': [], 'parent': None}],
   [{'id': 'b', 'kind': 'person', 'name': 'b', 'description': 'd', 'technology': '', 'tags': [], 'parent': None}]),
  {'added': [], 'removed': ['a']}),
 ('S1',
  'diff_elements',
  ([{'id': 'a', 'kind': 'person', 'name': 'a', 'description': 'd', 'technology': '', 'tags': [], 'parent': None}],
   [{'id': 'a', 'kind': 'person', 'name': 'a', 'description': 'd', 'technology': '', 'tags': [], 'parent': None}]),
  {'added': [], 'removed': []}),
 ('S2',
  'changed_elements',
  ([{'id': 'a', 'kind': 'person', 'name': 'a', 'description': 'd', 'technology': '', 'tags': [], 'parent': None}],
   [{'id': 'a', 'kind': 'person', 'name': 'a', 'description': 'd', 'technology': '', 'tags': [], 'parent': None}]),
  {}),
 ('S2',
  'changed_elements',
  ([{'id': 'a', 'kind': 'person', 'name': 'Старе', 'description': 'd', 'technology': '', 'tags': [], 'parent': None}],
   [{'id': 'a', 'kind': 'person', 'name': 'Нове', 'description': 'd', 'technology': '', 'tags': [], 'parent': None}]),
  {'a': ['name']}),
 ('S2',
  'changed_elements',
  ([{'id': 'a', 'kind': 'person', 'name': 'a', 'description': '1', 'technology': '', 'tags': [], 'parent': None}],
   [{'id': 'a', 'kind': 'person', 'name': 'a', 'description': '2', 'technology': '', 'tags': [], 'parent': None}]),
  {'a': ['description']}),
 ('S3',
  'diff_relationships',
  ([{'src': 'a', 'dst': 'b', 'description': 'uses', 'technology': '', 'tags': []}],
   [{'src': 'a', 'dst': 'b', 'description': 'uses', 'technology': '', 'tags': []}]),
  {'added': [], 'removed': [], 'changed': []}),
 ('S3',
  'diff_relationships',
  ([{'src': 'a', 'dst': 'b', 'description': 'uses', 'technology': '', 'tags': []}],
   [{'src': 'a', 'dst': 'b', 'description': 'uses', 'technology': '', 'tags': []},
    {'src': 'b', 'dst': 'c', 'description': 'uses', 'technology': '', 'tags': []}]),
  {'added': [('b', 'c')], 'removed': [], 'changed': []}),
 ('S3',
  'diff_relationships',
  ([{'src': 'a', 'dst': 'b', 'description': 'uses', 'technology': '', 'tags': []},
    {'src': 'b', 'dst': 'c', 'description': 'uses', 'technology': '', 'tags': []}],
   [{'src': 'a', 'dst': 'b', 'description': 'uses', 'technology': '', 'tags': []}]),
  {'added': [], 'removed': [('b', 'c')], 'changed': []})]


@pytest.mark.parametrize("tag,fn,args,expected", T10, ids=_ids(T10, "T10"))
def test_task_10(tag, fn, args, expected):
    run(10, fn, args, expected)
