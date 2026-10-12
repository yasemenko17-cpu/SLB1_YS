"""Відкриті тести задачі 3: Перевірка правил C4.

Запуск: pytest tests/test_lab_03.py
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


T03 = [('S1',
  'lint_model',
  ([{'id': 'u', 'kind': 'person', 'name': 'u', 'description': 'd', 'technology': '', 'tags': [], 'parent': None},
    {'id': 's',
     'kind': 'softwareSystem',
     'name': 's',
     'description': 'd',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'w',
     'kind': 'container',
     'name': 'w',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 's'}],
   [],
   {'E001', 'E003', 'E002'}),
  []),
 ('S1',
  'lint_model',
  ([{'id': 'u', 'kind': 'person', 'name': 'u', 'description': '', 'technology': '', 'tags': [], 'parent': None}],
   [],
   {'E001', 'E003', 'E002'}),
  ['E001 u']),
 ('S1',
  'lint_model',
  ([{'id': 'u', 'kind': 'person', 'name': 'u', 'description': '   ', 'technology': '', 'tags': [], 'parent': None}],
   [],
   {'E001', 'E003', 'E002'}),
  ['E001 u']),
 ('S2',
  'lint_model',
  ([{'id': 'u', 'kind': 'person', 'name': 'u', 'description': 'd', 'technology': '', 'tags': [], 'parent': None},
    {'id': 's',
     'kind': 'softwareSystem',
     'name': 's',
     'description': 'd',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'w',
     'kind': 'container',
     'name': 'w',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 's'},
    {'id': 'k',
     'kind': 'component',
     'name': 'k',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 'w'}],
   [],
   {'E011', 'E010'}),
  []),
 ('S2',
  'lint_model',
  ([{'id': 'w',
     'kind': 'container',
     'name': 'w',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': None}],
   [],
   {'E011', 'E010'}),
  ['E010 w']),
 ('S2',
  'lint_model',
  ([{'id': 'u', 'kind': 'person', 'name': 'u', 'description': 'd', 'technology': '', 'tags': [], 'parent': None},
    {'id': 'w',
     'kind': 'container',
     'name': 'w',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 'u'}],
   [],
   {'E011', 'E010'}),
  ['E010 w']),
 ('S3',
  'lint_model',
  ([{'id': 'u', 'kind': 'person', 'name': 'u', 'description': 'd', 'technology': '', 'tags': [], 'parent': None},
    {'id': 's',
     'kind': 'softwareSystem',
     'name': 's',
     'description': 'd',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'w',
     'kind': 'container',
     'name': 'w',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 's'},
    {'id': 'a',
     'kind': 'container',
     'name': 'a',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 's'},
    {'id': 'p',
     'kind': 'softwareSystem',
     'name': 'p',
     'description': 'd',
     'technology': '',
     'tags': [],
     'parent': None}],
   [{'src': 'u', 'dst': 'w', 'description': 'uses', 'technology': '', 'tags': []},
    {'src': 'w', 'dst': 'a', 'description': 'uses', 'technology': '', 'tags': []},
    {'src': 'a', 'dst': 'p', 'description': 'uses', 'technology': '', 'tags': []}],
   {'E020', 'E022', 'E023', 'W030', 'E021', 'E024'}),
  []),
 ('S3',
  'lint_model',
  ([{'id': 'u', 'kind': 'person', 'name': 'u', 'description': 'd', 'technology': '', 'tags': [], 'parent': None},
    {'id': 's',
     'kind': 'softwareSystem',
     'name': 's',
     'description': 'd',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'w',
     'kind': 'container',
     'name': 'w',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 's'},
    {'id': 'a',
     'kind': 'container',
     'name': 'a',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 's'},
    {'id': 'p',
     'kind': 'softwareSystem',
     'name': 'p',
     'description': 'd',
     'technology': '',
     'tags': [],
     'parent': None}],
   [{'src': 'u', 'dst': 'w', 'description': 'uses', 'technology': '', 'tags': []},
    {'src': 'w', 'dst': 'a', 'description': 'uses', 'technology': '', 'tags': []},
    {'src': 'a', 'dst': 'p', 'description': 'uses', 'technology': '', 'tags': []},
    {'src': 'u', 'dst': 'zzz', 'description': 'uses', 'technology': '', 'tags': []}],
   {'E020', 'E022', 'E023', 'W030', 'E021', 'E024'}),
  ['E020 u->zzz']),
 ('S3',
  'lint_model',
  ([{'id': 'u', 'kind': 'person', 'name': 'u', 'description': 'd', 'technology': '', 'tags': [], 'parent': None},
    {'id': 's',
     'kind': 'softwareSystem',
     'name': 's',
     'description': 'd',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'w',
     'kind': 'container',
     'name': 'w',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 's'},
    {'id': 'a',
     'kind': 'container',
     'name': 'a',
     'description': 'd',
     'technology': 'Tech',
     'tags': [],
     'parent': 's'},
    {'id': 'p',
     'kind': 'softwareSystem',
     'name': 'p',
     'description': 'd',
     'technology': '',
     'tags': [],
     'parent': None}],
   [{'src': 'u', 'dst': 'w', 'description': 'uses', 'technology': '', 'tags': []},
    {'src': 'a', 'dst': 'a', 'description': 'uses', 'technology': '', 'tags': []},
    {'src': 'a', 'dst': 'p', 'description': 'uses', 'technology': '', 'tags': []}],
   {'E020', 'E022', 'E023', 'W030', 'E021', 'E024'}),
  ['E021 a->a'])]


@pytest.mark.parametrize("tag,fn,args,expected", T03, ids=_ids(T03, "T03"))
def test_task_03(tag, fn, args, expected):
    run(3, fn, args, expected)
