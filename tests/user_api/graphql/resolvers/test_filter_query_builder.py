import pytest

from user_api.graphql.resolvers import FilterQueryBuilder
from user_api.models import User


@pytest.fixture
def builder():
    return FilterQueryBuilder(User.query, {"name_Istartswith": "aaa",
                                           "last_name_exact": "Doe"})


def test_entity(builder):
    assert builder.entity == User


def test_build(builder, mocker):
    query = mocker.patch.object(builder, "base_query")

    FilterPredicateMock = mocker.patch("user_api.graphql.resolvers.FilterPredicate")

    result = builder.build()

    assert result == query.filter().filter()

    FilterPredicateMock.call_count == 2
