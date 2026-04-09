"""Динамическое создание классов через type() (задание 7.2)."""

from __future__ import annotations


def make_dataclass(name: str, fields: dict[str, type]) -> type:
    """Создаёт класс с заданными полями, используя type().

    Аргументы:
        name: имя создаваемого класса
        fields: словарь {имя_поля: тип} (тип для документации, не для валидации)

    Возвращает класс с:
        - __init__(**kwargs) — принимает именованные аргументы для всех полей
        - __repr__() — формат "ClassName(field1=value1, field2=value2)"
        - __eq__(other) — сравнение по типу и значениям всех полей

    Пример:
        Point = make_dataclass("Point", {"x": float, "y": float})
        p = Point(x=1.0, y=2.0)
        assert repr(p) == "Point(x=1.0, y=2.0)"
    """
    raise NotImplementedError
