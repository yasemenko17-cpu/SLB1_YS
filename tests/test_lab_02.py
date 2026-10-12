"""Відкриті тести задачі 2: Розбір зв'язків моделі.

Запуск: pytest tests/test_lab_02.py
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


T02 = [('S1',
  'parse_relationships',
  ('u -> s "Використовує"',),
  [{'src': 'u', 'dst': 's', 'description': 'Використовує', 'technology': '', 'tags': []}]),
 ('S1',
  'parse_relationships',
  ('w -> a "Викликає" "JSON/HTTPS"',),
  [{'src': 'w', 'dst': 'a', 'description': 'Викликає', 'technology': 'JSON/HTTPS', 'tags': []}]),
 ('S1',
  'parse_relationships',
  ('a -> b',),
  [{'src': 'a', 'dst': 'b', 'description': '', 'technology': '', 'tags': []}]),
 ('S2',
  'parse_relationships',
  ('a -> b "A -> B"',),
  [{'src': 'a', 'dst': 'b', 'description': 'A -> B', 'technology': '', 'tags': []}]),
 ('S2',
  'parse_relationships',
  ('a -> b "каже \\"привіт\\""',),
  [{'src': 'a', 'dst': 'b', 'description': 'каже "привіт"', 'technology': '', 'tags': []}]),
 ('S2',
  'parse_relationships',
  ('a -> b "порт #1" "TCP // 80"',),
  [{'src': 'a', 'dst': 'b', 'description': 'порт #1', 'technology': 'TCP // 80', 'tags': []}]),
 ('S3',
  'parse_relationships',
  ('a = container "A" "d" "Py" {\n  this -> b "x"\n}',),
  [{'src': 'a', 'dst': 'b', 'description': 'x', 'technology': '', 'tags': []}]),
 ('S3',
  'parse_relationships',
  ('a = container "A" "d" "Py" {\n  -> b "x" "T"\n}',),
  [{'src': 'a', 'dst': 'b', 'description': 'x', 'technology': 'T', 'tags': []}]),
 ('S3', 'parse_relationships', ('-> b',), ValueError("Неповний зв'язок: -> b"))]


@pytest.mark.parametrize("tag,fn,args,expected", T02, ids=_ids(T02, "T02"))
def test_task_02(tag, fn, args, expected):
    run(2, fn, args, expected)
