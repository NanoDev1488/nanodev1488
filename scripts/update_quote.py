"""
Обновляет секцию README между <!--QUOTE-START--> и <!--QUOTE-END-->
случайной цитатой с бесплатного API (без ключа).
"""

import os
import re
import sys

import requests

README_PATH = os.environ.get("README_PATH", "README.md")

START_MARKER = "<!--QUOTE-START-->"
END_MARKER = "<!--QUOTE-END-->"


def fetch_quote():
    # zenquotes.io - бесплатный, без ключа, без лимитов для личного использования
    resp = requests.get("https://zenquotes.io/api/random", timeout=15)
    resp.raise_for_status()
    data = resp.json()[0]
    return data["q"], data["a"]


def update_readme(quote: str, author: str):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    section = f'{START_MARKER}\n> {quote}\n>\n> — {author}\n{END_MARKER}'

    if not pattern.search(content):
        print("Маркеры цитаты не найдены в README.")
        sys.exit(1)

    new_content = pattern.sub(section, content)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("Цитата обновлена.")


if __name__ == "__main__":
    quote, author = fetch_quote()
    update_readme(quote, author)
