"""Невеликий перевірник артефактів студента: модель Structurizr DSL, діаграми Mermaid, ADR, сценарії якості.

Це готовий інструмент викладача: його не потрібно змінювати. Він читає файли теки artifacts/
і повертає списки зауважень (порожній список означає, що артефакт приймається).
"""
import re
from pathlib import Path

ISO_25010 = ["Функційна відповідність", "Ефективність виконання", "Сумісність", "Взаємодія з користувачем",
             "Надійність", "Безпека", "Супровідність", "Гнучкість", "Безпечність"]
STATUSES = ["Запропоновано", "Прийнято", "Відхилено", "Застаріло"]
PLACEHOLDER = "<ЗАПОВНІТЬ"
DECL = re.compile(r'^[ \t]*(\w+)[ \t]*=[ \t]*(person|softwareSystem|container|component)[ \t]+((?:"(?:[^"\\]|\\.)*"[ \t]*)+)', re.M)
REL = re.compile(r'^[ \t]*(\w+)[ \t]*->[ \t]*(\w+)((?:[ \t]+"(?:[^"\\]|\\.)*")*)', re.M)
STR = re.compile(r'"((?:[^"\\]|\\.)*)"')


def read_dir(root: Path) -> dict:
    """Збирає вміст артефактів: workspace.dsl, diagrams.md, scenarios.md і всі adr/*.md."""
    root = Path(root)
    get = lambda p: (root / p).read_text(encoding="utf-8") if (root / p).exists() else ""
    return {"dsl": get("workspace.dsl"), "diagrams": get("diagrams.md"), "scenarios": get("scenarios.md"),
            "adr": {p.name: p.read_text(encoding="utf-8") for p in sorted((root / "adr").glob("*.md"))}}


def model_of(dsl: str):
    """Повертає (елементи, зв'язки): елемент = (id, вид, [рядки]), зв'язок = (джерело, ціль, [рядки])."""
    els = [(m.group(1), m.group(2), STR.findall(m.group(3))) for m in DECL.finditer(dsl)]
    rels = [(m.group(1), m.group(2), STR.findall(m.group(3))) for m in REL.finditer(dsl)]
    return els, rels


def check_workspace(dsl: str) -> list[str]:
    errs: list[str] = []
    if PLACEHOLDER in dsl:
        errs.append("у workspace.dsl лишилися незаповнені місця <ЗАПОВНІТЬ ...>")
    if dsl.count("{") != dsl.count("}"):
        errs.append("у workspace.dsl дужки { } не збалансовані")
    for key in ("workspace", "model {", "views {"):
        if key not in dsl:
            errs.append(f"у workspace.dsl немає «{key}»")
    els, rels = model_of(dsl)
    ids = [e[0] for e in els]
    if len(ids) != len(set(ids)):
        errs.append("є повторені ідентифікатори елементів")
    count = lambda k: sum(1 for e in els if e[1] == k)
    for kind, need in (("person", 1), ("softwareSystem", 2), ("container", 3)):
        if count(kind) < need:
            errs.append(f"елементів виду {kind} має бути щонайменше {need}, є {count(kind)}")
    for eid, kind, strs in els:
        if len(strs) < 2 or not strs[1].strip():
            errs.append(f"елемент {eid} без опису")
        if kind in ("container", "component") and (len(strs) < 3 or not strs[2].strip()):
            errs.append(f"елемент {eid} без технології")
    if len(rels) < 6:
        errs.append(f"зв'язків має бути щонайменше 6, є {len(rels)}")
    for s, d, strs in rels:
        if s not in ids or d not in ids:
            errs.append(f"зв'язок {s} -> {d} посилається на невідомий елемент")
        if not strs or not strs[0].strip():
            errs.append(f"зв'язок {s} -> {d} без опису")
    if not re.search(r"^\s*systemContext\s+\w+", dsl, re.M):
        errs.append("немає подання systemContext")
    if not re.search(r"^\s*container\s+\w+\s+\"[^\"]*\"\s*(?:\"[^\"]*\"\s*)?\{", dsl, re.M):
        errs.append("немає подання container")
    if dsl.count("include *") < 2:
        errs.append("у поданнях має бути include *")
    return errs


def check_diagrams(text: str, dsl: str) -> list[str]:
    errs: list[str] = []
    if PLACEHOLDER in text:
        errs.append("у diagrams.md лишилися незаповнені місця")
    blocks = re.findall(r"```mermaid\n(.*?)\n```", text, re.S)
    heads = [b.split("\n", 1)[0].strip() for b in blocks]
    for need in ("C4Context", "C4Container"):
        if need not in heads:
            errs.append(f"у diagrams.md немає блоку Mermaid {need}")
    ids = {e[0] for e in model_of(dsl)[0]}
    for b in blocks:
        aliases = set(re.findall(r"^\s*(?:Person|Person_Ext|System|System_Ext|Container|ContainerDb|Component|System_Boundary|Container_Boundary)\((\w+),", b, re.M))
        for a, c in re.findall(r"Rel\((\w+),\s*(\w+),", b):
            if a not in aliases or c not in aliases:
                errs.append(f"Rel({a}, {c}) у діаграмі посилається на елемент, якого в ній немає")
        for a in aliases - ids:
            errs.append(f"позначення {a} з діаграми відсутнє у workspace.dsl")
        if "Rel(" not in b:
            errs.append("діаграма без жодного зв'язку Rel")
    return errs


def check_adr(name: str, text: str) -> list[str]:
    errs: list[str] = []
    pre = f"{name}: "
    if PLACEHOLDER in text:
        errs.append(pre + "лишилися незаповнені місця")
    if not re.match(r"^# ADR-\d{3}: \S", text):
        errs.append(pre + "перший рядок має мати вигляд «# ADR-NNN: Назва»")
    m = re.search(r"^- Статус: (.+)$", text, re.M)
    st = m.group(1).strip() if m else ""
    if not (st in STATUSES or re.fullmatch(r"Замінено ADR-\d{3}", st)):
        errs.append(pre + "некоректний «- Статус:»")
    md = re.search(r"^- Дата: (\d{4}-\d{2}-\d{2})$", text, re.M)
    if st in ("Прийнято",) and not md:
        errs.append(pre + "для статусу «Прийнято» потрібна «- Дата: РРРР-ММ-ДД»")
    for sec in ("Контекст", "Варіанти", "Рішення", "Наслідки"):
        mm = re.search(rf"^## {sec}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
        if not mm or not mm.group(1).strip():
            errs.append(pre + f"немає або порожній розділ «{sec}»")
    var = re.search(r"^## Варіанти\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if var and sum(1 for ln in var.group(1).split("\n") if ln.startswith("- ")) < 2:
        errs.append(pre + "у «Варіанти» потрібно щонайменше два пункти")
    for key in ("Плюси", "Мінуси"):
        if not re.search(rf"^- {key}: \S", text, re.M):
            errs.append(pre + f"немає рядка «- {key}:»")
    ma = re.search(r"^- Атрибути якості: (.+)$", text, re.M)
    if not ma or any(x.strip() not in ISO_25010 for x in ma.group(1).split(",")):
        errs.append(pre + "«- Атрибути якості:» має містити назви характеристик ISO/IEC 25010")
    return errs


UNIT = re.compile(r"\d+(?:[.,]\d+)?\s*(?:мс|с|хв|год|%|запитів/с|запитів/хв)")


def check_scenarios(text: str, dsl: str) -> list[str]:
    errs: list[str] = []
    if PLACEHOLDER in text:
        errs.append("у scenarios.md лишилися незаповнені місця")
    lines = [ln for ln in text.split("\n") if re.match(r"^\d+\. ", ln)]
    if len(lines) < 3:
        errs.append(f"сценаріїв має бути щонайменше 3, є {len(lines)}")
    els = {e[0].lower() for e in model_of(dsl)[0]} | {e[2][0].strip().lower() for e in model_of(dsl)[0] if e[2]}
    attrs = set()
    for ln in lines:
        parts = {}
        for chunk in re.sub(r"^\d+\.\s*", "", ln).split(";"):
            k, _, v = chunk.partition(":")
            parts[k.strip()] = v.strip()
        for need in ("Атрибут", "Джерело", "Стимул", "Артефакт", "Середовище", "Відповідь", "Міра"):
            if not parts.get(need):
                errs.append(f"сценарій «{ln[:30]}…»: немає частини «{need}»")
        if parts.get("Атрибут") and parts["Атрибут"] not in ISO_25010:
            errs.append(f"сценарій «{ln[:30]}…»: атрибут не з переліку ISO/IEC 25010")
        attrs.add(parts.get("Атрибут"))
        if parts.get("Міра") and not UNIT.search(parts["Міра"]):
            errs.append(f"сценарій «{ln[:30]}…»: міра без числа й одиниці")
        if parts.get("Артефакт") and parts["Артефакт"].strip().lower() not in els:
            errs.append(f"сценарій «{ln[:30]}…»: артефакт не збігається з жодним елементом моделі")
    if len({a for a in attrs if a}) < 2:
        errs.append("сценарії мають охоплювати щонайменше два різні атрибути якості")
    return errs


def check_all(root: Path) -> list[str]:
    a = read_dir(root)
    errs = check_workspace(a["dsl"]) + check_diagrams(a["diagrams"], a["dsl"]) + check_scenarios(a["scenarios"], a["dsl"])
    if not a["adr"]:
        errs.append("у теці adr/ немає жодного ADR")
    for name, text in a["adr"].items():
        errs += check_adr(name, text)
    return errs
