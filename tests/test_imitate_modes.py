from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEEDLES = [
    "Look first",
    "Burst look",
    "Look again",
    "Prose is not truth",
    "Do not patch first",
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
    assert "1518" in report.read_text(encoding="utf-8")
