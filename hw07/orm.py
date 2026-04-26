"""Mini-ORM с метаклассами (задание 7.1)."""

from __future__ import annotations


class Field:
    """Базовый дескриптор поля.

    Реализуйте:
    - __set_name__(self, owner, name) — сохраняет имя атрибута
    - __get__(self, obj, objtype=None) — возвращает значение из obj
    - __set__(self, obj, value) — валидирует и сохраняет значение
    - validate(self, value) — проверяет тип и ограничения
    """

    def __set_name__(self, owner: type, name: str) -> None:
        raise NotImplementedError

    def __get__(self, obj: object, objtype: type | None = None) -> object:
        raise NotImplementedError

    def __set__(self, obj: object, value: object) -> None:
        raise NotImplementedError

    def validate(self, value: object) -> None:
        raise NotImplementedError


# === Вариант 0: IntField, StringField, DateField, BoolField ===


class IntField(Field):
    """Целочисленное поле.

    Параметры: min_value, max_value (опциональные).
    TypeError если значение не int (bool отвергается, несмотря на то что bool — подкласс int).
    ValueError если значение вне диапазона.
    """

    def __init__(self, *, min_value: int | None = None, max_value: int | None = None) -> None:
        raise NotImplementedError


class StringField(Field):
    """Строковое поле.

    Параметры: max_length (опциональный).
    TypeError если значение не str.
    ValueError если длина превышает max_length.
    """

    def __init__(self, *, max_length: int | None = None) -> None:
        raise NotImplementedError


class DateField(Field):
    """Поле даты.

    Принимает datetime.date.
    TypeError если значение не date.
    """

    def __init__(self) -> None:
        raise NotImplementedError


class BoolField(Field):
    """Логическое поле.

    Принимает только bool (строго, int не допускается).
    TypeError если значение не bool.
    """

    def __init__(self) -> None:
        raise NotImplementedError


# === Вариант 1: FloatField, ListField, EmailField, ChoiceField ===


class FloatField(Field):
    """Поле с плавающей точкой.

    Принимает float и int. Параметры: min_value, max_value (опциональные).
    TypeError если значение не числовое.
    ValueError если значение вне диапазона.
    """

    def __init__(self, *, min_value: float | None = None, max_value: float | None = None) -> None:
        raise NotImplementedError


class ListField(Field):
    """Поле-список.

    Параметры: item_type (опциональный) — тип элементов списка.
    TypeError если значение не list.
    ValueError если элементы не соответствуют item_type.
    """

    def __init__(self, *, item_type: type | None = None) -> None:
        raise NotImplementedError


class EmailField(Field):
    """Поле email.

    TypeError если значение не str.
    ValueError если значение не соответствует формату email.
    """

    def __init__(self) -> None:
        raise NotImplementedError


class ChoiceField(Field):
    """Поле с выбором из допустимых значений.

    Параметры: choices — коллекция допустимых значений.
    ValueError если значение не входит в choices.
    """

    def __init__(self, *, choices: tuple[object, ...] | list[object]) -> None:
        raise NotImplementedError


# === Вариант 2: IntField (выше), StringField (выше), ForeignKeyField, JSONField ===


class ForeignKeyField(Field):
    """Поле внешнего ключа.

    Параметры: to — класс модели, на которую ссылается поле.
    TypeError если значение не является экземпляром указанной модели.
    """

    def __init__(self, *, to: type) -> None:
        raise NotImplementedError


class JSONField(Field):
    """JSON-поле.

    Принимает dict или list. Проверяет, что значение JSON-сериализуемо.
    TypeError если значение не dict и не list.
    ValueError если значение не JSON-сериализуемо.
    """

    def __init__(self) -> None:
        raise NotImplementedError


# === Метакласс и базовая модель ===


class ModelMeta(type):
    """Метакласс для моделей.

    Собирает все Field-экземпляры из атрибутов класса в cls._fields (dict).
    Поддерживает наследование: дочерний класс содержит поля родителя.
    """

    def __new__(mcs, name: str, bases: tuple[type, ...], namespace: dict[str, object]) -> ModelMeta:
        raise NotImplementedError


class Model(metaclass=ModelMeta):
    """Базовый класс модели.

    Реализуйте:
    - __init__(**kwargs) — устанавливает значения полей
    - validate() — вызывает validate() для каждого поля
    - to_dict() -> dict — возвращает словарь {имя_поля: значение}
    - from_dict(cls, data: dict) -> Model — создаёт экземпляр из словаря
    - __repr__() — читаемое представление
    """

    def __init__(self, **kwargs: object) -> None:
        raise NotImplementedError

    def validate(self) -> None:
        raise NotImplementedError

    def to_dict(self) -> dict[str, object]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Model:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError
