from flask import Flask
from backend.routes.lexer_routes import routes_lexer
from backend.routes.parser_routes import routes_parser
from backend.routes.semantic_routes import routes_semantic
from backend.routes.jwt_routes import routes_jwt

app = Flask(__name__)
app.register_blueprint(routes_lexer, url_prefix="/api/lexer")
app.register_blueprint(routes_parser, url_prefix="/api/parser")
app.register_blueprint(routes_semantic, url_prefix="/api/semantic")
app.register_blueprint(routes_jwt, url_prefix="/api/jwt")



if __name__ == "__main__":
    app.run(debug=True)