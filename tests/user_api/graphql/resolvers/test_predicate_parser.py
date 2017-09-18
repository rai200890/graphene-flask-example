import pytest

from user_api.graphql.resolvers import PredicateParser


@pytest.fixture
def parser(request):
    return PredicateParser(request.param)


@pytest.mark.parametrize("parser, expected", [
    ("name_Istartswith", "name"),
    ("last_name_startswith", "last_name")
], indirect=["parser"])
def test_field_name(parser, expected):
    return parser.field_name == expected


@pytest.mark.parametrize("parser, expected", [
    ("name_Istartswith", False),
    ("name_startswith", True)
], indirect=["parser"])
def test_sensitive_case(parser, expected):
    return parser.sensitive_case is expected


@pytest.mark.parametrize("parser, expected", [
    ("name_Istartswith", "startswith"),
    ("last_name_endswith", "endswith")
], indirect=["parser"])
def test_matcher(parser, expected):
    return parser.matcher == expected
