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
                applyTeamFilters(data.matches_data);
            } else {
                displayNoMatchesFound();
            }
        })
        .catch(error => {
            console.error('Error fetching match data:', error);
            displayNoMatchesFound();
        });
}

function applyTeamFilters(matches) {
    const teamA = document.getElementById('teamADropdown').value;
    const teamB = document.getElementById('teamBDropdown').value;


    let filteredMatches = matches.filter(match => {
        const matchesTeamA = !teamA || match.Team_A_Name === teamA;
        const matchesTeamB = !teamB || match.Team_B_Name === teamB;
        return matchesTeamA && matchesTeamB;
    });

    if (filteredMatches.length > 0) {
        displayMatches(filteredMatches);
    } else {
        displayNoMatchesFound();
    }
}

function displayMatches(matches) {
    const table = document.getElementById('matchesTable');
    table.innerHTML = '';
    const header = `
        <thead>
        <tr>
            <th>Match ID</th>
            <th>Team A</th>
            <th>Team B</th>
            <th>Venue</th>
           <th>First Umpire</th>
           <th>Second Umpire</th>
           <th>Seating_Capacity</th>
           <th>Pitch Outfield</th>
            <th>Date</th>
            <th>Time</th>
        </tr>
        </thead>`;

    let rows = matches.map(match => `
    <tbody>
        <tr>
            <td>${match.Match_ID}</td>
            <td>${match.Team_A_Name}</td>
            <td>${match.Team_B_Name}</td>
            <td><a href="#" onclick="fetchVenueDetails('${match.Venue}'); return false;">${match.Venue}</a></td>
            <td>${match.First_Umpire}</td>
            <td>${match.Second_Umpire}</td>
            <td>${match.Seating_Capacity}</td>
            <td>${match.Pitch_Outfield}</td>
            <td>${match.Date}</td>
            <td>${match.Time}</td>
        </tr>
        </tbody>`
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

function ensureModalExists() {
    if (!document.getElementById('venueModal')) {
        console.log('Modal does not exist, needs to be created or initialized.');
    } else {
        console.log('Modal exists.');
    }
}



function fetchVenueDetails(venueName) {
    fetch(`/api/venue/${encodeURIComponent(venueName)}`)
        .then(response => {
            if (!response.ok) throw new Error('Venue not found');
            return response.json();
        })
        .then(data => {
            ensureModalExists();
            const modalBody = document.querySelector('#venueModal .modal-body');
            modalBody.innerHTML = `
                <strong>Name:</strong> ${data.name}<br>
                <strong>Location:</strong> ${data.location}<br>
                <strong>Capacity:</strong> ${data.capacity}<br>
                <strong>Details:</strong> ${data.other_details}`;
            $('#venueModal').modal('show');
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function fetchTeamComposition(year, teamName) {
    let url;
    if (teamName) {
        url = `/teamComposition/${encodeURIComponent(year)}/${encodeURIComponent(teamName)}`;
    } else {
        url = `/allTeamCompositions/${encodeURIComponent(year)}`;
    }

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch team composition');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            if (data && Object.keys(data).length > 0) {
                if (teamName) {
                    displayTeamCompositionOnly(data);
                } else {
                   displayTeamComposition(data);
                }
            } else {
                alert('No team composition data available.');
            }
        })
        .catch(error => {
            console.error('Failed to fetch team composition', error);
            alert('Failed to fetch team composition');
        });
}


function displayTeamComposition(teamData) {
    const teamList = document.getElementById('teamList');
    teamList.innerHTML = '';

    Object.entries(teamData.team_compositions).forEach(([teamName, info]) => {
        const teamContainer = document.createElement('div');
        teamContainer.className = 'team-container';

        const teamHeader = document.createElement('h3');
        teamHeader.textContent = teamName;

        const toggleButton = document.createElement('button');
        toggleButton.textContent = 'Team Composition Details';
        toggleButton.onclick = () => toggleDetails(teamName);

        const detailsDiv = document.createElement('div');
        detailsDiv.id = teamName + '-details';
        detailsDiv.style.display = 'none';
        detailsDiv.innerHTML = `
            <strong>Captain:</strong> ${info.leadership.Captain || 'None'}<br>
            <strong>Coach:</strong> ${info.leadership.Coach || 'None'}<br>
            <strong>Players:</strong> ${listPlayers(info.players)}
        `;

        teamContainer.appendChild(teamHeader);
        teamContainer.appendChild(toggleButton);
        teamContainer.appendChild(detailsDiv);
        teamList.appendChild(teamContainer);
    });
}

function listPlayers(players) {
    if (!players || players.length === 0) return 'No players';
    return players.map(player => `${player.Player} (ID: ${player.Player_id})`).join(', ');
}

function toggleDetails(teamName) {
    const details = document.getElementById(teamName + '-details');
    if (details) {
        details.style.display = details.style.display === 'none' ? 'block' : 'none';
    }
}

function displayTeamCompositionOnly(data) {
    if (!data || !data.team_details) {
        console.error('No team details data available.');
        return;
    }

    const teamDetails = data.team_details;

    const container = document.getElementById('teamDetailsContainer');
    container.innerHTML = '';

    const table = document.createElement('table');
    table.className = 'table table-striped';

    const leadership = teamDetails.leadership;
    let html = `
        <thead>
            <tr><th colspan="2">Leadership</th></tr>
        </thead>
        <tbody>
            <tr>
                <td>Captain</td>
                <td>${leadership.Captain} (ID: ${leadership.Captain_id})</td>
            </tr>
            <tr>
                <td>Coach</td>
                <td>${leadership.Coach} (ID: ${leadership.Coach_id})</td>
            </tr>
        </tbody>
    `;


    html += `
        <thead>
            <tr><th colspan="3">Players</th></tr>
        </thead>
        <tbody>
    `;
    teamDetails.players.forEach(player => {
        html += `
            <tr>
                <td>${player.Player}</td>
                <td>ID: ${player.Player_id}</td>
                <td>Team: ${player.Team}</td>
            </tr>
        `;
    });

    html += '</tbody>';
    table.innerHTML = html;
    container.appendChild(table);
}






