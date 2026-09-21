# Vibe Coding

**Разберись в коде. Внеси изменение. Проверь результат.**

46 навыков и 241 инженерный сценарий для Codex и Claude Code: карты проекта, постановка задач, ревью, поиск ошибок, реализация и проверка готовности к выпуску.

[Каталог сценариев](https://arty-kk.github.io/vibe-coding) · [English](README.md) · [Релизы](https://github.com/arty-kk/vibe-coding/releases) · [Поддержка](https://github.com/arty-kk/vibe-coding/issues)

## Установка

```sh
codex plugin marketplace add arty-kk/vibe-coding
```

Открой каталог плагинов в приложении, выбери источник **Vibe Coding** и установи **Vibe Coding**. Начни новую задачу для загрузки навыков.

Для Claude Code:

```sh
claude plugin marketplace add arty-kk/vibe-coding
claude plugin install vibe-coding@vibe-coding
```

Начни новую сессию и вызови `/vibe-coding:vibe`. Для конкретного навыка используй тот же префикс, например `/vibe-coding:vibe-review`. Инструкции учитывают `CLAUDE.md` и правила Claude, а в Codex — применимые `AGENTS.md`.

## Использование

```text
Используй Vibe Coding. Разберись в проекте и покажи, где находятся основные правила и данные.
```

| Задача | Навык |
| --- | --- |
| Составить карту проекта | `$vibe-map` |
| Сформулировать задачу и критерии готовности | `$vibe-task` |
| Проверить ветку или патч | `$vibe-review` |
| Найти и исправить один новый баг | `$vibe-probe` |
| Реализовать поведение продукта | `$vibe-product` |
| Проверить готовность к выпуску | `$vibe-quality` |

Указывай результат, область работы и ограничения. «Проверь» запускает анализ; «исправь» разрешает изменения. Плагин находит владельца правила в коде, проверяет затронутые связи и сообщает фактический результат проверок.

Подробные сценарии загружаются по задаче. Поддерживаются backend, frontend, базы данных, очереди, инфраструктура, безопасность, AI, мобильные и desktop-приложения.

Плагину не нужен отдельный API-ключ или сервер. Для запуска конкретного проекта нужны его обычные зависимости и доступы. Плагин опубликован в каталоге OpenAI. Для Claude Code доступна установка из публичного GitHub-маркетплейса.

## Разработка

```sh
python3 plugins/vibe-coding/scripts/validate.py
python3 -m unittest discover -s tests -v
python3 plugins/vibe-coding/scripts/catalog.py search "платежи"
```

[Правила разработки](CONTRIBUTING.md) · [Установка и обновление](plugins/vibe-coding/docs/INSTALL.md) · [MIT License](LICENSE)
