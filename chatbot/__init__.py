from flask import Flask
from settings import SECRET_KEY
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from settings import NLU_MODEL_PATH
from rasa_nlu.model import Interpreter
from duckling import DucklingWrapper

duckling = DucklingWrapper()

interpreter = Interpreter.load(NLU_MODEL_PATH)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = SECRET_KEY
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % parse.quote_plus(con_str)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)
CORS(app)
db = SQLAlchemy(app)


from chatbot import routes


