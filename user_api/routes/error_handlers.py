from flask import jsonify


def handle_not_found(err):
    return jsonify({"errors": ["resource not found"]}), 404


def handle_bad_request(err):
    messages = ["{} {}".format(key, ",".join(value)) for key, value in err.data["messages"].items()]
    return jsonify({"errors": messages}), 400


def register_handlers(app):
    @app.errorhandler(404)
    def handle_404(err):
        return handle_not_found(err)

    @app.errorhandler(400)
    def handle_400(err):
        return handle_bad_request(err)
