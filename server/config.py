
from flask import Flask, session, request, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData, func
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

from datetime import datetime
import re


app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xdb\xaf3\xe3\xe5\xce\xa9lqt/\xcc\xb6\xa7m,'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)
CORS(app)
bcrypt = Bcrypt(app)
