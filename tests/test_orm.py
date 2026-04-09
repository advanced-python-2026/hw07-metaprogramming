"""Тесты для Mini-ORM (задание 7.1)."""

from __future__ import annotations

import datetime
import json

import pytest

from hw07.orm import (
    BoolField,
    ChoiceField,
    DateField,
    EmailField,
    Field,
    FloatField,
    ForeignKeyField,
    IntField,
    JSONField,
    ListField,
    Model,
    ModelMeta,
    StringField,
)

# ---------------------------------------------------------------------------
# Helpers: динамическое создание моделей по варианту
# ---------------------------------------------------------------------------


def _make_model_v0():
    """Вариант 0: IntField, StringField, DateField, BoolField."""

    class UserV0(Model):
        age = IntField(min_value=0, max_value=150)
        name = StringField(max_length=100)
        birthday = DateField()
        active = BoolField()

    return UserV0


def _make_model_v1():
    """Вариант 1: FloatField, ListField, EmailField, ChoiceField."""

    class UserV1(Model):
        score = FloatField(min_value=0.0, max_value=100.0)
        tags = ListField(item_type=str)
        email = EmailField()
        role = ChoiceField(choices=("admin", "user", "guest"))

    return UserV1


def _make_model_v2():
    """Вариант 2: IntField, StringField, ForeignKeyField, JSONField."""

    class Department(Model):
        dept_id = IntField(min_value=1)
        dept_name = StringField(max_length=50)

    class Employee(Model):
        emp_id = IntField(min_value=1)
        emp_name = StringField(max_length=100)
        department = ForeignKeyField(to=Department)
        metadata = JSONField()

    return Department, Employee


_MODEL_FACTORIES = {0: _make_model_v0, 1: _make_model_v1, 2: _make_model_v2}


def _valid_kwargs_v0():
    return {"age": 25, "name": "Alice", "birthday": datetime.date(1999, 5, 15), "active": True}


def _valid_kwargs_v1():
    return {"score": 95.5, "tags": ["python", "dev"], "email": "a@b.com", "role": "admin"}


def _valid_kwargs_v2(dept_instance):
    return {
        "emp_id": 1,
        "emp_name": "Bob",
        "department": dept_instance,
        "metadata": {"level": 3},
    }


# ===================================================================
# Общие тесты (все варианты)
# ===================================================================


class TestModelCommon:
    """Общие тесты Model/ModelMeta, параметризованные по варианту."""

    def test_model_creation(self, variant: int):
        """Модель создаётся с корректными kwargs."""
        if variant == 0:
            cls = _make_model_v0()
            obj = cls(**_valid_kwargs_v0())
            assert obj.age == 25
        elif variant == 1:
            cls = _make_model_v1()
            obj = cls(**_valid_kwargs_v1())
            assert obj.score == 95.5
        else:
            Dept, Emp = _make_model_v2()
            dept = Dept(dept_id=1, dept_name="IT")
            obj = Emp(**_valid_kwargs_v2(dept))
            assert obj.emp_id == 1

    def test_validate_passes_valid(self, variant: int):
        """validate() не бросает исключение для валидных данных."""
        if variant == 0:
            cls = _make_model_v0()
            obj = cls(**_valid_kwargs_v0())
        elif variant == 1:
            cls = _make_model_v1()
            obj = cls(**_valid_kwargs_v1())
        else:
            Dept, Emp = _make_model_v2()
            dept = Dept(dept_id=1, dept_name="IT")
            obj = Emp(**_valid_kwargs_v2(dept))
        obj.validate()  # должен пройти без исключений

    def test_to_dict(self, variant: int):
        """to_dict() возвращает корректный словарь."""
        if variant == 0:
            cls = _make_model_v0()
            kw = _valid_kwargs_v0()
            obj = cls(**kw)
            d = obj.to_dict()
            assert d["age"] == 25
            assert d["name"] == "Alice"
            assert d["birthday"] == datetime.date(1999, 5, 15)
            assert d["active"] is True
        elif variant == 1:
            cls = _make_model_v1()
            kw = _valid_kwargs_v1()
            obj = cls(**kw)
            d = obj.to_dict()
            assert d["score"] == 95.5
            assert d["tags"] == ["python", "dev"]
            assert d["email"] == "a@b.com"
            assert d["role"] == "admin"
        else:
            Dept, Emp = _make_model_v2()
            dept = Dept(dept_id=1, dept_name="IT")
            obj = Emp(**_valid_kwargs_v2(dept))
            d = obj.to_dict()
            assert d["emp_id"] == 1
            assert d["emp_name"] == "Bob"
            assert d["metadata"] == {"level": 3}

    def test_from_dict(self, variant: int):
        """from_dict() создаёт экземпляр из словаря."""
        if variant == 0:
            cls = _make_model_v0()
            kw = _valid_kwargs_v0()
            obj = cls.from_dict(kw)
            assert obj.age == 25
            assert obj.name == "Alice"
        elif variant == 1:
            cls = _make_model_v1()
            kw = _valid_kwargs_v1()
            obj = cls.from_dict(kw)
            assert obj.score == 95.5
            assert obj.email == "a@b.com"
        else:
            Dept, Emp = _make_model_v2()
            dept = Dept(dept_id=1, dept_name="IT")
            kw = _valid_kwargs_v2(dept)
            obj = Emp.from_dict(kw)
            assert obj.emp_id == 1

    def test_repr(self, variant: int):
        """__repr__ возвращает читаемую строку."""
        if variant == 0:
            cls = _make_model_v0()
            obj = cls(**_valid_kwargs_v0())
        elif variant == 1:
            cls = _make_model_v1()
            obj = cls(**_valid_kwargs_v1())
        else:
            Dept, Emp = _make_model_v2()
            dept = Dept(dept_id=1, dept_name="IT")
            obj = Emp(**_valid_kwargs_v2(dept))
        r = repr(obj)
        assert isinstance(r, str)
        assert len(r) > 0
        # repr должен содержать имя класса
        assert obj.__class__.__name__ in r

    def test_fields_collected(self, variant: int):
        """_fields содержит все объявленные поля."""
        if variant == 0:
            cls = _make_model_v0()
            assert set(cls._fields.keys()) == {"age", "name", "birthday", "active"}
        elif variant == 1:
            cls = _make_model_v1()
            assert set(cls._fields.keys()) == {"score", "tags", "email", "role"}
        else:
            Dept, Emp = _make_model_v2()
            assert set(Emp._fields.keys()) == {"emp_id", "emp_name", "department", "metadata"}

    def test_fields_are_field_instances(self, variant: int):
        """Все значения _fields — экземпляры Field."""
        if variant == 0:
            cls = _make_model_v0()
        elif variant == 1:
            cls = _make_model_v1()
        else:
            _, cls = _make_model_v2()
        for f in cls._fields.values():
            assert isinstance(f, Field)

    def test_metaclass_is_model_meta(self, variant: int):
        """Метакласс модели — ModelMeta."""
        if variant == 0:
            cls = _make_model_v0()
        elif variant == 1:
            cls = _make_model_v1()
        else:
            _, cls = _make_model_v2()
        assert type(cls) is ModelMeta

    def test_inheritance(self):
        """Дочерний класс наследует поля родителя."""

        class Base(Model):
            base_id = IntField(min_value=0)

        class Child(Base):
            child_name = StringField(max_length=50)

        assert "base_id" in Child._fields
        assert "child_name" in Child._fields
        assert len(Child._fields) == 2

    def test_inheritance_does_not_modify_parent(self):
        """Наследование не добавляет поля в родительский класс."""

        class Parent(Model):
            pid = IntField()

        class ChildA(Parent):
            extra = StringField(max_length=10)

        assert "extra" not in Parent._fields
        assert "extra" in ChildA._fields

    def test_from_dict_missing_keys(self, variant: int):
        """from_dict() raises when required fields are missing."""
        if variant == 0:
            cls = _make_model_v0()
            incomplete = {"age": 25}  # missing name, birthday, active
        elif variant == 1:
            cls = _make_model_v1()
            incomplete = {"score": 95.5}  # missing tags, email, role
        else:
            _, cls = _make_model_v2()
            incomplete = {"emp_id": 1}  # missing emp_name, department, metadata
        with pytest.raises((TypeError, ValueError)):
            cls.from_dict(incomplete)


# ===================================================================
# Вариант 0: IntField, StringField, DateField, BoolField
# ===================================================================


class TestVariant0:
    """Тесты для полей варианта 0."""

    @pytest.fixture(autouse=True)
    def _skip_if_wrong_variant(self, variant: int):
        if variant != 0:
            pytest.skip("Вариант 0: IntField, StringField, DateField, BoolField")

    # --- IntField ---

    def test_intfield_accepts_int(self):
        class M(Model):
            val = IntField()

        obj = M(val=42)
        assert obj.val == 42

    def test_intfield_rejects_str(self):
        class M(Model):
            val = IntField()

        with pytest.raises(TypeError):
            M(val="hello")

    def test_intfield_rejects_float(self):
        class M(Model):
            val = IntField()

        with pytest.raises(TypeError):
            M(val=3.14)

    def test_intfield_min_value(self):
        class M(Model):
            val = IntField(min_value=0)

        with pytest.raises(ValueError):
            M(val=-1)

    def test_intfield_max_value(self):
        class M(Model):
            val = IntField(max_value=10)

        with pytest.raises(ValueError):
            M(val=11)

    def test_intfield_range_valid(self):
        class M(Model):
            val = IntField(min_value=1, max_value=100)

        obj = M(val=50)
        assert obj.val == 50

    def test_intfield_boundary_values(self):
        class M(Model):
            val = IntField(min_value=0, max_value=10)

        obj_min = M(val=0)
        obj_max = M(val=10)
        assert obj_min.val == 0
        assert obj_max.val == 10

    def test_intfield_no_constraints(self):
        class M(Model):
            val = IntField()

        obj = M(val=-999999)
        assert obj.val == -999999

    # --- StringField ---

    def test_stringfield_accepts_str(self):
        class M(Model):
            val = StringField()

        obj = M(val="hello")
        assert obj.val == "hello"

    def test_stringfield_rejects_int(self):
        class M(Model):
            val = StringField()

        with pytest.raises(TypeError):
            M(val=42)

    def test_stringfield_max_length_valid(self):
        class M(Model):
            val = StringField(max_length=5)

        obj = M(val="abc")
        assert obj.val == "abc"

    def test_stringfield_max_length_exceeded(self):
        class M(Model):
            val = StringField(max_length=3)

        with pytest.raises(ValueError):
            M(val="toolong")

    def test_stringfield_exact_max_length(self):
        class M(Model):
            val = StringField(max_length=5)

        obj = M(val="abcde")
        assert obj.val == "abcde"

    def test_stringfield_empty(self):
        class M(Model):
            val = StringField()

        obj = M(val="")
        assert obj.val == ""

    def test_stringfield_no_max_length(self):
        class M(Model):
            val = StringField()

        long = "x" * 10000
        obj = M(val=long)
        assert obj.val == long

    def test_stringfield_rejects_none(self):
        class M(Model):
            val = StringField()

        with pytest.raises(TypeError):
            M(val=None)

    # --- DateField ---

    def test_datefield_accepts_date(self):
        class M(Model):
            val = DateField()

        d = datetime.date(2024, 1, 15)
        obj = M(val=d)
        assert obj.val == d

    def test_datefield_rejects_str(self):
        class M(Model):
            val = DateField()

        with pytest.raises(TypeError):
            M(val="2024-01-15")

    def test_datefield_accepts_datetime_subclass(self):
        """datetime.datetime is a subclass of date, so DateField should accept it."""

        class M(Model):
            val = DateField()

        dt = datetime.datetime.now()
        obj = M(val=dt)
        assert obj.val == dt

    def test_datefield_rejects_int(self):
        class M(Model):
            val = DateField()

        with pytest.raises(TypeError):
            M(val=20240115)

    def test_datefield_rejects_none(self):
        class M(Model):
            val = DateField()

        with pytest.raises(TypeError):
            M(val=None)

    def test_datefield_various_dates(self):
        class M(Model):
            val = DateField()

        for d in [datetime.date(2000, 1, 1), datetime.date(2099, 12, 31)]:
            obj = M(val=d)
            assert obj.val == d

    def test_datefield_in_to_dict(self):
        class M(Model):
            val = DateField()

        d = datetime.date(2024, 6, 15)
        obj = M(val=d)
        assert obj.to_dict()["val"] == d

    def test_datefield_in_from_dict(self):
        class M(Model):
            val = DateField()

        d = datetime.date(2024, 6, 15)
        obj = M.from_dict({"val": d})
        assert obj.val == d

    # --- BoolField ---

    def test_boolfield_accepts_true(self):
        class M(Model):
            val = BoolField()

        obj = M(val=True)
        assert obj.val is True

    def test_boolfield_accepts_false(self):
        class M(Model):
            val = BoolField()

        obj = M(val=False)
        assert obj.val is False

    def test_boolfield_rejects_int(self):
        """bool is subclass of int, но BoolField должен принимать только bool."""

        class M(Model):
            val = BoolField()

        with pytest.raises(TypeError):
            M(val=1)

    def test_boolfield_rejects_zero(self):
        class M(Model):
            val = BoolField()

        with pytest.raises(TypeError):
            M(val=0)

    def test_boolfield_rejects_str(self):
        class M(Model):
            val = BoolField()

        with pytest.raises(TypeError):
            M(val="true")

    def test_boolfield_rejects_none(self):
        class M(Model):
            val = BoolField()

        with pytest.raises(TypeError):
            M(val=None)

    def test_boolfield_in_to_dict(self):
        class M(Model):
            val = BoolField()

        obj = M(val=True)
        assert obj.to_dict()["val"] is True

    def test_boolfield_validate(self):
        class M(Model):
            val = BoolField()

        obj = M(val=False)
        obj.validate()  # не должен бросать


# ===================================================================
# Вариант 1: FloatField, ListField, EmailField, ChoiceField
# ===================================================================


class TestVariant1:
    """Тесты для полей варианта 1."""

    @pytest.fixture(autouse=True)
    def _skip_if_wrong_variant(self, variant: int):
        if variant != 1:
            pytest.skip("Вариант 1: FloatField, ListField, EmailField, ChoiceField")

    # --- FloatField ---

    def test_floatfield_accepts_float(self):
        class M(Model):
            val = FloatField()

        obj = M(val=3.14)
        assert obj.val == 3.14

    def test_floatfield_accepts_int(self):
        class M(Model):
            val = FloatField()

        obj = M(val=42)
        assert obj.val == 42

    def test_floatfield_rejects_str(self):
        class M(Model):
            val = FloatField()

        with pytest.raises(TypeError):
            M(val="3.14")

    def test_floatfield_min_value(self):
        class M(Model):
            val = FloatField(min_value=0.0)

        with pytest.raises(ValueError):
            M(val=-0.1)

    def test_floatfield_max_value(self):
        class M(Model):
            val = FloatField(max_value=100.0)

        with pytest.raises(ValueError):
            M(val=100.1)

    def test_floatfield_range_valid(self):
        class M(Model):
            val = FloatField(min_value=0.0, max_value=10.0)

        obj = M(val=5.5)
        assert obj.val == 5.5

    def test_floatfield_boundary(self):
        class M(Model):
            val = FloatField(min_value=0.0, max_value=10.0)

        obj_min = M(val=0.0)
        obj_max = M(val=10.0)
        assert obj_min.val == 0.0
        assert obj_max.val == 10.0

    def test_floatfield_rejects_none(self):
        class M(Model):
            val = FloatField()

        with pytest.raises(TypeError):
            M(val=None)

    # --- ListField ---

    def test_listfield_accepts_list(self):
        class M(Model):
            val = ListField()

        obj = M(val=[1, 2, 3])
        assert obj.val == [1, 2, 3]

    def test_listfield_rejects_tuple(self):
        class M(Model):
            val = ListField()

        with pytest.raises(TypeError):
            M(val=(1, 2, 3))

    def test_listfield_rejects_str(self):
        class M(Model):
            val = ListField()

        with pytest.raises(TypeError):
            M(val="hello")

    def test_listfield_item_type_valid(self):
        class M(Model):
            val = ListField(item_type=int)

        obj = M(val=[1, 2, 3])
        assert obj.val == [1, 2, 3]

    def test_listfield_item_type_invalid(self):
        class M(Model):
            val = ListField(item_type=int)

        with pytest.raises((TypeError, ValueError)):
            M(val=[1, "two", 3])

    def test_listfield_empty_list(self):
        class M(Model):
            val = ListField(item_type=str)

        obj = M(val=[])
        assert obj.val == []

    def test_listfield_no_item_type(self):
        class M(Model):
            val = ListField()

        obj = M(val=[1, "two", 3.0])
        assert obj.val == [1, "two", 3.0]

    def test_listfield_nested(self):
        class M(Model):
            val = ListField(item_type=str)

        obj = M(val=["a", "b", "c"])
        obj.validate()

    # --- EmailField ---

    def test_emailfield_valid(self):
        class M(Model):
            val = EmailField()

        obj = M(val="user@example.com")
        assert obj.val == "user@example.com"

    def test_emailfield_rejects_no_at(self):
        class M(Model):
            val = EmailField()

        with pytest.raises(ValueError):
            M(val="userexample.com")

    def test_emailfield_rejects_no_domain(self):
        class M(Model):
            val = EmailField()

        with pytest.raises(ValueError):
            M(val="user@")

    def test_emailfield_rejects_no_local(self):
        class M(Model):
            val = EmailField()

        with pytest.raises(ValueError):
            M(val="@example.com")

    def test_emailfield_rejects_int(self):
        class M(Model):
            val = EmailField()

        with pytest.raises(TypeError):
            M(val=42)

    def test_emailfield_valid_complex(self):
        class M(Model):
            val = EmailField()

        obj = M(val="first.last+tag@sub.domain.org")
        assert "@" in obj.val

    def test_emailfield_rejects_spaces(self):
        class M(Model):
            val = EmailField()

        with pytest.raises(ValueError):
            M(val="user @example.com")

    def test_emailfield_rejects_empty(self):
        class M(Model):
            val = EmailField()

        with pytest.raises(ValueError):
            M(val="")

    # --- ChoiceField ---

    def test_choicefield_valid(self):
        class M(Model):
            val = ChoiceField(choices=("a", "b", "c"))

        obj = M(val="a")
        assert obj.val == "a"

    def test_choicefield_invalid(self):
        class M(Model):
            val = ChoiceField(choices=("a", "b", "c"))

        with pytest.raises(ValueError):
            M(val="d")

    def test_choicefield_int_choices(self):
        class M(Model):
            val = ChoiceField(choices=(1, 2, 3))

        obj = M(val=2)
        assert obj.val == 2

    def test_choicefield_int_invalid(self):
        class M(Model):
            val = ChoiceField(choices=(1, 2, 3))

        with pytest.raises(ValueError):
            M(val=4)

    def test_choicefield_all_choices_accepted(self):
        choices = ("admin", "user", "guest")

        class M(Model):
            val = ChoiceField(choices=choices)

        for c in choices:
            obj = M(val=c)
            assert obj.val == c

    def test_choicefield_empty_string_if_in_choices(self):
        class M(Model):
            val = ChoiceField(choices=("", "a"))

        obj = M(val="")
        assert obj.val == ""

    def test_choicefield_none_not_in_choices(self):
        class M(Model):
            val = ChoiceField(choices=("a", "b"))

        with pytest.raises(ValueError):
            M(val=None)

    def test_choicefield_validate(self):
        class M(Model):
            val = ChoiceField(choices=("x", "y"))

        obj = M(val="x")
        obj.validate()


# ===================================================================
# Вариант 2: IntField, StringField, ForeignKeyField, JSONField
# ===================================================================


class TestVariant2:
    """Тесты для полей варианта 2."""

    @pytest.fixture(autouse=True)
    def _skip_if_wrong_variant(self, variant: int):
        if variant != 2:
            pytest.skip("Вариант 2: IntField, StringField, ForeignKeyField, JSONField")

    # --- IntField (повтор из варианта 0) ---

    def test_intfield_accepts_int(self):
        class M(Model):
            val = IntField()

        obj = M(val=42)
        assert obj.val == 42

    def test_intfield_rejects_str(self):
        class M(Model):
            val = IntField()

        with pytest.raises(TypeError):
            M(val="hello")

    def test_intfield_min_value(self):
        class M(Model):
            val = IntField(min_value=0)

        with pytest.raises(ValueError):
            M(val=-1)

    def test_intfield_max_value(self):
        class M(Model):
            val = IntField(max_value=10)

        with pytest.raises(ValueError):
            M(val=11)

    def test_intfield_range_valid(self):
        class M(Model):
            val = IntField(min_value=1, max_value=100)

        obj = M(val=50)
        assert obj.val == 50

    def test_intfield_boundary_values(self):
        class M(Model):
            val = IntField(min_value=0, max_value=10)

        assert M(val=0).val == 0
        assert M(val=10).val == 10

    def test_intfield_no_constraints(self):
        class M(Model):
            val = IntField()

        assert M(val=-999).val == -999

    def test_intfield_rejects_bool(self):
        """IntField should reject bool even though bool is subclass of int."""

        class M(Model):
            emp_id = IntField(min_value=1)
            emp_name = StringField(max_length=100)

        with pytest.raises(TypeError):
            M(emp_id=True, emp_name="Alice")

    # --- StringField (повтор из варианта 0) ---

    def test_stringfield_accepts_str(self):
        class M(Model):
            val = StringField()

        obj = M(val="hello")
        assert obj.val == "hello"

    def test_stringfield_rejects_int(self):
        class M(Model):
            val = StringField()

        with pytest.raises(TypeError):
            M(val=42)

    def test_stringfield_max_length(self):
        class M(Model):
            val = StringField(max_length=3)

        with pytest.raises(ValueError):
            M(val="toolong")

    def test_stringfield_exact_length(self):
        class M(Model):
            val = StringField(max_length=5)

        obj = M(val="abcde")
        assert obj.val == "abcde"

    def test_stringfield_empty(self):
        class M(Model):
            val = StringField()

        obj = M(val="")
        assert obj.val == ""

    def test_stringfield_no_max(self):
        class M(Model):
            val = StringField()

        obj = M(val="x" * 10000)
        assert len(obj.val) == 10000

    def test_stringfield_rejects_none(self):
        class M(Model):
            val = StringField()

        with pytest.raises(TypeError):
            M(val=None)

    def test_stringfield_rejects_list(self):
        class M(Model):
            val = StringField()

        with pytest.raises(TypeError):
            M(val=["a", "b"])

    # --- ForeignKeyField ---

    def test_fk_accepts_correct_model(self):
        class Target(Model):
            tid = IntField()

        class Source(Model):
            ref = ForeignKeyField(to=Target)

        t = Target(tid=1)
        s = Source(ref=t)
        assert s.ref is t

    def test_fk_rejects_wrong_model(self):
        class Target(Model):
            tid = IntField()

        class Other(Model):
            oid = IntField()

        class Source(Model):
            ref = ForeignKeyField(to=Target)

        other = Other(oid=1)
        with pytest.raises(TypeError):
            Source(ref=other)

    def test_fk_rejects_non_model(self):
        class Target(Model):
            tid = IntField()

        class Source(Model):
            ref = ForeignKeyField(to=Target)

        with pytest.raises(TypeError):
            Source(ref="not a model")

    def test_fk_rejects_int(self):
        class Target(Model):
            tid = IntField()

        class Source(Model):
            ref = ForeignKeyField(to=Target)

        with pytest.raises(TypeError):
            Source(ref=42)

    def test_fk_rejects_none(self):
        class Target(Model):
            tid = IntField()

        class Source(Model):
            ref = ForeignKeyField(to=Target)

        with pytest.raises(TypeError):
            Source(ref=None)

    def test_fk_accepts_subclass(self):
        """ForeignKeyField должен принимать экземпляры подклассов целевой модели."""

        class Target(Model):
            tid = IntField()

        class ChildTarget(Target):
            extra = StringField()

        class Source(Model):
            ref = ForeignKeyField(to=Target)

        child = ChildTarget(tid=1, extra="x")
        s = Source(ref=child)
        assert s.ref is child

    def test_fk_in_to_dict(self):
        class Target(Model):
            tid = IntField()

        class Source(Model):
            ref = ForeignKeyField(to=Target)

        t = Target(tid=1)
        s = Source(ref=t)
        d = s.to_dict()
        assert "ref" in d

    def test_fk_validate(self):
        class Target(Model):
            tid = IntField()

        class Source(Model):
            ref = ForeignKeyField(to=Target)

        t = Target(tid=1)
        s = Source(ref=t)
        s.validate()

    # --- JSONField ---

    def test_jsonfield_accepts_dict(self):
        class M(Model):
            val = JSONField()

        obj = M(val={"key": "value"})
        assert obj.val == {"key": "value"}

    def test_jsonfield_accepts_list(self):
        class M(Model):
            val = JSONField()

        obj = M(val=[1, 2, 3])
        assert obj.val == [1, 2, 3]

    def test_jsonfield_rejects_str(self):
        class M(Model):
            val = JSONField()

        with pytest.raises(TypeError):
            M(val="not json")

    def test_jsonfield_rejects_int(self):
        class M(Model):
            val = JSONField()

        with pytest.raises(TypeError):
            M(val=42)

    def test_jsonfield_rejects_none(self):
        class M(Model):
            val = JSONField()

        with pytest.raises(TypeError):
            M(val=None)

    def test_jsonfield_complex_nested(self):
        class M(Model):
            val = JSONField()

        data = {"users": [{"name": "Alice", "scores": [1, 2, 3]}], "count": 1}
        obj = M(val=data)
        assert obj.val == data

    def test_jsonfield_non_serializable(self):
        """Объект, содержащий не-JSON-сериализуемые значения, должен быть отклонён."""

        class M(Model):
            val = JSONField()

        with pytest.raises((TypeError, ValueError)):
            M(val={"func": lambda x: x})

    def test_jsonfield_serializable_check(self):
        """Проверяем, что валидный JSON действительно сериализуется."""

        class M(Model):
            val = JSONField()

        data = {"a": [1, 2.0, "three", True, None]}
        obj = M(val=data)
        # Должно быть JSON-сериализуемо
        assert json.dumps(obj.val) is not None

    def test_jsonfield_empty_dict(self):
        class M(Model):
            val = JSONField()

        obj = M(val={})
        assert obj.val == {}

    def test_jsonfield_empty_list(self):
        class M(Model):
            val = JSONField()

        obj = M(val=[])
        assert obj.val == []


# ===================================================================
# Тесты validate() с ошибками типа (все варианты)
# ===================================================================


class TestValidateTypeErrors:
    """Тесты validate() — TypeError для неверного типа."""

    def test_validate_raises_type_error(self, variant: int):
        """validate() бросает TypeError при неверном типе поля."""
        if variant == 0:
            cls = _make_model_v0()
        elif variant == 1:
            cls = _make_model_v1()
        else:
            _, cls = _make_model_v2()
        with pytest.raises(TypeError):
            if variant == 0:
                cls(age="bad", name="A", birthday=datetime.date.today(), active=True)
            elif variant == 1:
                cls(score="bad", tags=[], email="a@b.com", role="admin")
            else:
                cls(emp_id="bad", emp_name="A", department=None, metadata={})


class TestValidateValueErrors:
    """Тесты validate() — ValueError для нарушения ограничений."""

    def test_validate_raises_value_error(self, variant: int):
        """validate() бросает ValueError при нарушении ограничения."""
        if variant == 0:
            cls = _make_model_v0()
            with pytest.raises(ValueError):
                cls(age=-1, name="A", birthday=datetime.date.today(), active=True)
        elif variant == 1:
            cls = _make_model_v1()
            with pytest.raises(ValueError):
                cls(score=-1.0, tags=[], email="a@b.com", role="admin")
        else:
            Dept, Emp = _make_model_v2()
            with pytest.raises(ValueError):
                Dept(dept_id=0, dept_name="IT")  # min_value=1
