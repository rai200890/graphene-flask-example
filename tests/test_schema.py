import pytest

from user_api.graphql.schema import schema
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


@pytest.fixture
def user_mutation_without_phone():
    return """mutation MyMutation{
  createUser(input:{name: "Johnny", lastName: "Doe", email: "johnny.doe@email.com"}){
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


@pytest.fixture
def user_mutation_without_phone_result():
    return {
        "createUser": {
            "user": {
                "name": "Johnny",
                "phones": {
                    "edges": []
                }
            }
        }
    }


@pytest.fixture
def user_mutation_with_phones_result():
    return {
        "createUser": {
            "user": {
                "name": "Joey",
                "phones": {
                    "edges": [
                        {
                            "node": {
                                "ddd": "55",
                                "number": "123456780"
                            }
                        }
                    ]
                }
            }
        }
    }


@pytest.fixture
def query(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def expected_result(request):
    return request.getfixturevalue(request.param)


# O parâmetro indirect permite que seja chamada uma fixture dentro do parametrize
# indirect=True é análogo a chamar indirect para todos os parâmetros da lista,
# neste caso indirect=["query", "expected_result"]
# https://hackebrot.github.io/pytest-tricks/mark_parametrize_with_indirect/
@pytest.mark.parametrize("query, expected_result", [
    ("filter_query", "filter_query_empty_result"),
    ("filter_by_id_query", "filter_by_id_query_result"),
    ("filter_by_name_istarts_query", "filter_query_empty_result"),
    ("paging_query", "filter_query_empty_result"),
    ("filter_query", "filter_query_non_empty_result"),
    ("filter_by_name_istarts_query", "filter_by_name_istarts_query_result"),
    ("user_mutation_without_phone", "user_mutation_without_phone_result"),
    ("user_mutation_with_phones", "user_mutation_with_phones_result")
], indirect=True)
def test_query_result(query, expected_result):
    result = schema.execute(query)

    assert result.data == expected_result
