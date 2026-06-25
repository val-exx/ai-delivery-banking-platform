from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScaffoldPlan:
    module_name: str
    files: tuple[str, ...]

    def to_markdown(self) -> str:
        lines = [
            f"# Scaffold plan for `{self.module_name}`",
            "",
            "Recommended files:",
            "",
        ]
        lines.extend(f"- `{path}`" for path in self.files)
        return "\n".join(lines)


def module_plan(module_name: str) -> ScaffoldPlan:
    normalized = module_name.strip().lower().replace("_", "-")
    if not normalized:
        raise ValueError("module_name cannot be empty")

    files = (
        f"{normalized}/README.md",
        f"{normalized}/pyproject.toml",
        f"{normalized}/src/{normalized.replace('-', '_')}/__init__.py",
        f"{normalized}/tests/test_smoke.py",
        f"{normalized}/Dockerfile",
        f"{normalized}/docs/architecture.md",
        f"{normalized}/docker-compose.yml",
        f"{normalized}/.github/workflows/ci.yml",
        f"{normalized}/docs/interview-notes.md",
    )
    return ScaffoldPlan(module_name=normalized, files=files)

