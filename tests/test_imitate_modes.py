from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEEDLES = [
    "Look first",
    "Burst look",
    "Look again",
    "Prose is not truth",
    "Do not patch first",
    "Chat first",
    "Seek go-ahead before a long-running task",
    "A status question is not a standing goal",
]


def test_kilo_and_opencode_codex_modes_exist_and_match() -> None:
    kilo = ROOT / ".kilo" / "agent" / "codex.md"
    oc = ROOT / ".opencode" / "agent" / "codex.md"
    spec = ROOT / "spec" / "codex-imitate-mode.md"
    report = ROOT / "reports" / "codex-gold-behavior.md"
    assert kilo.is_file() and oc.is_file() and spec.is_file() and report.is_file()
    kt = kilo.read_text(encoding="utf-8")
    ot = oc.read_text(encoding="utf-8")
    st = spec.read_text(encoding="utf-8")
    for n in NEEDLES:
        assert n in kt and n in ot, n
    assert "Do not patch first" in st
    assert "exec → exec → exec" in st or "exec -> exec -> exec" in st
    rt = report.read_text(encoding="utf-8")
    assert "1521" in rt
    assert "Do not average originators" in rt
    assert "codex_work_desktop" in rt
    assert "| js_cell | 29231 |" in rt
    assert "| codex_work_desktop | 87 |" in rt
    assert "one file once" in rt
    first = rt.split("## first tool in session")[-1].split("## tool bigrams")[0]
    assert "| exec | 1131 |" in first
    assert "create_thread" not in first
    work = (ROOT / "reports" / "codex-work-desktop-only.md").read_text(encoding="utf-8")
    assert "codex_work_desktop" in work
    assert "with apply_patch: **1**" in work
    err = (ROOT / "reports" / "codex-work-errors.md").read_text(encoding="utf-8")
    assert "failed outputs: **5**" in err
    assert "| shell_command | 4 |" in err
    assert "Primary gold" in st or "codex_work_desktop" in st
