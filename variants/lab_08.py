import re
from datetime import datetime

ISO_ATTRIBUTES = {
    "Функційна відповідність",
    "Ефективність виконання",
    "Сумісність",
    "Взаємодія з користувачем",
    "Надійність",
    "Безпека",
    "Супровідність",
    "Гнучкість",
    "Безпечність"
}

VALID_STATUSES = {
    "Запропоновано", "Прийнято", "Відхилено", "Застаріло",
    "Proposed", "Accepted", "Rejected", "Deprecated",
    "запропоновано", "прийнято", "відхилено", "застаріло",
    "proposed", "accepted", "rejected", "deprecated"
}

def validate_adr(text: str, rules: set[str]) -> list[str]:
    errors = []
    lines = [line.strip() for line in text.splitlines()]
    non_empty_lines = [l for l in lines if l]
    
    if not non_empty_lines:
        if "A01" in rules:
            errors.append("A01")
        return sorted(errors)

    # A01: Перший непорожній рядок
    adr_num = None
    first_line = non_empty_lines[0]
    m_adr = re.match(r"^#\s*ADR-(\d{3}):\s*(.+)$", first_line)
    if not m_adr:
        if "A01" in rules:
            errors.append("A01")
    else:
        adr_num = m_adr.group(1)

    # Збираємо статус і дату до першого розділу ## (ігноруємо символи списків на початку)
    status_line = None
    date_line = None
    for line in lines:
        if line.startswith("##"):
            break
        clean_line = re.sub(r"^[-*]\s*", "", line).strip()
        if clean_line.startswith("Статус:") or clean_line.startswith("Status:"):
            status_line = clean_line.split(":", 1)[1].strip()
        elif clean_line.startswith("Дата:") or clean_line.startswith("Date:"):
            date_line = clean_line.split(":", 1)[1].strip()

    # Розбиваємо документ на розділи за заголовками ##
    sections = {}
    current_sec = None
    current_content = []
    
    for line in lines:
        if line.startswith("##"):
            if current_sec:
                sections[current_sec] = current_content
            current_sec = line[2:].strip()
            current_content = []
        elif current_sec:
            current_content.append(line)
    if current_sec:
        sections[current_sec] = current_content

    # A02: Перевірка обов'язкових розділів Контекст, Рішення, Наслідки
    if "A02" in rules:
        for sec in ["Контекст", "Рішення", "Наслідки"]:
            if sec not in sections or not any(l.strip() for l in sections[sec]):
                errors.append(f"A02 {sec}")

    # A10, A11, A12 (Ваш набір 2)
    replaced_match = None
    if "A10" in rules:
        is_valid_status = False
        if status_line:
            if status_line in VALID_STATUSES:
                is_valid_status = True
            else:
                m_rep = re.match(r"^(Замінено|Replaced)\s+ADR-(\d{3})$", status_line, re.IGNORECASE)
                if m_rep:
                    is_valid_status = True
                    replaced_match = m_rep.group(2)
        if not is_valid_status:
            errors.append("A10")

    if "A11" in rules:
        date_valid = True
        if date_line:
            try:
                datetime.strptime(date_line, "%Y-%m-%d")
            except ValueError:
                date_valid = False
        
        status_lower = status_line.lower() if status_line else ""
        status_requires_date = ("прийнято" in status_lower or "accepted" in status_lower or 
                                "замінено" in status_lower or "replaced" in status_lower)
        if not date_line and status_requires_date:
            date_valid = False
            
        if date_line and not date_valid:
            errors.append("A11")
        elif not date_line and status_requires_date:
            errors.append("A11")

    if "A12" in rules and replaced_match and adr_num:
        if replaced_match == adr_num:
            errors.append("A12")

    # A20: Варіанти
    if "A20" in rules:
        var_lines = sections.get("Варіанти", [])
        bullet_count = sum(1 for l in var_lines if l.startswith("-") or l.startswith("*") or (l and not l.startswith("#")))
        if bullet_count < 2:
            errors.append("A20")

    # A21, A22, A23: Наслідки та атрибути
    conseq_text = "\n".join(sections.get("Наслідки", []))
    if "A21" in rules:
        if not re.search(r"(Плюси|Pros):\s*(.+)", conseq_text, re.IGNORECASE):
            errors.append("A21")
    if "A22" in rules:
        if not re.search(r"(Мінуси|Cons):\s*(.+)", conseq_text, re.IGNORECASE):
            errors.append("A22")
    if "A23" in rules:
        attr_match = re.search(r"(Атрибути якості|Quality attributes):\s*(.+)", text, re.IGNORECASE)
        if not attr_match:
            errors.append("A23")
        else:
            attrs = [a.strip() for a in attr_match.group(2).split(",")]
            for a in attrs:
                if a not in ISO_ATTRIBUTES:
                    errors.append("A23")
                    break

    return sorted(errors)