"""Перевірка власних артефактів: pytest artifacts_check  (лише після виконання частини Б роботи)."""
import os
from pathlib import Path

import pytest
from archlint import check_adr, check_diagrams, check_scenarios, check_workspace, read_dir

ROOT = Path(os.environ.get("ARTIFACTS_DIR", Path(__file__).resolve().parent.parent / "artifacts"))
ART = read_dir(ROOT)


def _show(errors):
    assert not errors, "\n" + "\n".join("- " + e for e in errors)


def test_workspace_dsl():
    _show(check_workspace(ART["dsl"]))


def test_diagrams_md():
    _show(check_diagrams(ART["diagrams"], ART["dsl"]))


def test_scenarios_md():
    _show(check_scenarios(ART["scenarios"], ART["dsl"]))


def test_adr_exists():
    assert ART["adr"], "у теці artifacts/adr/ немає жодного файлу .md"


@pytest.mark.parametrize("name", sorted(ART["adr"]) or ["немає-файлів"])
def test_adr_file(name):
    assert name in ART["adr"], "створіть щонайменше один ADR у artifacts/adr/"
    _show(check_adr(name, ART["adr"][name]))
