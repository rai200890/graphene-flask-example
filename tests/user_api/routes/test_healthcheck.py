import json


def test_healthcheck_down(api_test_client, db, mocker):
    db.engine.execute = mocker.Mock(side_effect=Exception())
    result = api_test_client.get("/api/healthcheck")
    data = json.loads(result.data.decode("utf-8"))

    assert result.status_code == 500
    assert data == {"status": "DOWN"}


def test_healthcheck_up(api_test_client, db, mocker):
    db.engine.execute = mocker.Mock()
    result = api_test_client.get("/api/healthcheck")
    data = json.loads(result.data.decode("utf-8"))

    assert result.status_code == 200
    assert data == {"status": "UP"}
