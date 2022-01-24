from flask import Flask
from flask_cors import CORS
from routes import BLUEPRINTS


if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)

    for bp in BLUEPRINTS:
        app.register_blueprint(blueprint=bp)

    app.run()
