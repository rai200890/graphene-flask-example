from flask import jsonify
from flask.views import MethodView

from user_api.app import db


class HealthcheckView(MethodView):

    def get(self):
        try:
            db.engine.execute("SELECT 1;").fetchone()
            return jsonify({"status": "OK"})
        except:
            return jsonify({"status": "DOWN"})
