# coding: utf-8
import pytest
from decouple import config
from sqlalchemy import event

from user_api.app import app as _app, db as _db


@pytest.fixture(scope="session")
def app(request):
    # Sobrescreve a string de conexão com o banco de dados da aplicação para usar o banco de testes
    _app.config["SQLALCHEMY_DATABASE_URI"] = config("SQLALCHEMY_DATABASE_URI_TEST", "sqlite:///:memory:")
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


# O banco de dados é recriado antes da execução de cada caso de teste
@pytest.fixture(scope="session", autouse=True)
def db(app, request):
    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()
    # Registra função que apaga todos as tabelas do banco de dados após a execução da suite de testes
    request.addfinalizer(teardown)
    return _db


# Inpirado em: http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html
@pytest.fixture(scope="function", autouse=True)
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()
    session = db.create_scoped_session(options={"bind": connection})
    session.begin(subtransactions=True)

    db.session = session

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()

    def teardown():
        transaction.rollback()
        connection.close()
        session.close()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def api_test_client(app):
    return app.test_client()
