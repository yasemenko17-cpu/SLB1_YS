# Стартовий проєкт SIS-LAB01

1. Відкрийте проєкт у GitHub Codespaces (Code → Codespaces → Create codespace) або локально: `python3 -m venv .venv`, `source .venv/bin/activate`, `pip install -r requirements.txt`. Права адміністратора не потрібні.
2. Визначте свою задачу й набір за номером варіанта: задача = `(номер - 1) // 3 + 1`, набір = `(номер - 1) % 3 + 1`. Реалізуйте функції у файлі `variants/lab_NN.py` за карткою варіанта.
3. Запускайте відкриті тести своєї задачі й свого набору: `pytest tests/test_lab_NN.py -k S2` (замініть `S2` на свій набір: `S1`, `S2` або `S3`).
4. Змінюйте лише свій файл у `variants/` (і за бажанням додавайте `tests/test_my.py`).
5. Частина Б: заповніть файли теки `artifacts/` для власної системи й перевірте їх командою `pytest artifacts_check`.
6. Необов'язково: перевірка синтаксису DSL офіційним інструментом (потрібен Docker, у Codespaces він є): `docker run --rm -v "$PWD/artifacts:/w" structurizr/structurizr:latest validate -w /w/workspace.dsl`.
