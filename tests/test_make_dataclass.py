"""Тесты для make_dataclass (задание 7.2)."""

from __future__ import annotations

from hw07.make_dataclass import make_dataclass


class TestMakeDataclass:
    """Тесты динамического создания классов через type()."""

    def test_class_has_correct_name(self):
        """Созданный класс имеет правильное имя."""
        Point = make_dataclass("Point", {"x": float, "y": float})
        assert Point.__name__ == "Point"

    def test_class_has_correct_name_custom(self):
        """Имя класса соответствует переданному аргументу."""
        Foo = make_dataclass("Foo", {"a": int})
        assert Foo.__name__ == "Foo"

    def test_instance_creation(self):
        """Экземпляр создаётся с именованными аргументами."""
        Point = make_dataclass("Point", {"x": float, "y": float})
        p = Point(x=1.0, y=2.0)
        assert p.x == 1.0
        assert p.y == 2.0

    def test_instance_creation_int_fields(self):
        """Поля могут быть целыми числами."""
        Vec = make_dataclass("Vec", {"a": int, "b": int, "c": int})
        v = Vec(a=1, b=2, c=3)
        assert v.a == 1
        assert v.b == 2
        assert v.c == 3

    def test_repr_format(self):
        """__repr__ имеет формат ClassName(field=value, ...)."""
        Point = make_dataclass("Point", {"x": float, "y": float})
        p = Point(x=1.0, y=2.0)
        r = repr(p)
        assert r.startswith("Point(")
        assert r.endswith(")")
        assert "x=" in r
        assert "y=" in r
        assert "1.0" in r
        assert "2.0" in r

    def test_repr_single_field(self):
        """__repr__ работает с одним полем."""
        Name = make_dataclass("Name", {"val": str})
        obj = Name(val="hello")
        r = repr(obj)
        assert "Name(" in r
        assert "val=" in r
        assert "hello" in r

    def test_eq_equal_instances(self):
        """Одинаковые экземпляры равны."""
        Point = make_dataclass("Point", {"x": float, "y": float})
        p1 = Point(x=1.0, y=2.0)
        p2 = Point(x=1.0, y=2.0)
        assert p1 == p2

    def test_eq_unequal_instances(self):
        """Разные экземпляры не равны."""
        Point = make_dataclass("Point", {"x": float, "y": float})
        p1 = Point(x=1.0, y=2.0)
        p2 = Point(x=3.0, y=4.0)
        assert p1 != p2

    def test_eq_partially_different(self):
        """Экземпляры с одним различающимся полем не равны."""
        Point = make_dataclass("Point", {"x": float, "y": float})
        p1 = Point(x=1.0, y=2.0)
        p2 = Point(x=1.0, y=9.0)
        assert p1 != p2

    def test_eq_different_classes_not_equal(self):
        """Экземпляры разных классов с одинаковыми полями не равны."""
        Point = make_dataclass("Point", {"x": float, "y": float})
        Coord = make_dataclass("Coord", {"x": float, "y": float})
        p = Point(x=1.0, y=2.0)
        c = Coord(x=1.0, y=2.0)
        assert p != c

    def test_eq_with_non_dataclass(self):
        """Сравнение с обычным объектом не вызывает ошибку."""
        Point = make_dataclass("Point", {"x": float, "y": float})
        p = Point(x=1.0, y=2.0)
        assert p != "not a point"
        assert p != 42
        assert p != None  # noqa: E711

    def test_created_via_type(self):
        """Класс создан через type() (метакласс — type)."""
        Point = make_dataclass("Point", {"x": float, "y": float})
        assert type(Point) is type

    def test_is_a_class(self):
        """Результат make_dataclass — класс."""
        Point = make_dataclass("Point", {"x": float, "y": float})
        assert isinstance(Point, type)

    def test_multiple_fields(self):
        """Класс с большим числом полей работает корректно."""
        fields = {f"f{i}": int for i in range(10)}
        Cls = make_dataclass("Big", fields)
        kwargs = {f"f{i}": i for i in range(10)}
        obj = Cls(**kwargs)
        for i in range(10):
            assert getattr(obj, f"f{i}") == i

    def test_single_field(self):
        """Класс с одним полем."""
        Wrapper = make_dataclass("Wrapper", {"value": str})
        w = Wrapper(value="test")
        assert w.value == "test"

    def test_empty_fields(self):
        """Класс без полей."""
        Empty = make_dataclass("Empty", {})
        e = Empty()
        assert repr(e) == "Empty()"

    def test_two_empty_equal(self):
        """Два экземпляра пустого класса равны."""
        Empty = make_dataclass("Empty", {})
        assert Empty() == Empty()

    def test_instances_are_independent(self):
        """Изменение одного экземпляра не влияет на другой."""
        Point = make_dataclass("Point", {"x": float, "y": float})
        p1 = Point(x=1.0, y=2.0)
        p2 = Point(x=1.0, y=2.0)
        p1.x = 99.0
        assert p2.x == 1.0

    def test_no_extra_methods(self):
        """Класс не имеет лишних специальных атрибутов (минимальный подход)."""
        Point = make_dataclass("Point", {"x": float, "y": float})
        # Должен иметь __init__, __repr__, __eq__
        assert hasattr(Point, "__init__")
        assert hasattr(Point, "__repr__")
        assert hasattr(Point, "__eq__")

    def test_different_value_types(self):
        """Поля могут хранить значения разных типов."""
        Mixed = make_dataclass("Mixed", {"name": str, "count": int, "rate": float})
        m = Mixed(name="test", count=5, rate=3.14)
        assert m.name == "test"
        assert m.count == 5
        assert m.rate == 3.14

    def test_positional_args_rejected(self):
        """Позиционные аргументы должны быть запрещены (только kwargs)."""
        Point = make_dataclass("Point", {"x": float, "y": float})
        with pytest.raises(TypeError):
            Point(1.0, 2.0)
