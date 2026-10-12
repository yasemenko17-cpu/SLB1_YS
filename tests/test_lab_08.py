"""Відкриті тести задачі 8: Перевірка записів ADR.

Запуск: pytest tests/test_lab_08.py
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


T08 = [('S1',
  'validate_adr',
  ('# ADR-007: Використати PostgreSQL\n'
   '\n'
   '- Статус: Прийнято\n'
   '- Дата: 2026-03-14\n'
   '\n'
   '## Контекст\n'
   'Потрібні транзакції.\n'
   '\n'
   '## Варіанти\n'
   '- PostgreSQL\n'
   '- MongoDB\n'
   '\n'
   '## Рішення\n'
   'Обрано PostgreSQL.\n'
   '\n'
   '## Наслідки\n'
   '- Плюси: транзакції\n'
   '- Мінуси: складне масштабування\n'
   '- Атрибути якості: Надійність, Ефективність виконання\n',
   {'A01', 'A02'}),
  []),
 ('S1',
  'validate_adr',
  ('ADR-007: без решітки\n'
   '\n'
   '- Статус: Прийнято\n'
   '- Дата: 2026-03-14\n'
   '\n'
   '## Контекст\n'
   'Потрібні транзакції.\n'
   '\n'
   '## Варіанти\n'
   '- PostgreSQL\n'
   '- MongoDB\n'
   '\n'
   '## Рішення\n'
   'Обрано PostgreSQL.\n'
   '\n'
   '## Наслідки\n'
   '- Плюси: транзакції\n'
   '- Мінуси: складне масштабування\n'
   '- Атрибути якості: Надійність, Ефективність виконання\n',
   {'A01', 'A02'}),
  ['A01']),
 ('S1',
  'validate_adr',
  ('# ADR-7: коротке число\n'
   '\n'
   '- Статус: Прийнято\n'
   '- Дата: 2026-03-14\n'
   '\n'
   '## Контекст\n'
   'Потрібні транзакції.\n'
   '\n'
   '## Варіанти\n'
   '- PostgreSQL\n'
   '- MongoDB\n'
   '\n'
   '## Рішення\n'
   'Обрано PostgreSQL.\n'
   '\n'
   '## Наслідки\n'
   '- Плюси: транзакції\n'
   '- Мінуси: складне масштабування\n'
   '- Атрибути якості: Надійність, Ефективність виконання\n',
   {'A01', 'A02'}),
  ['A01']),
 ('S2',
  'validate_adr',
  ('# ADR-007: Використати PostgreSQL\n'
   '\n'
   '- Статус: Прийнято\n'
   '- Дата: 2026-03-14\n'
   '\n'
   '## Контекст\n'
   'Потрібні транзакції.\n'
   '\n'
   '## Варіанти\n'
   '- PostgreSQL\n'
   '- MongoDB\n'
   '\n'
   '## Рішення\n'
   'Обрано PostgreSQL.\n'
   '\n'
   '## Наслідки\n'
   '- Плюси: транзакції\n'
   '- Мінуси: складне масштабування\n'
   '- Атрибути якості: Надійність, Ефективність виконання\n',
   {'A12', 'A11', 'A10'}),
  []),
 ('S2',
  'validate_adr',
  ('# ADR-007: Використати PostgreSQL\n'
   '\n'
   '- Дата: 2026-03-14\n'
   '\n'
   '## Контекст\n'
   'Потрібні транзакції.\n'
   '\n'
   '## Варіанти\n'
   '- PostgreSQL\n'
   '- MongoDB\n'
   '\n'
   '## Рішення\n'
   'Обрано PostgreSQL.\n'
   '\n'
   '## Наслідки\n'
   '- Плюси: транзакції\n'
   '- Мінуси: складне масштабування\n'
   '- Атрибути якості: Надійність, Ефективність виконання\n',
   {'A12', 'A11', 'A10'}),
  ['A10']),
 ('S2',
  'validate_adr',
  ('# ADR-007: Використати PostgreSQL\n'
   '\n'
   '- Статус: Готово\n'
   '- Дата: 2026-03-14\n'
   '\n'
   '## Контекст\n'
   'Потрібні транзакції.\n'
   '\n'
   '## Варіанти\n'
   '- PostgreSQL\n'
   '- MongoDB\n'
   '\n'
   '## Рішення\n'
   'Обрано PostgreSQL.\n'
   '\n'
   '## Наслідки\n'
   '- Плюси: транзакції\n'
   '- Мінуси: складне масштабування\n'
   '- Атрибути якості: Надійність, Ефективність виконання\n',
   {'A12', 'A11', 'A10'}),
  ['A10']),
 ('S3',
  'validate_adr',
  ('# ADR-007: Використати PostgreSQL\n'
   '\n'
   '- Статус: Прийнято\n'
   '- Дата: 2026-03-14\n'
   '\n'
   '## Контекст\n'
   'Потрібні транзакції.\n'
   '\n'
   '## Варіанти\n'
   '- PostgreSQL\n'
   '- MongoDB\n'
   '\n'
   '## Рішення\n'
   'Обрано PostgreSQL.\n'
   '\n'
   '## Наслідки\n'
   '- Плюси: транзакції\n'
   '- Мінуси: складне масштабування\n'
   '- Атрибути якості: Надійність, Ефективність виконання\n',
   {'A21', 'A22', 'A23', 'A20'}),
  []),
 ('S3',
  'validate_adr',
  ('# ADR-007: Використати PostgreSQL\n'
   '\n'
   '- Статус: Прийнято\n'
   '- Дата: 2026-03-14\n'
   '\n'
   '## Контекст\n'
   'Потрібні транзакції.\n'
   '\n'
   '## Варіанти\n'
   '- PostgreSQL\n'
   '\n'
   '## Рішення\n'
   'Обрано PostgreSQL.\n'
   '\n'
   '## Наслідки\n'
   '- Плюси: транзакції\n'
   '- Мінуси: складне масштабування\n'
   '- Атрибути якості: Надійність, Ефективність виконання\n',
   {'A21', 'A22', 'A23', 'A20'}),
  ['A20']),
 ('S3',
  'validate_adr',
  ('# ADR-007: Використати PostgreSQL\n'
   '\n'
   '- Статус: Прийнято\n'
   '- Дата: 2026-03-14\n'
   '\n'
   '## Контекст\n'
   'Потрібні транзакції.\n'
   '\n'
   '## Рішення\n'
   'Обрано PostgreSQL.\n'
   '\n'
   '## Наслідки\n'
   '- Плюси: транзакції\n'
   '- Мінуси: складне масштабування\n'
   '- Атрибути якості: Надійність, Ефективність виконання\n',
   {'A21', 'A22', 'A23', 'A20'}),
  ['A20'])]


@pytest.mark.parametrize("tag,fn,args,expected", T08, ids=_ids(T08, "T08"))
def test_task_08(tag, fn, args, expected):
    run(8, fn, args, expected)
