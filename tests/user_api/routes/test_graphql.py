import json

import pytest


@pytest.fixture
def url(request):
    return "/api/graphql?{}".format(request.param)


@pytest.fixture
def body(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def valid_response():
    return {
        "data": {
           "users": {
             "edges": []
           }
        }
    }


@pytest.fixture
def invalid_response():
    return {
        "errors": [
            {
                "message": "Syntax Error GraphQL request (3:3) \
Expected Name, found }\n\n2:   users{ \n3:   }\n     ^\n4: }\n",
                "locations": [
                    {"line": 3,
                     "column": 3}]
                 }
            ]
    }


@pytest.mark.parametrize("url, status_code, body", [
    ("query=query%7B%0A%20%20users\
     %7B%0A%20%20%20%20edges%7B%0A%20%20%20%20%20%20\
     node%7B%0A%20%20%20%20%20%20%20%20name%0A%20%20\
     %20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D", 200, "valid_response"),
    ("query=query%7B%0A%20%20users%7B%20%0A%20%20%7D%0A%7D", 400, "invalid_response")
], indirect=["url", "body"])
def test_post(api_test_client, url, status_code, body):
    result = api_test_client.get(url)
    data = json.loads(result.data.decode("utf-8"))

    assert result.status_code == status_code
    assert data == body
