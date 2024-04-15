from flask import jsonify
from .models import Database
from app import app, db_connection, db_cursor
import mysql.connector

db_connection = None
db_cursor = None

@app.before_request
def before_each_request():
    global db_connection, db_cursor
    db_connection = mysql.connector.connect(**app.config['DB_CONFIG'])
    db_cursor = db_connection.cursor()

@app.teardown_appcontext
def close_db_connection(exception=None):
    db_connection.close()

@app.route('/')
def testing():
    return 'testing'

@app.route('/player/<string:player_name>', methods=['GET'])
def get_player_info_by_name(player_name):
    global db_connection, db_cursor
    db = Database(db_connection, db_cursor)
    query = "SELECT * FROM player_info WHERE player_name = %s"
    data = db.execute_read_query(query, (player_name,))
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
    



@app.route('/check-email/<string:email>', methods=['GET'])
def check_email_exists(email):
    global db_connection, db_cursor
    db = Database(db_connection, db_cursor)
    query = "SELECT COUNT(*) FROM fan_engagement WHERE email = %s"
    data = db.execute_read_query(query, (email,))
    count = data[0][0]

    if count > 0:
        return jsonify({"exists": True})
    else:
        return jsonify({"exists": False})
    

@app.route('/all-player-votes', methods=['GET'])
def get_all_player_votes():
    global db_connection, db_cursor
    db = Database(db_connection, db_cursor)
    query = "SELECT COUNT(*) AS votes, t2.player_name FROM fan_engagement AS t1 \
             JOIN player_info AS t2 ON t1.player = t2.player_id GROUP BY t1.player"
    data = db.execute_read_query(query)

    if data:
        player_votes = [{"player_name": row[1], "votes": row[0]} for row in data]
        return jsonify(player_votes)
    else:
        return jsonify({"message": "No player votes found"}), 404



@app.route('/season-info/<int:year>', methods=['GET'])
def get_season_info(year):
    global db_connection, db_cursor
    db = Database(db_connection, db_cursor)
    query = "SELECT * FROM season_info WHERE year = %s"
    data = db.execute_read_query(query, (year,))
    
    if data:
        season_info = {
            "year": data[0][0],
            "budget": float(data[0][1]),
            "winners_team_id": data[0][2],
            "runners_team_id": data[0][3],
            "orange_cap_holder": data[0][4],
            "purple_cap_holder": data[0][5],
            "best_coach": data[0][6],
            "fair_play_award": data[0][7]
        }
        return jsonify(season_info)
    else:
        return jsonify({"message": "Season information not found"}), 404



@app.route('/team-budget/<int:season>/<string:franchise>', methods=['GET'])
def get_team_composition(season, franchise):
    global db_connection, db_cursor
    db = Database(db_connection, db_cursor)

    # Call the stored procedure to calculate budget details
    db_cursor.callproc('Calculate_Budget_Details', (franchise, season))
    # budget_details = db_cursor.fetchone()  # Fetch the results of the stored procedure
    for result in db_cursor.stored_results():
        budget_details = result.fetchall()

    # Query to fetch team composition
    query = "SELECT t2.*, t1.player_cost, t3.owner \
             FROM team_composition AS t1 \
             JOIN player_info AS t2 ON t1.player_id = t2.player_id \
             JOIN franchise_info AS t3 ON t3.franchise_id = t1.franchise \
             WHERE t1.season = %s AND t3.franchise_name = %s"
    data = db.execute_read_query(query, (season, franchise))

    if data:
        team_composition = []
        for row in data:
            player_info = {
                "player_id": row[0],
                "player_name": row[1],
                "date_of_birth": str(row[2]),  
                "is_international": bool(row[3]), 
                "innings_played": row[4],
                "catches_taken": row[5],
                "run_outs": row[6],
                "total_runs": row[7],
                "strike_rate": float(row[8]),  
                "num_thirties": row[9],
                "num_fifties": row[10],
                "num_centuries": row[11],
                "num_stumpings": row[12],
                "bowling_average": float(row[13]), 
                "bowling_economy": float(row[14]),  
                "overs_bowled": float(row[15]),
                "wickets_taken": row[16],
                "best_bowling": row[17],
                "player_cost": float(row[18]),
            }
            team_composition.append(player_info)
        
        # Construct the response including team composition and budget details
        response = {
            "team_composition": team_composition,
            "budget_details": {
                "total_money_spent": float(budget_details[0][0]),
                "avg_money_spent_international": float(budget_details[0][1]),
                "avg_money_spent_domestic": float(budget_details[0][2])
            }
        }
        return jsonify(response)
    else:
        return jsonify({"message": "No team composition found for the specified season and franchise"}), 404



