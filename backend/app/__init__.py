from flask import Flask

from .security import InputValidationError


def create_app():
    app = Flask(__name__)

    @app.errorhandler(InputValidationError)
    def handle_validation_error(error):
        return {"error": "Validation error", "message": str(error)}, 400

    @app.errorhandler(400)
    def handle_bad_request(error):
        return {"error": "Bad request"}, 400

    @app.errorhandler(404)
    def handle_not_found(error):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def handle_server_error(error):
        return {"error": "Internal server error"}, 500

    @app.get("/api/health")
    def health():
        return {"status": "ok"}, 200

    return app
