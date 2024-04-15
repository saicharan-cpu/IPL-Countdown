from flask import Flask
from app import config  


db_connection = None
db_cursor = None
app = Flask(__name__)
app.config.from_object(config)

