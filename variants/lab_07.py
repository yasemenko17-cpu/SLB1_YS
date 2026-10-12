"""Лабораторна SIS-LAB01. Задача 7: Аналіз залежностей між контейнерами.

Правила — у student.md (розділ 7, задача 7) та в картці вашого варіанта.
Відкриті тести: pytest tests/test_lab_07.py
"""


def fan_in_out(edges: list[tuple[str, str]]) -> dict[str, tuple[int, int]]:
    """Для кожного вузла повертає (кількість вхідних, кількість вихідних) зв'язків."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


def find_cycles(edges: list[tuple[str, str]]) -> list[list[str]]:
    """Повертає групи вузлів, що утворюють цикл."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


def layers(edges: list[tuple[str, str]]) -> list[list[str]]:
    """Розкладає вузли за шарами залежностей."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі
