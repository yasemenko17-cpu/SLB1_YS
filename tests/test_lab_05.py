"""Відкриті тести задачі 5: Експорт подання у Mermaid.

Запуск: pytest tests/test_lab_05.py
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


T05 = [('S1',
  'to_mermaid',
  ([{'id': 'customer',
     'kind': 'person',
     'name': 'Покупець',
     'description': 'Купує товари',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'admin',
     'kind': 'person',
     'name': 'Адміністратор',
     'description': 'Керує каталогом',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'shop',
     'kind': 'softwareSystem',
     'name': 'Інтернет-магазин',
     'description': 'Продає товари онлайн',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'pay',
     'kind': 'softwareSystem',
     'name': 'Платіжний шлюз',
     'description': 'Приймає платежі',
     'technology': '',
     'tags': ['Зовнішня'],
     'parent': None},
    {'id': 'mail',
     'kind': 'softwareSystem',
     'name': 'Поштова служба',
     'description': 'Доставляє листи',
     'technology': '',
     'tags': ['Зовнішня'],
     'parent': None},
    {'id': 'web',
     'kind': 'container',
     'name': 'Веб-застосунок',
     'description': 'Інтерфейс покупця',
     'technology': 'React',
     'tags': [],
     'parent': 'shop'},
    {'id': 'api',
     'kind': 'container',
     'name': 'API',
     'description': 'Бізнес-логіка',
     'technology': 'Python',
     'tags': [],
     'parent': 'shop'},
    {'id': 'db',
     'kind': 'container',
     'name': 'База даних',
     'description': 'Зберігає замовлення',
     'technology': 'PostgreSQL',
     'tags': ['База даних'],
     'parent': 'shop'},
    {'id': 'ctrl',
     'kind': 'component',
     'name': 'Контролер замовлень',
     'description': 'Приймає запити',
     'technology': 'FastAPI',
     'tags': [],
     'parent': 'api'},
    {'id': 'svc',
     'kind': 'component',
     'name': 'Сервіс замовлень',
     'description': 'Правила замовлень',
     'technology': 'Python',
     'tags': [],
     'parent': 'api'},
    {'id': 'repo',
     'kind': 'component',
     'name': 'Репозиторій',
     'description': 'Доступ до даних',
     'technology': 'SQLAlchemy',
     'tags': [],
     'parent': 'api'}],
   {'elements': ['customer', 'admin', 'shop', 'pay', 'mail'],
    'relationships': [('customer', 'shop', 'Переглядає товари'),
                      ('admin', 'shop', 'Керує каталогом'),
                      ('shop', 'pay', 'Проводить платіж; Платіж'),
                      ('shop', 'mail', 'Надсилає листи')]},
   'context',
   'shop'),
  'C4Context\n'
  '  title Системний контекст: Інтернет-магазин\n'
  '  Person(customer, "Покупець", "Купує товари")\n'
  '  Person(admin, "Адміністратор", "Керує каталогом")\n'
  '  System(shop, "Інтернет-магазин", "Продає товари онлайн")\n'
  '  System_Ext(pay, "Платіжний шлюз", "Приймає платежі")\n'
  '  System_Ext(mail, "Поштова служба", "Доставляє листи")\n'
  '  Rel(customer, shop, "Переглядає товари")\n'
  '  Rel(admin, shop, "Керує каталогом")\n'
  '  Rel(shop, pay, "Проводить платіж; Платіж")\n'
  '  Rel(shop, mail, "Надсилає листи")'),
 ('S1',
  'to_mermaid',
  ([{'id': 'reader',
     'kind': 'person',
     'name': 'Читач',
     'description': 'Шукає книги',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'lib',
     'kind': 'softwareSystem',
     'name': 'Бібліотека',
     'description': 'Облік фонду',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'cat',
     'kind': 'softwareSystem',
     'name': 'Зовнішній каталог',
     'description': 'Каталог видавців',
     'technology': '',
     'tags': ['Зовнішня'],
     'parent': None},
    {'id': 'app',
     'kind': 'container',
     'name': 'Застосунок',
     'description': 'Пошук і видача',
     'technology': 'Django',
     'tags': [],
     'parent': 'lib'},
    {'id': 'store',
     'kind': 'container',
     'name': 'Сховище',
     'description': 'Записи про книги',
     'technology': 'SQLite',
     'tags': ['База даних'],
     'parent': 'lib'}],
   {'elements': ['reader', 'lib', 'cat'],
    'relationships': [('reader', 'lib', 'Шукає книги'), ('lib', 'cat', 'Імпортує описи')]},
   'context',
   'lib'),
  'C4Context\n'
  '  title Системний контекст: Бібліотека\n'
  '  Person(reader, "Читач", "Шукає книги")\n'
  '  System(lib, "Бібліотека", "Облік фонду")\n'
  '  System_Ext(cat, "Зовнішній каталог", "Каталог видавців")\n'
  '  Rel(reader, lib, "Шукає книги")\n'
  '  Rel(lib, cat, "Імпортує описи")'),
 ('S1',
  'to_mermaid',
  ([{'id': 's',
     'kind': 'softwareSystem',
     'name': 'Сайт',
     'description': '',
     'technology': '',
     'tags': [],
     'parent': None}],
   {'elements': ['s'], 'relationships': []},
   'context',
   's'),
  'C4Context\n  title Системний контекст: Сайт\n  System(s, "Сайт", "")'),
 ('S2',
  'to_mermaid',
  ([{'id': 'customer',
     'kind': 'person',
     'name': 'Покупець',
     'description': 'Купує товари',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'admin',
     'kind': 'person',
     'name': 'Адміністратор',
     'description': 'Керує каталогом',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'shop',
     'kind': 'softwareSystem',
     'name': 'Інтернет-магазин',
     'description': 'Продає товари онлайн',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'pay',
     'kind': 'softwareSystem',
     'name': 'Платіжний шлюз',
     'description': 'Приймає платежі',
     'technology': '',
     'tags': ['Зовнішня'],
     'parent': None},
    {'id': 'mail',
     'kind': 'softwareSystem',
     'name': 'Поштова служба',
     'description': 'Доставляє листи',
     'technology': '',
     'tags': ['Зовнішня'],
     'parent': None},
    {'id': 'web',
     'kind': 'container',
     'name': 'Веб-застосунок',
     'description': 'Інтерфейс покупця',
     'technology': 'React',
     'tags': [],
     'parent': 'shop'},
    {'id': 'api',
     'kind': 'container',
     'name': 'API',
     'description': 'Бізнес-логіка',
     'technology': 'Python',
     'tags': [],
     'parent': 'shop'},
    {'id': 'db',
     'kind': 'container',
     'name': 'База даних',
     'description': 'Зберігає замовлення',
     'technology': 'PostgreSQL',
     'tags': ['База даних'],
     'parent': 'shop'},
    {'id': 'ctrl',
     'kind': 'component',
     'name': 'Контролер замовлень',
     'description': 'Приймає запити',
     'technology': 'FastAPI',
     'tags': [],
     'parent': 'api'},
    {'id': 'svc',
     'kind': 'component',
     'name': 'Сервіс замовлень',
     'description': 'Правила замовлень',
     'technology': 'Python',
     'tags': [],
     'parent': 'api'},
    {'id': 'repo',
     'kind': 'component',
     'name': 'Репозиторій',
     'description': 'Доступ до даних',
     'technology': 'SQLAlchemy',
     'tags': [],
     'parent': 'api'}],
   {'elements': ['customer', 'admin', 'pay', 'mail', 'web', 'api', 'db'],
    'relationships': [('customer', 'web', 'Переглядає товари'),
                      ('admin', 'web', 'Керує каталогом'),
                      ('web', 'api', 'Викликає API'),
                      ('api', 'db', 'Читає і пише; SQL'),
                      ('api', 'pay', 'Проводить платіж; Платіж'),
                      ('api', 'mail', 'Надсилає листи')]},
   'container',
   'shop'),
  'C4Container\n'
  '  title Контейнери: Інтернет-магазин\n'
  '  Person(customer, "Покупець", "Купує товари")\n'
  '  Person(admin, "Адміністратор", "Керує каталогом")\n'
  '  System_Ext(pay, "Платіжний шлюз", "Приймає платежі")\n'
  '  System_Ext(mail, "Поштова служба", "Доставляє листи")\n'
  '  System_Boundary(shop, "Інтернет-магазин") {\n'
  '    Container(web, "Веб-застосунок", "React", "Інтерфейс покупця")\n'
  '    Container(api, "API", "Python", "Бізнес-логіка")\n'
  '    ContainerDb(db, "База даних", "PostgreSQL", "Зберігає замовлення")\n'
  '  }\n'
  '  Rel(customer, web, "Переглядає товари")\n'
  '  Rel(admin, web, "Керує каталогом")\n'
  '  Rel(web, api, "Викликає API")\n'
  '  Rel(api, db, "Читає і пише; SQL")\n'
  '  Rel(api, pay, "Проводить платіж; Платіж")\n'
  '  Rel(api, mail, "Надсилає листи")'),
 ('S2',
  'to_mermaid',
  ([{'id': 'reader',
     'kind': 'person',
     'name': 'Читач',
     'description': 'Шукає книги',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'lib',
     'kind': 'softwareSystem',
     'name': 'Бібліотека',
     'description': 'Облік фонду',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'cat',
     'kind': 'softwareSystem',
     'name': 'Зовнішній каталог',
     'description': 'Каталог видавців',
     'technology': '',
     'tags': ['Зовнішня'],
     'parent': None},
    {'id': 'app',
     'kind': 'container',
     'name': 'Застосунок',
     'description': 'Пошук і видача',
     'technology': 'Django',
     'tags': [],
     'parent': 'lib'},
    {'id': 'store',
     'kind': 'container',
     'name': 'Сховище',
     'description': 'Записи про книги',
     'technology': 'SQLite',
     'tags': ['База даних'],
     'parent': 'lib'}],
   {'elements': ['reader', 'cat', 'app', 'store'],
    'relationships': [('reader', 'app', 'Шукає книги'),
                      ('app', 'store', 'Читає записи'),
                      ('app', 'cat', 'Імпортує описи')]},
   'container',
   'lib'),
  'C4Container\n'
  '  title Контейнери: Бібліотека\n'
  '  Person(reader, "Читач", "Шукає книги")\n'
  '  System_Ext(cat, "Зовнішній каталог", "Каталог видавців")\n'
  '  System_Boundary(lib, "Бібліотека") {\n'
  '    Container(app, "Застосунок", "Django", "Пошук і видача")\n'
  '    ContainerDb(store, "Сховище", "SQLite", "Записи про книги")\n'
  '  }\n'
  '  Rel(reader, app, "Шукає книги")\n'
  '  Rel(app, store, "Читає записи")\n'
  '  Rel(app, cat, "Імпортує описи")'),
 ('S2',
  'to_mermaid',
  ([{'id': 's',
     'kind': 'softwareSystem',
     'name': 'С',
     'description': 'd',
     'technology': '',
     'tags': [],
     'parent': None}],
   {'elements': [], 'relationships': []},
   'container',
   's'),
  'C4Container\n  title Контейнери: С\n  System_Boundary(s, "С") {\n  }'),
 ('S3',
  'to_mermaid',
  ([{'id': 'customer',
     'kind': 'person',
     'name': 'Покупець',
     'description': 'Купує товари',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'admin',
     'kind': 'person',
     'name': 'Адміністратор',
     'description': 'Керує каталогом',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'shop',
     'kind': 'softwareSystem',
     'name': 'Інтернет-магазин',
     'description': 'Продає товари онлайн',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'pay',
     'kind': 'softwareSystem',
     'name': 'Платіжний шлюз',
     'description': 'Приймає платежі',
     'technology': '',
     'tags': ['Зовнішня'],
     'parent': None},
    {'id': 'mail',
     'kind': 'softwareSystem',
     'name': 'Поштова служба',
     'description': 'Доставляє листи',
     'technology': '',
     'tags': ['Зовнішня'],
     'parent': None},
    {'id': 'web',
     'kind': 'container',
     'name': 'Веб-застосунок',
     'description': 'Інтерфейс покупця',
     'technology': 'React',
     'tags': [],
     'parent': 'shop'},
    {'id': 'api',
     'kind': 'container',
     'name': 'API',
     'description': 'Бізнес-логіка',
     'technology': 'Python',
     'tags': [],
     'parent': 'shop'},
    {'id': 'db',
     'kind': 'container',
     'name': 'База даних',
     'description': 'Зберігає замовлення',
     'technology': 'PostgreSQL',
     'tags': ['База даних'],
     'parent': 'shop'},
    {'id': 'ctrl',
     'kind': 'component',
     'name': 'Контролер замовлень',
     'description': 'Приймає запити',
     'technology': 'FastAPI',
     'tags': [],
     'parent': 'api'},
    {'id': 'svc',
     'kind': 'component',
     'name': 'Сервіс замовлень',
     'description': 'Правила замовлень',
     'technology': 'Python',
     'tags': [],
     'parent': 'api'},
    {'id': 'repo',
     'kind': 'component',
     'name': 'Репозиторій',
     'description': 'Доступ до даних',
     'technology': 'SQLAlchemy',
     'tags': [],
     'parent': 'api'}],
   {'elements': ['pay', 'db', 'ctrl', 'svc', 'repo'],
    'relationships': [('ctrl', 'svc', 'Передає замовлення'),
                      ('svc', 'repo', 'Зберігає'),
                      ('repo', 'db', 'SQL'),
                      ('svc', 'pay', 'Платіж')]},
   'component',
   'api'),
  'C4Component\n'
  '  title Компоненти: API\n'
  '  System_Ext(pay, "Платіжний шлюз", "Приймає платежі")\n'
  '  ContainerDb(db, "База даних", "PostgreSQL", "Зберігає замовлення")\n'
  '  Container_Boundary(api, "API") {\n'
  '    Component(ctrl, "Контролер замовлень", "FastAPI", "Приймає запити")\n'
  '    Component(svc, "Сервіс замовлень", "Python", "Правила замовлень")\n'
  '    Component(repo, "Репозиторій", "SQLAlchemy", "Доступ до даних")\n'
  '  }\n'
  '  Rel(ctrl, svc, "Передає замовлення")\n'
  '  Rel(svc, repo, "Зберігає")\n'
  '  Rel(repo, db, "SQL")\n'
  '  Rel(svc, pay, "Платіж")'),
 ('S3',
  'to_mermaid',
  ([{'id': 's',
     'kind': 'softwareSystem',
     'name': 'С',
     'description': 'd',
     'technology': '',
     'tags': [],
     'parent': None},
    {'id': 'a', 'kind': 'container', 'name': 'А', 'description': 'd', 'technology': 'Go', 'tags': [], 'parent': 's'},
    {'id': 'k', 'kind': 'component', 'name': 'К', 'description': 'd', 'technology': 'Go', 'tags': [], 'parent': 'a'},
    {'id': 'l', 'kind': 'component', 'name': 'Л', 'description': 'd', 'technology': 'Go', 'tags': [], 'parent': 'a'}],
   {'elements': ['k', 'l'], 'relationships': [('k', 'l', 'x; y'), ('l', 'k', 'z')]},
   'component',
   'a'),
  'C4Component\n'
  '  title Компоненти: А\n'
  '  Container_Boundary(a, "А") {\n'
  '    Component(k, "К", "Go", "d")\n'
  '    Component(l, "Л", "Go", "d")\n'
  '  }\n'
  '  Rel(k, l, "x; y")\n'
  '  Rel(l, k, "z")'),
 ('S3',
  'to_mermaid',
  ([{'id': 'a',
     'kind': 'container',
     'name': 'А',
     'description': 'd',
     'technology': 'Go',
     'tags': [],
     'parent': None}],
   {'elements': [], 'relationships': []},
   'component',
   'a'),
  'C4Component\n  title Компоненти: А\n  Container_Boundary(a, "А") {\n  }')]


@pytest.mark.parametrize("tag,fn,args,expected", T05, ids=_ids(T05, "T05"))
def test_task_05(tag, fn, args, expected):
    run(5, fn, args, expected)
