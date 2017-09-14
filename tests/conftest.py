import pytest
from decouple import config
from user_api.app import app as _app, db as _db

from sqlalchemy import inspect


@pytest.fixture(scope="session")
def app(request):
    _app.config["SQLALCHEMY_DATABASE_URI"] = config("SQLALCHEMY_DATABASE_URI_TEST", "sqlite:///:memory:")
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        request.addfinalizer(teardown)
    return _app


@pytest.fixture(scope="session", autouse=True)
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

    session = db.create_scoped_session(options={"bind": connection})
    db.session = session

    def teardown():
        transaction.rollback()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope="function", autouse=True)
def clear_db(session, request):
    inspector = inspect(session.bind.engine)
    for table_name in reversed(inspector.get_table_names()):
        session.execute("DELETE FROM {};".format(table_name))


@pytest.fixture
def api_test_client(app):
    return app.test_client()
