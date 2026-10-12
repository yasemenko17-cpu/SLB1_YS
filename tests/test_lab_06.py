"""Відкриті тести задачі 6: Діаграми в документації Markdown.

Запуск: pytest tests/test_lab_06.py
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


T06 = [('S1',
  'embed_diagrams',
  ('# Архітектура\n\n<!-- diagram:ctx -->\n\nТекст.', {'ctx': 'C4Context\n  title A'}),
  '# Архітектура\n\n<!-- diagram:ctx -->\n```mermaid\nC4Context\n  title A\n```\n<!-- /diagram:ctx -->\n\nТекст.'),
 ('S1',
  'embed_diagrams',
  ('<!-- diagram:ctx -->', {'ctx': 'G'}),
  '<!-- diagram:ctx -->\n```mermaid\nG\n```\n<!-- /diagram:ctx -->'),
 ('S1', 'embed_diagrams', ('Без маркерів\nдва рядки', {'ctx': 'G'}), 'Без маркерів\nдва рядки'),
 ('S2',
  'embed_diagrams',
  ('Вступ\n<!-- diagram:ctx -->\n```mermaid\nСТАРЕ\n```\n<!-- /diagram:ctx -->\nКінець', {'ctx': 'НОВЕ'}),
  'Вступ\n<!-- diagram:ctx -->\n```mermaid\nНОВЕ\n```\n<!-- /diagram:ctx -->\nКінець'),
 ('S2',
  'embed_diagrams',
  ('<!-- diagram:ctx -->\n```mermaid\n1\n2\n3\n4\n```\n<!-- /diagram:ctx -->', {'ctx': 'X'}),
  '<!-- diagram:ctx -->\n```mermaid\nX\n```\n<!-- /diagram:ctx -->'),
 ('S2',
  'embed_diagrams',
  ('<!-- diagram:ctx -->\n```mermaid\nG\n```\n<!-- /diagram:ctx -->', {'ctx': 'G'}),
  '<!-- diagram:ctx -->\n```mermaid\nG\n```\n<!-- /diagram:ctx -->'),
 ('S3', 'embed_diagrams', ('<!-- diagram:zzz -->', {'ctx': 'G'}), ValueError('Немає діаграми: zzz')),
 ('S3',
  'embed_diagrams',
  ('<!-- diagram:ctx -->\n```mermaid\nстаре\n```\nтекст', {'ctx': 'G'}),
  ValueError('Немає закриваючого маркера: ctx')),
 ('S3',
  'embed_diagrams',
  ('<!-- diagram:ctx -->\n```mermaid\nстаре', {'ctx': 'G'}),
  ValueError('Немає закриваючого маркера: ctx'))]


@pytest.mark.parametrize("tag,fn,args,expected", T06, ids=_ids(T06, "T06"))
def test_task_06(tag, fn, args, expected):
    run(6, fn, args, expected)
