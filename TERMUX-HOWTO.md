# Установка через Termux — пошагово

## ⚠️ Сначала — про токен

Ты присылал токен в чат — **обязательно отзови его** на
https://github.com/settings/tokens (кнопка Delete) и создай новый.
Новый токен вставляй **только в терминал Termux**, никогда никому в чат/переписку.

При создании нового токена (Settings → Developer settings →
Personal access tokens → Tokens classic → Generate new token) выбери права:
- `repo` (полный доступ к репозиториям)
- `workflow` (чтобы Actions могли пушить коммиты)

---

## 1. Установка пакетов в Termux

```bash
pkg update -y && pkg upgrade -y
pkg install git gh -y
```

`gh` — официальный GitHub CLI, с ним не придётся руками собирать API-запросы.

## 2. Логин в GitHub через токен (не сохраняя его в истории команд)

```bash
gh auth login
```

Выбери:
- `GitHub.com`
- `HTTPS`
- `Paste an authentication token` → вставь свой **новый** токен

`gh` сам безопасно сохранит токен в конфиге Termux (не в bash history).

## 3. Создание репозитория `nanodev1488/nanodev1488` (профильный)

```bash
cd ~
mkdir nanodev1488-profile && cd nanodev1488-profile
gh repo create nanodev1488/nanodev1488 --public --confirm
```

## 4. Заливаем файлы

Перенеси на телефон файлы из архива, который я собрал (README.md, .github/,
scripts/, assets/) — проще всего через Google Drive / Telegram "Избранное" →
скачать в `~/nanodev1488-profile/` (в Termux это будет видно как
`~/storage/downloads/`, если делал `termux-setup-storage`).

```bash
termux-setup-storage
cp -r ~/storage/downloads/nanodev1488-profile/* ~/nanodev1488-profile/
```

Положи своё фото:
```bash
cp ~/storage/downloads/твоё_фото.jpg ~/nanodev1488-profile/assets/photo.jpg
```

## 5. Пушим

```bash
cd ~/nanodev1488-profile
git init
git add .
git commit -m "init profile readme"
git branch -M main
git remote add origin https://github.com/nanodev1488/nanodev1488.git
git push -u origin main
```

`gh` подставит токен автоматически при пуше через HTTPS — вводить его
вручную не придётся.

## 6. Включаем права для Actions

```bash
gh api -X PUT repos/nanodev1488/nanodev1488/actions/permissions/workflow \
  -f default_workflow_permissions=write
```

Либо через сайт: **Settings → Actions → General → Workflow permissions →
Read and write permissions**.

## 7. Запускаем воркфлоу вручную (не ждать расписания)

```bash
gh workflow run "Generate Snake"
gh workflow run "Update README"
```

Проверить статус:
```bash
gh run list
```

## 8. (Если ещё не создан) репозиторий самого проекта

```bash
cd ~
gh repo create nanodev1488/NanoDecompiler --public --confirm
# дальше обычный git init / add / commit / push из папки с проектом
```

---

## Что дальше по плану
- лента последних постов из t.me/nanodev_MC
- бейджи/виджеты про сообщество Rumain
- кастомный баннер вместо стандартных badge-сервисов

Скажи, когда будешь готов — продолжим.
