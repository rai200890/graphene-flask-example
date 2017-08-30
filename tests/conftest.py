import pytest
from decouple import config
from app import app as _app, db as _db


def pytest_sessionstart(session):
    _app.config["SQLALCHEMY_DATABASE_URI"] = config("SQLALCHEMY_DATABASE_URI_TEST")
    _app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    _app.config["TESTING"] = True
    _app.config["SECRET_KEY"] = "super-secret"
    _db.drop_all()
    _db.create_all()


@pytest.fixture(scope="session")
def app(request):
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        request.addfinalizer(teardown)
    return _app


@pytest.fixture(scope="session")
def db(app, request):
    def teardown():
        _db.drop_all()

    _db.app = app

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
def api_test_client(app):
    return app.test_client()
