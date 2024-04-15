function searchPlayerById() {
    const playerId = document.getElementById('searchInput').value;
    if (playerId) {
        fetch(`/player/${playerId}`)
            .then(response => {
                if (!response.ok) throw new Error('No player found');
                return response.json();
            })
            .then(player => {
                displayPlayerInfo(player);
            })
            .catch(error => {
                console.error('Error fetching player data:', error);
                document.getElementById('playerInfo').textContent = 'Player not found';
            });
    }
}

function displayPlayerInfo(player) {
    const playerInfo = document.getElementById('playerInfo');
    playerInfo.innerHTML = `
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Date of Birth</th>
                    <th>International</th>
                    <th>Innings Played</th>
                    <th>Catches Taken</th>
                    <th>Run Outs</th>
                    <th>Total Runs</th>
                    <th>Strike Rate</th>
                    <th>30s</th>
                    <th>50s</th>
                    <th>100s</th>
                    <th>Stumpings</th>
                    <th>Bowling Average</th>
                    <th>Bowling Economy</th>
                    <th>Overs Bowled</th>
                    <th>Wickets Taken</th>
                    <th>Best Bowling</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>${player.player_id}</td>
                    <td>${player.player_name}</td>
                    <td>${player.date_of_birth}</td>
                    <td>${player.is_international ? 'Yes' : 'No'}</td>
                    <td>${player.innings_played}</td>
                    <td>${player.catches_taken}</td>
                    <td>${player.run_outs}</td>
                    <td>${player.total_runs}</td>
                    <td>${player.strike_rate}</td>
                    <td>${player.num_thirties}</td>
                    <td>${player.num_fifties}</td>
                    <td>${player.num_centuries}</td>
                    <td>${player.num_stumpings}</td>
                    <td>${player.bowling_average}</td>
                    <td>${player.bowling_economy}</td>
                    <td>${player.overs_bowled}</td>
                    <td>${player.wickets_taken}</td>
                    <td>${player.best_bowling}</td>
                </tr>
            </tbody>
        </table>
    `;
}


document.getElementById('searchForm').addEventListener('submit', function(event) {
            event.preventDefault();
            searchPlayerById();
        });
