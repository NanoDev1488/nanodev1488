"""
Обновляет секцию README между <!--TG-FEED-START--> и <!--TG-FEED-END-->
последними постами из публичного телеграм-канала.

Использует публичную preview-страницу t.me/s/<channel> — она доступна
без авторизации и без бот-токена, специально предназначена для встраивания
превью канала на сторонние сайты.
"""

import os
import re
import sys

import requests
from bs4 import BeautifulSoup

CHANNEL = os.environ.get("TG_CHANNEL", "nanodev_MC")
README_PATH = os.environ.get("README_PATH", "README.md")
MAX_POSTS = int(os.environ.get("TG_MAX_POSTS", "3"))

START_MARKER = "<!--TG-FEED-START-->"
END_MARKER = "<!--TG-FEED-END-->"


def fetch_posts():
    url = f"https://t.me/s/{CHANNEL}"
    resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    messages = soup.select(".tgme_widget_message_wrap")

    posts = []
    for msg in messages[-MAX_POSTS:]:
        text_el = msg.select_one(".tgme_widget_message_text")
        link_el = msg.select_one(".tgme_widget_message_date")

        text = text_el.get_text(" ", strip=True) if text_el else "(медиа-пост)"
        link = link_el["href"] if link_el and link_el.has_attr("href") else url

        if len(text) > 150:
            text = text[:150].rstrip() + "…"

        posts.append((text, link))

    posts.reverse()  # свежие сверху
    return posts


def update_readme(posts):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )

    if not posts:
        body = "_Не удалось получить посты (канал приватный или пустой)._"
    else:
        lines = [f"- [{text}]({link})" for text, link in posts]
        body = "\n".join(lines)

    section = f"{START_MARKER}\n{body}\n{END_MARKER}"

    if not pattern.search(content):
        print("Маркеры TG-ленты не найдены в README.")
        sys.exit(1)

    new_content = pattern.sub(section, content)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Лента обновлена, постов: {len(posts)}.")


if __name__ == "__main__":
    posts = fetch_posts()
    update_readme(posts)
