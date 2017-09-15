from flask import jsonify


def handle_not_found(err):
    return jsonify({"mensagem": "Não encontrado"}), 404


def handle_unprocessable_entity(err):
    messages = ["{} {}".format(key, ",".join(value)) for key, value in err.data["messages"].items()]
    return jsonify({"mensagem": "; ".join(messages)}), 400


def register_handlers(app):
    @app.errorhandler(404)
    def handle_404(err):
        return handle_not_found(err)

    @app.errorhandler(422)
    def handle_422(err):
        return handle_unprocessable_entity(err)
