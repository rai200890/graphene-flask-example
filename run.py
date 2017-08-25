from user_api.app import app


if __name__ == "__main__":
    app.run(port=app.config["PORT"], host="0.0.0.0")
