from os import getcwd
import logging.config

from decouple import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView

from user_api.routes.error_handlers import register_handlers


db = SQLAlchemy()


def register_routes(app):
    from user_api.graphql.schema import schema
    from user_api.routes.healthcheck import HealthcheckView
    app.add_url_rule("/api/graphql", view_func=GraphQLView.as_view("graphql",
                                                                   schema=schema,
                                                                   graphiql=app.config["DEBUG"],
                                                                   context={"session": db.session}))
    app.add_url_rule("/api/healthcheck", view_func=HealthcheckView.as_view("healthcheck"))


def create_app():
    logging.config.fileConfig(config("LOG_CONFIG",
                                     default="{}/user_api/conf/logging.default.conf".format(getcwd())))
    app = Flask(__name__)
    app.config["DEBUG"] = config("DEBUG", cast=bool)
    app.config["PORT"] = config("PORT", cast=int)
    app.config["SQLALCHEMY_DATABASE_URI"] = config("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config("SQLALCHEMY_TRACK_MODIFICATIONS",
                                                          cast=bool,
                                                          default=False)
    app.config["SECRET_KEY"] = config("SECRET_KEY")
    db.init_app(app)

    register_routes(app)
    register_handlers(app)

    return app


app = create_app()
