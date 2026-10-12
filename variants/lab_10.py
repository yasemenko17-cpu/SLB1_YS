"""Лабораторна SIS-LAB01. Задача 10: Порівняння версій моделі.

Правила — у student.md (розділ 7, задача 10) та в картці вашого варіанта.
Відкриті тести: pytest tests/test_lab_10.py
"""


def diff_elements(old: list[dict], new: list[dict]) -> dict[str, list[str]]:
    """Знаходить додані й видалені елементи."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


def changed_elements(old: list[dict], new: list[dict]) -> dict[str, list[str]]:
    """Знаходить змінені поля елементів."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


def diff_relationships(old: list[dict], new: list[dict]) -> dict[str, list[tuple[str, str]]]:
    """Порівнює зв'язки двох версій."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі
