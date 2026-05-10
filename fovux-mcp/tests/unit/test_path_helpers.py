"""Tests for repository path discovery helpers."""

from __future__ import annotations

from pathlib import Path

from tests.path_helpers import find_package_root


def test_find_package_root_skips_mutmut_copy(tmp_path: Path) -> None:
    """Mutation-test copies should not be mistaken for the real package root."""
    package_root = tmp_path / "fovux-mcp"
    copied_root = package_root / "mutants"
    test_file = copied_root / "tests" / "security" / "test_http_security.py"

    (package_root / "scripts").mkdir(parents=True)
    (package_root / "src" / "fovux").mkdir(parents=True)
    (copied_root / "src" / "fovux").mkdir(parents=True)
    test_file.parent.mkdir(parents=True)

    (package_root / "pyproject.toml").write_text('[project]\nname = "fovux-mcp"\n')
    (package_root / "Dockerfile").write_text("FROM scratch\n")
    (package_root / "scripts" / "check_tool_docs.py").write_text("print('ok')\n")
    (copied_root / "pyproject.toml").write_text('[project]\nname = "fovux-mcp"\n')
    test_file.write_text("# copied test\n")

    assert find_package_root(test_file) == package_root.resolve()
