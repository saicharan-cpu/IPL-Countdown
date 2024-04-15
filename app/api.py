from flask import jsonify, render_template
import mysql.connector
from .models import Database

import mysql.connector

db_connection = None
db_cursor = None

def setup_database(app):
    @app.before_request
    def before_each_request():
        global db_connection, db_cursor
        db_connection = mysql.connector.connect(**app.config['DB_CONFIG'])
        db_cursor = db_connection.cursor()

    @app.teardown_appcontext
    def close_db_connection(exception=None):
        if db_connection:
            db_connection.close()



def configure_routes(app):
    @app.route('/home')
    def home():
        return render_template('Main/index.html')

    setup_database(app)
    @app.route('/')
    def test():
        return render_template('Main/index.html')

    @app.route('/aboutproject')
    def aboutproject():
        return render_template('Main/AboutProject.html')
    @app.route('/IPLFeatures')
    def features():
        return render_template('Main/IPLFeatures.html')

    @app.route('/playerInfo')
    def playerInfo():
        return render_template('PlayerInfo/Input/PlayerInfoInputs.html')

    @app.route('/coaches')
    def coaches():
        return render_template('Coaches/Input/CoachesInput.html')

    @app.route('/teamComposition')
    def teamComposition():
        return render_template('Teamcomposition/Input/TeamCompositionInput.html')

    @app.route('/budget')
    def budget():
        return render_template('Teamcomposition/Input/TeamCompositionInput.html')

    @app.route('/matchesScheduled')
    def matchesScheduled():
        return render_template('MatchSchedule/Input/MatchScheduleInput.html')


    @app.route('/player/<int:player_id>', methods=['GET'])
    def get_player_info(player_id):
        global db_connection, db_cursor
        db = Database(db_connection, db_cursor)
        query = "SELECT * FROM player_info WHERE player_id = %s"
        data = db.execute_read_query(query, (player_id,))
        if data:
            player_info = data[0]
            player_data = {
                "player_id": player_info[0],
                "player_name": player_info[1],
                "date_of_birth": str(player_info[2]),
                "is_international": bool(player_info[3]),
                "innings_played": player_info[4],
                "catches_taken": player_info[5],
                "run_outs": player_info[6],
                "total_runs": player_info[7],
                "strike_rate": float(player_info[8]),
                "num_thirties": player_info[9],
                "num_fifties": player_info[10],
                "num_centuries": player_info[11],
                "num_stumpings": player_info[12],
                "bowling_average": float(player_info[13]),
                "bowling_economy": float(player_info[14]),
                "overs_bowled": float(player_info[15]),
                "wickets_taken": player_info[16],
                "best_bowling": player_info[17]
            }
            return jsonify(player_data)
        else:
            return jsonify({"message": "Player not found"}), 404