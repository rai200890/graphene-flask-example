from decouple import config
from flask import jsonify, Flask
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = config("DEBUG", cast=bool)
    app.config["PORT"] = config("PORT", cast=int)
    app.config["SQLALCHEMY_DATABASE_URI"] = config("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config("SQLALCHEMY_TRACK_MODIFICATIONS",
                                                          cast=bool, default=False)
    db.init_app(app)
    app.config["SECRET_KEY"] = config("SECRET_KEY")
    from user_api.schema import schema
    app.add_url_rule("/api/graphql", view_func=GraphQLView.as_view("graphql",
                                                                   schema=schema,
                                                                   graphiql=app.config["DEBUG"],
                                                                   context={"session": db.session}))

    @app.route("/api/healthcheck")
    def healthcheck():
        try:
            db.engine.execute("SELECT 1;").fetchone()
            return jsonify({"status": "OK"})
        except SQLAlchemyError:
            return jsonify({"status": "DOWN"})

    @app.errorhandler(404)
    def handle_not_found(err):
        return jsonify({"mensagem": "Não encontrado"}), 404

    @app.errorhandler(422)
    def handle_unprocessable_entity(err):
        messages = ["{} {}".format(key, ",".join(value)) for key, value in err.data["messages"].items()]
        return jsonify({"mensagem": "; ".join(messages)}), 400
    return app


app = create_app()
