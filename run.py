from flask import Flask
from api.views.my_app import app


if __name__ == '__main__':
    app.run(debug=True, port=8080)
