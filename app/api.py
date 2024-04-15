from flask import Flask, jsonify
from .models import Database
from app import db_connection, db_cursor, app

db = Database(db_connection, db_cursor)

@app.route('/')
def testing():
    return 'testing'


@app.route('/player/<int:player_id>', methods=['GET'])
def get_player_info(player_id):
    query = "SELECT * FROM player_info WHERE player_id = %s"

    data = db.execute_read_query(query, (player_id,))
    if data:
        player_info = data[0]
        player_data = {
            "player_id": player_info[0],
            "player_name": player_info[1],
            "date_of_birth": str(player_info[2]),  # Convert date object to string
            "is_international": bool(player_info[3]),  # Convert boolean value to Python boolean
            "innings_played": player_info[4],
            "catches_taken": player_info[5],
            "run_outs": player_info[6],
            "total_runs": player_info[7],
            "strike_rate": float(player_info[8]),  # Convert decimal to float
            "num_thirties": player_info[9],
            "num_fifties": player_info[10],
            "num_centuries": player_info[11],
            "num_stumpings": player_info[12],
            "bowling_average": float(player_info[13]),  # Convert decimal to float
            "bowling_economy": float(player_info[14]),  # Convert decimal to float
            "overs_bowled": float(player_info[15]),  # Convert decimal to float
            "wickets_taken": player_info[16],
            "best_bowling": player_info[17]
        }
        return jsonify(player_data)
    else:
        return jsonify({"message": "Player not found"}), 404
