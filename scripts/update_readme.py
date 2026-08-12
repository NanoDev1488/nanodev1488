"""
Скрипт обновляет секцию README между маркерами
<!--PROJECT-STATUS-START--> и <!--PROJECT-STATUS-END-->
данными о репозитории nano-decompiler (звёзды, язык, последний коммит).

Запускается через GitHub Actions по расписанию (см. update-readme.yml).
"""

import os
import re
import sys
from datetime import datetime, timezone

import requests

GITHUB_USER = os.environ.get("GITHUB_USER", "nanodev1488")
REPO_NAME = os.environ.get("REPO_NAME", "NanoDecompiler")
README_PATH = os.environ.get("README_PATH", "README.md")
TOKEN = os.environ.get("GITHUB_TOKEN")

START_MARKER = "<!--PROJECT-STATUS-START-->"
END_MARKER = "<!--PROJECT-STATUS-END-->"


def fetch_repo_data():
    headers = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}"
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()


def fetch_last_commit():
    headers = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/commits"
    resp = requests.get(url, headers=headers, params={"per_page": 1}, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        return None
    commit = data[0]["commit"]
    return {
        "message": commit["message"].splitlines()[0],
        "date": commit["author"]["date"],
    }


def build_section(repo, last_commit):
    stars = repo.get("stargazers_count", 0)
    language = repo.get("language", "?")
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        f"- ⭐ Звёзды: **{stars}**",
        f"- 🈺 Основной язык: **{language}**",
    ]
    if last_commit:
        lines.append(f"- 📝 Последний коммит: _{last_commit['message']}_")
    lines.append(f"- 🕒 Обновлено: {updated}")

    return "\n".join(lines)


def update_readme(new_section: str):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    replacement = f"{START_MARKER}\n{new_section}\n{END_MARKER}"

    if not pattern.search(content):
        print("Маркеры не найдены в README, ничего не меняю.")
        sys.exit(1)

    new_content = pattern.sub(replacement, content)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README обновлён.")


if __name__ == "__main__":
    repo = fetch_repo_data()
    last_commit = fetch_last_commit()
    section = build_section(repo, last_commit)
    update_readme(section)
