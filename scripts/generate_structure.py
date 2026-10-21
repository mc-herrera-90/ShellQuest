
import fnmatch
import json
import os
from html import escape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

OUTPUT = ROOT / "docs" / "reference" / "project-structure.md"

REPO_URL = os.getenv(
    "SHELLQUEST_REPO_URL",
    "https://github.com/TU_USUARIO/ShellQuest",
).rstrip("/")

BRANCH = os.getenv("SHELLQUEST_BRANCH", "main")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Puedes ignorar carpetas, archivos o patrones de rutas.
IGNORE_PATTERNS = [
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".idea",
    ".vscode",
    "site",
    "dist",
    "build",
    ".env",
    ".env.*",
    "*.pyc",
    "*.pyo",
    "uv.lock",
    "docs/reference/project-structure.md",
]

# Construir enlaces al código fuente.
def github_url(path: str, is_dir: bool = False) -> str:
    kind = "tree" if is_dir else "blob"
    return (
        f"{REPO_URL}/{kind}/"
        f"{quote(BRANCH, safe='/')}/"
        f"{quote(path, safe='/')}"
    )


def parse_repository_url() -> tuple[str, str]:
    parsed = urlparse(REPO_URL)
    parts = parsed.path.strip("/").split("/")

    if parsed.hostname != "github.com" or len(parts) < 2:
        raise ValueError(
            "SHELLQUEST_REPO_URL debe ser una URL válida "
            "de un repositorio de GitHub."
        )

    owner = parts[0]
    repo = parts[1].removesuffix(".git")
    return owner, repo


def should_ignore(path: str) -> bool:
    parts = path.split("/")

    for pattern in IGNORE_PATTERNS:
        if any(fnmatch.fnmatch(part, pattern) for part in parts):
            return True

        if fnmatch.fnmatch(path, pattern):
            return True

    return False


def fetch_repository_tree() -> list[dict]:
    owner, repo = parse_repository_url()

    api_url = (
        f"https://api.github.com/repos/{owner}/{repo}"
        f"/git/trees/{quote(BRANCH, safe='/')}?recursive=1"
    )

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ShellQuest-Documentation",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    request = Request(api_url, headers=headers)

    try:
        with urlopen(request, timeout=30) as response:
            data = json.load(response)
    except HTTPError as error:
        raise RuntimeError(
            f"GitHub respondió HTTP {error.code}. "
            "Comprueba el repositorio, la rama y los permisos."
        ) from error
    except URLError as error:
        raise RuntimeError(
            f"No se pudo conectar con GitHub: {error.reason}"
        ) from error

    if data.get("truncated"):
        raise RuntimeError(
            "GitHub devolvió un árbol incompleto. "
            "Hay que consultar los subárboles por separado."
        )

    return [
        entry
        for entry in data.get("tree", [])
        if entry["type"] in {"blob", "tree"}
        and not should_ignore(entry["path"])
    ]


def build_hierarchy(entries: list[dict]) -> dict:
    root = {"dirs": {}, "files": []}

    for entry in entries:
        parts = entry["path"].split("/")
        current = root

        for part in parts[:-1]:
            current = current["dirs"].setdefault(
                part, {"dirs": {}, "files": []}
            )

        name = parts[-1]

        if entry["type"] == "tree":
            current["dirs"].setdefault(
                name, {"dirs": {}, "files": []}
            )
        else:
            current["files"].append(name)

    return root


def render_tree(node: dict, path: str = "") -> str:
    html = ["<ul>"]

    directories = sorted(node["dirs"].items(), key=lambda x: x[0].lower())

    for name, child in directories:
        relative = f"{path}/{name}".strip("/")
        label = escape(name)
        url = escape(github_url(relative, is_dir=True), quote=True)

        html.append("<li><details>")
        html.append(
            f"<summary>📁 "
            f'<a href="{url}" target="_blank" '
            f'rel="noopener noreferrer" '
            f'onclick="event.stopPropagation()">{label}/</a>'
            "</summary>"
        )
        html.append(render_tree(child, relative))
        html.append("</details></li>")

    for name in sorted(node["files"], key=str.lower):
        relative = f"{path}/{name}".strip("/")
        label = escape(name)
        url = escape(github_url(relative), quote=True)

        html.append(
            "<li>📄 "
            f'<a href="{url}" target="_blank" '
            f'rel="noopener noreferrer">{label}</a>'
            "</li>"
        )

    html.append("</ul>")
    return "\n".join(html)


def main() -> None:
    entries = fetch_repository_tree()
    hierarchy = build_hierarchy(entries)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    content = (
        "---\n"
        "icon: material/folder\n"
        "---\n\n"
        "# Estructura del proyecto\n\n"
        "Árbol generado desde el repositorio remoto de GitHub. "
        "Expande las carpetas o pulsa un archivo para abrirlo.\n\n"
        '<div class="file-tree">\n'
        + render_tree(hierarchy)
        + "\n</div>\n"
    )

    OUTPUT.write_text(content, encoding="utf-8")

    print(
        f"Documentación generada: {OUTPUT.relative_to(ROOT)} "
        f"({len(entries)} entradas)"
    )


if __name__ == "__main__":
    main()
