import pytest

from user_api.graphql.resolvers import PredicateParser


@pytest.fixture
def parser():
    return PredicateParser("name_Istartswith")


def test_field_name(parser):
    return parser.field_name == "name"


def test_insensitive_case(parser):
    return parser.insensitive_case is True


def test_matcher(parser):
    return parser.matcher == "startswith"
