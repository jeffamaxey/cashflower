import pandas as pd
import pytest

from unittest import TestCase

from cashflower.cashflow import CashflowModelError, Model, ModelPointSet, Runplan, variable, Variable
from cashflower.start import load_settings


class TestVariableDecorator(TestCase):
    def test_variable_decorator(self):

        @variable()
        def foo(t):
            return t

        assert isinstance(foo, Variable)


class TestRunplan(TestCase):
    def test_runplan(self):
        runplan = Runplan(data=pd.DataFrame({
            "version": [1, 2],
            "value": [57, 89]
        }))
        assert runplan.version == "1"
        assert runplan.get("value") == 57

        empty_runplan = Runplan()
        assert empty_runplan.version == "1"

        runplan.version = "2"
        assert runplan.version == "2"

    def test_runplan_raises_error_when_no_version_column(self):
        with pytest.raises(CashflowModelError):
            Runplan(data=pd.DataFrame({"a": [1, 2, 3]}))

    def test_runplan_raises_error_when_non_existent_version_is_set(self):
        runplan = Runplan(data=pd.DataFrame({
            "version": [1, 2],
            "value": [57, 89]
        }))
        with pytest.raises(CashflowModelError):
            runplan.version = "3"

    def test_runplan_raises_error_when_non_existent_attribute_is_get(self):
        runplan = Runplan(data=pd.DataFrame({
            "version": [1, 2],
            "value": [57, 89]
        }))
        with pytest.raises(CashflowModelError):
            runplan.get("foo")


class TestModelPointSet(TestCase):
    def test_model_point_set(self):
        main = ModelPointSet(data=pd.DataFrame({
            "id": [1, 2, 3],
            "age": [52, 47, 35]
        }))
        assert len(main) == 3

        main.name = "main"
        main.settings = load_settings()
        main.initialize()
        assert main.id == "1"
        assert main.get("age") == 52
        assert repr(main) == "MPS: main"

    def test_model_point_set_raises_error_when_no_id_col(self):
        main = ModelPointSet(
            data=pd.DataFrame({"age": [52, 47, 35]}),
            name="policy",
            settings=load_settings()
        )
        with pytest.raises(CashflowModelError):
            main.initialize()

    def test_model_point_set_raises_error_when_no_unique_keys(self):
        main = ModelPointSet(
            data=pd.DataFrame({"id": [1, 2, 2]}),
            name="main",
            settings=load_settings()
        )
        with pytest.raises(CashflowModelError):
            main.initialize()


class TestVariable(TestCase):
    def test_variable_is_called(self):
        @variable()
        def foo(t):
            return t

        foo.name = "foo"
        foo.settings = load_settings()

        foo.calculate_t(10)

        assert foo(10) == 10

        with pytest.raises(CashflowModelError):
            foo(-1)
