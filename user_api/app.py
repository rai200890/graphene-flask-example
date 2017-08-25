from os import environ, getcwd
from os.path import join, exists
from datetime import timedelta

from flask import jsonify, Flask
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config["PORT"] = int(environ.get("PORT"))
application.config["SQLALCHEMY_DATABASE_URI"] = environ.get("SQLALCHEMY_DATABASE_URI")
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
application.config["SECRET_KEY"] = environ.get("SECRET_KEY")

db = SQLAlchemy(application)


@application.route("/api/healthcheck")
def healthcheck():
    try:
        db.engine.execute("SELECT 1;").fetchone()
        return jsonify({"status": "OK"})
    except SQLAlchemyError:
        return jsonify({"status": "DOWN"})


@application.errorhandler(404)
def handle_not_found(err):
    return jsonify({"mensagem": "Não encontrado"}), 404


@application.errorhandler(422)
def handle_unprocessable_entity(err):
    messages = ["{} {}".format(key, ",".join(value)) for key, value in err.data["messages"].items()]
    return jsonify({"mensagem": "; ".join(messages)}), 400


if __name__ == "__main__":
    application.run(port=application.config["PORT"], host="0.0.0.0")
