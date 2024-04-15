from flask import jsonify
from .models import Database
from app import app, db_connection, db_cursor
import mysql.connector
import re

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


@app.route('/matches/<int:year>', methods=['GET'])
def get_matches_by_season(year):
    global db_connection, db_cursor
    db = Database(db_connection, db_cursor)

    # Adjusted query to include direct umpire references
    query = ("""
        SELECT 
            m.match_id,
            fi1.franchise_name AS Team_A_Name,
            fi2.franchise_name AS Team_B_Name,
            v.name AS Venue,
            v.location AS Location,
            v.seating_capacity AS Seating_Capacity,
            v.pitch_outfield AS Pitch_Outfield,
            m.match_date AS Date,
            m.scheduled_time AS Time,
            ui1.umpire_name AS First_Umpire,
            ui2.umpire_name AS Second_Umpire
        FROM 
            matches m 
            JOIN franchise_info fi1 ON m.team_a = fi1.franchise_id 
            JOIN franchise_info fi2 ON m.team_b = fi2.franchise_id 
            JOIN venue_info v ON m.venue = v.name
            JOIN umpire_info ui1 ON m.first_umpire = ui1.umpire_id
            JOIN umpire_info ui2 ON m.second_umpire = ui2.umpire_id
        WHERE 
            m.season = %s
    """)
    data = db.execute_read_query(query, (year,))
    if data:
        results = [{'Match_ID': row[0], 'Team_A_Name': row[1], 'Team_B_Name': row[2],
                    'Venue': row[3], 'Location': row[4], 'Seating_Capacity': row[5],
                    'Pitch_Outfield': row[6], 'Date': row[7], 'Time': row[8],
                    'First_Umpire': row[9], 'Second_Umpire': row[10]} for row in data]
        return jsonify(matches_data=results)
    else:
        return jsonify({"message": "Matches info not found for the given year"}), 404

@app.route('/teamComposition/<int:season>/<franchise_name>', methods=['GET'])
def get_team_details(season, franchise_name):
    global db_connection, db_cursor
    db = Database(db_connection, db_cursor)
    franchise_name = re.sub(r'\s+', '', franchise_name)
    players_query = """
    SELECT p.player_id AS Player_id, p.player_name AS Player, f.franchise_name AS Team
    FROM team_composition tc
    JOIN player_info p ON tc.player_id = p.player_id
    JOIN franchise_info f ON tc.franchise = f.franchise_id
    WHERE tc.season = %s AND f.franchise_name = %s;
    """
    players_data = db.execute_read_query(players_query, (season, franchise_name))

    leadership_query = """
    SELECT cp.captain AS Captain_id, cap.player_name AS Captain, t.coach AS Coach_id, c.coach_name AS Coach
    FROM franchise_info f
    LEFT JOIN captaincy cp ON f.franchise_id = cp.franchise AND cp.season = %s
    LEFT JOIN player_info cap ON cp.captain = cap.player_id
    LEFT JOIN trains t ON f.franchise_id = t.franchise AND t.season = %s
    LEFT JOIN coach_info c ON t.coach = c.coach_id
    WHERE f.franchise_name = %s;
    """
    leadership_data = db.execute_read_query(leadership_query, (season, season, franchise_name))

    if players_data or leadership_data:
        results = {
            'players': [{'Player_id': row[0], 'Player': row[1], 'Team': row[2]} for row in players_data],
            'leadership': {
                'Captain_id': leadership_data[0][0],
                'Captain': leadership_data[0][1],
                'Coach_id': leadership_data[0][2],
                'Coach': leadership_data[0][3]
            } if leadership_data else {}
        }
        return jsonify(team_details=results)
    else:
        return jsonify({"message": "No details found for the specified team and season"}), 404


@app.route('/teamPerformance/<int:season>/<team_name>', methods=['GET'])
def get_team_performance(season, team_name):
    global db_connection, db_cursor
    db = Database(db_connection, db_cursor)
    team_name = re.sub(r'\s+', '', team_name)
    query = "SELECT tp.season, f.franchise_name AS Team, tp.matches_won AS Matches_Won, tp.matches_lost AS Matches_Lost, tp.points AS Total_Points, CASE WHEN s.winners_team_id = f.franchise_id THEN 1 ELSE 0 END AS Trophies_Won FROM team_performance tp JOIN franchise_info f ON tp.team_id = f.franchise_id LEFT JOIN season_info s ON tp.season = s.year WHERE tp.season = %s AND f.franchise_name = %s;"
    results = db.execute_read_query(query, (season, team_name))
    if results:
        formatted_results = [{'Season': row[0], 'Team': row[1], 'Matches Won': row[2], 'Matches Lost': row[3], 'Total Points': row[4], 'Trophies Won': row[5]} for row in results]
        return jsonify(formatted_results)
    else:
        return jsonify({"message": "No performance data found for the specified team and season"}), 404
