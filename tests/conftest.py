from os import environ
from datetime import timedelta

import pytest

from application import application as _application, db as _db


def pytest_sessionstart(session):
    _application.config["SQLALCHEMY_DATABASE_URI"] = environ.get("SQLALCHEMY_DATABASE_URI_TEST")
    _application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    _application.config["TESTING"] = True
    _application.config["SECRET_KEY"] = "super-secret"
    _db.drop_all()
    _db.create_all()


@pytest.fixture(scope="session")
def application(request):
    ctx = _application.application_context()
    ctx.push()

    def teardown():
        request.addfinalizer(teardown)
    return _application


@pytest.fixture(scope="session")
def db(application, request):
    def teardown():
        _db.drop_all()

    _db.application = application

    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="function")
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    session = db.create_scoped_session(options={"bind": connection, "binds": {}})
    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def api_test_client(application):
    return application.test_client()
