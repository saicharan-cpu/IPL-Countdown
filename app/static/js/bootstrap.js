function searchPlayerById() {
    const playerName = document.getElementById('searchInput').value;
    console.log("searching for player :"+playerName)
    if (playerName) {
        fetch(`/player/${encodeURIComponent(playerName)}`)
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

function fetchMatchesByYear(year) {
    fetch(`/matches/${encodeURIComponent(year)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch matches');
            }
            return response.json();
        })
        .then(data => {
            if (data.matches_data) {
                displayMatches(data.matches_data);
            } else {
                displayNoMatchesFound();
            }
        })
        .catch(error => {
            console.error('Error fetching match data:', error);
            displayNoMatchesFound();
        });
}

function displayMatches(matches) {
    const table = document.getElementById('matchesTable');
    table.innerHTML = ''; // Clear previous entries

    const header = `
        <tr>
            <th>Match ID</th>
            <th>Team A</th>
            <th>Team B</th>
            <th>Venue</th>
            <th>Date</th>
            <th>Time</th>
        </tr>`;
    let rows = matches.map(match => `
        <tr>
            <td>${match.Match_ID}</td>
            <td>${match.Team_A_Name}</td>
            <td>${match.Team_B_Name}</td>
            <td>${match.Venue}</td>
            <td>${match.Date}</td>
            <td>${match.Time}</td>
        </tr>`
    ).join('');

    table.innerHTML = header + rows;
}

function displayNoMatchesFound() {
    const table = document.getElementById('matchesTable');
    table.innerHTML = '<tr><td colspan="6">No matches found for selected year.</td></tr>';
}

document.addEventListener('DOMContentLoaded', function() {
console.log("Document loaded......");
    const dropdown = document.getElementById('yearDropdown');
    console.log("Dropdown is:", dropdown);
    document.getElementById('yearDropdown').addEventListener('change', function() {
        const selectedYear = this.value;
        console.log("selected year is:"+selectedYear);
        if (selectedYear) {
            fetchMatchesByYear(selectedYear);
        }
    });
});





