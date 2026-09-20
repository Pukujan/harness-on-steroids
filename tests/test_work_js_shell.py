from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_work_js_shell_report_locks_v10() -> None:
    text = (ROOT / "reports" / "codex-work-js-shell.md").read_text(encoding="utf-8")
    for n in (
        "with exec: **79**",
        "with js: **5**",
        "with shell_command: **2**",
        "also apply_patch: **1**",
        "| exec | 7345 |",
        "| js | 81 |",
        "| shell_command | 44 |",
    ):
        assert n in text, n


def test_modes_prefer_read_not_cwd_shell() -> None:
    kilo = (ROOT / ".kilo" / "agent" / "codex.md").read_text(encoding="utf-8")
    oc = (ROOT / ".opencode" / "agent" / "codex.md").read_text(encoding="utf-8")
    for text in (kilo, oc):
        assert "shell_command` is **2/85**" in text
        assert "Change the smallest slice with Edit or Write" not in text
        assert "apply_patch between shells" not in text
