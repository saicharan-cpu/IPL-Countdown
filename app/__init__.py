import mysql.connector
from flask import Flask
from app import config  


app = Flask(__name__)
app.config.from_object(config)


db_connection = mysql.connector.connect(**app.config['DB_CONFIG'])

db_cursor = db_connection.cursor()


@app.teardown_appcontext
def close_db_connection(exception=None):
    db_connection.close()

