from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from src.infra.listener import listenerLogin



app = Flask(__name__)
CORS(app)
api = Api(app)

# Webhook para el proyecto lpishopifyorder
api.add_resource(
    listenerLogin,
    "/login/<rut>/<password>/<periodo>"
)
