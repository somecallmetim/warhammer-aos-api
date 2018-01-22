from app_config import AppConfig

from flask import Flask
from flask_restful import Api
from resources.unit_resource import UnitResource

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = AppConfig.get_db_path()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = AppConfig.get_secret_key()
api = Api(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


api.add_resource(UnitResource, "/unit/<string:name>")


if __name__ == '__main__':
    from db import db
    db.init_app(app)

    @app.before_first_request
    def create_tables():

        db.create_all()

    app.run()
