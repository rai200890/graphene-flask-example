import pytest

from user_api.schema import schema
from user_api.models import User


@pytest.fixture
def user_1(session):
    user = User(name="John",
                last_name="Doe",
                email="john.doe@email.com")
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def user_2(session):
    user = User(name="Joe",
                last_name="Doe",
                email="joe.doe@email.com")
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def users(user_1, user_2):
    return [user_1, user_2]


@pytest.fixture
def filter_query():
    return """
query {
  users{
    edges{
      node{
        name,
        lastName,
      }
    }
  }
}
"""


@pytest.fixture
def filter_by_id_query():
    return """
    query {
        user(id: "VXNlclR5cGU6Mg=="){
        id,
        name,
        lastName,
        email
  }
}
"""


@pytest.fixture
def filter_by_name_istarts_query():
    return """
    query {
        users(name_Istartswith: "Joh"){
        edges{
            node{
            name,
            lastName
      }
    }
  }
}
"""


@pytest.fixture
def paging_query():
    return """
query{
    users(first: 1){
    edges{
      node{
        id,
        name,
        lastName,
        email
      }
    }
  }
}
"""


@pytest.fixture
def filter_query_empty_result():
    return {
        "users": {"edges": []}
    }


@pytest.fixture
def filter_by_id_query_result():
    return {
        "user": None
    }


@pytest.fixture
def filter_query_non_empty_result(users):
    return {
        "users": {
            "edges": [{"node": {"name": user.name, "lastName": user.last_name}} for user in users]
        }
    }


@pytest.fixture
def filter_by_name_istarts_query_result(user_1):
    return {
        "users": {
            "edges": [{"node": {"name": user_1.name, "lastName": user_1.last_name}}]
        }
    }


@pytest.fixture(params=[
    ("filter_query", "filter_query_empty_result"),
    ("filter_by_id_query", "filter_by_id_query_result"),
    ("filter_by_name_istarts_query", "filter_query_empty_result"),
    ("paging_query", "filter_query_empty_result")
])
def empty_query_result(request):
    return request.getfixturevalue(request.param[0]), request.getfixturevalue(request.param[1])


@pytest.fixture(params=[
    ("filter_query", "filter_query_non_empty_result"),
    ("filter_by_name_istarts_query", "filter_by_name_istarts_query_result")
])
def non_empty_query_result(request):
    return request.getfixturevalue(request.param[0]), request.getfixturevalue(request.param[1])


@pytest.fixture
def user_mutation_without_phone():
    return """mutation MyMutation{
  createUser(input:{name: "Johnny", lastName: "Doe", email: "john.doe@email.com"}){
    user{
      name
      phones {
        edges {
          node{
            ddd
            number
          }
        }
      }
    }
  }
}
"""


@pytest.fixture
def user_mutation_with_phones():
    return """mutation MyMutation{
  createUser(input:{
    name: "Joey", lastName: "Doe", email: "joey.doe@email.com",
    phones: [{ddd: "55", number: "123456780"}]
    }){
    user{
      name
      phones {
        edges {
          node{
            ddd
            number
          }
        }
      }
    }
  }
}
"""


def test_empty_query_result(empty_query_result):
    query, expected_result = empty_query_result
    result = schema.execute(query)

    assert result.data == expected_result


def test_nonempty_query_result(non_empty_query_result):
    query, expected_result = non_empty_query_result
    result = schema.execute(query)

    assert result.data == expected_result


def test_mutation_without_phone(user_mutation_without_phone):
    result = schema.execute(user_mutation_without_phone)

    user = User.query.first()

    assert result.data["createUser"]["user"]["name"] == user.name
    assert result.data["createUser"]["user"]["phones"]["edges"] == []


def test_mutation_with_phones(user_mutation_with_phones):
    result = schema.execute(user_mutation_with_phones)

    user = User.query.all()[-1]

    assert result.data["createUser"]["user"]["name"] == user.name
    assert result.data["createUser"]["user"]["phones"]["edges"][0]["node"]["ddd"] == user.phones[0].ddd
    assert result.data["createUser"]["user"]["phones"]["edges"][0]["node"]["number"] == user.phones[0].number
