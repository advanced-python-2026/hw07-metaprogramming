# ДЗ 7 — Метапрограммирование

Домашнее задание по курсу «Продвинутый Python».

## Задания

- **7.1** Mini-ORM с метаклассами (4 балла) — Field-дескрипторы, ModelMeta, Model
- **7.2** Динамическое создание классов через type() (2 балла) — make_dataclass

## Быстрый старт

```bash
uv sync
uv run pytest -v
uv run ruff check .
```

## Вариант

Вариант определяется автоматически по ФИО из `STUDENT.md`.
Впишите своё ФИО точно как в ведомости.

### Варианты полей для задания 7.1

| Вариант | Поля |
|---------|------|
| 0 | IntField, StringField, DateField, BoolField |
| 1 | FloatField, ListField, EmailField, ChoiceField |
| 2 | IntField, StringField, ForeignKeyField, JSONField |

## Материалы курса

[Конспект лекции](https://courses.sabalevsky.com/advanced-python/07-metaprogramming/)
