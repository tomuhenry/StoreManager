from flask import Flask
from api.endpoints.app import app, store

app.register_blueprint(store, url_prefix='/store-manager/api/v1')

