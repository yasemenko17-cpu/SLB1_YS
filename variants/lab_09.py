"""Лабораторна SIS-LAB01. Задача 9: Сценарії якості.

Правила — у student.md (розділ 7, задача 9) та в картці вашого варіанта.
Відкриті тести: pytest tests/test_lab_09.py
"""


def parse_scenario(text: str) -> dict[str, str]:
    """Розбирає сценарій якості на шість частин."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


def parse_measure(text: str) -> tuple[float, str]:
    """Перетворює міру відповіді на число в базових одиницях."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


def check_traceability(scenarios: list[dict], elements: list[dict]) -> dict[str, list[str]]:
    """Звіряє сценарії з елементами моделі."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі
