import pytest

from user_api.graphql.resolvers import FilterPredicate, PredicateParser
from user_api.models import User


@pytest.fixture
def filter_predicate():
    return FilterPredicate(User, "last_name_Iendswith", "Doe")


def test_parser(filter_predicate):
    assert isinstance(filter_predicate.parser, PredicateParser) is True


def test_field(filter_predicate):
    assert filter_predicate.field == User.last_name


@pytest.mark.parametrize(
    "filter_predicate, operator",  [
        (FilterPredicate(User, "last_name_startswith", "Doe"), "like"),
        (FilterPredicate(User, "last_name_Iendswith", "Doe"), "ilike"),
        ])
def test_operator(filter_predicate, operator):
    assert filter_predicate.operator == operator


@pytest.mark.parametrize(
    "filter_predicate, template",  [
        (FilterPredicate(User, "last_name_startswith", "Doe"), "{}%"),
        (FilterPredicate(User, "last_name_endswith", "Doe"), "%{}"),
        (FilterPredicate(User, "last_name_contains", "Doe"), "%{}%"),
        (FilterPredicate(User, "last_name_exact", "Doe"), "{}")
    ])
def test_template(filter_predicate, template):
    assert filter_predicate.template == template


def test_predicate(filter_predicate):
    assert str(filter_predicate.predicate) == 'lower("user".last_name) LIKE lower(:last_name_1)'
