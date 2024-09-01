from flask import Flask, render_template, request
from api import get_linked_accounts, getplayerinfo, testkey, getkey
import parse

app = Flask(__name__)

# Load API key from file or environment variable
API_KEY = "629d0172bf008686a578b8e7e874ee0b"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search(): 
    url = request.form.get('url', 'nourl')
    url=url.strip()
    #print(f"Received URL: {url}") 
    
    if not parse.validate_url(url):
        return render_template('results.html', error='Invalid URL. Please provide a valid start.gg match URL.')

    # Extract tournament_slug and set_id from URL
    tournament_slug, set_id = parse.extract_ids(url)

    if not tournament_slug or not set_id:
        return render_template('results.html', error='URL does not contain valid tournament or set information.')

    if not testkey(API_KEY):
        return render_template('results.html', error='Invalid API Key')
    #Tests passed
    #print("Tests passed")
    try:
        team1, team2 = get_linked_accounts(tournament_slug, set_id, API_KEY)
    except Exception as e:
        return render_template('results.html', error=f'Error fetching linked accounts: {e}')
    #print("Teams fetched")
    results_team1 = fetch_team_results(team1)
    results_team2 = fetch_team_results(team2)
   # print("Results fetched")
    #print(results_team1)
    #print("Results2 fetched")
    #print(results_team2)

    return render_template('results.html', results_team1=results_team1, results_team2=results_team2)

def fetch_team_results(team):
    results = []
    for player in team:
        #print("blizzard id: "+player['blizzard_id'])
        try:
            response = getplayerinfo(player['blizzard_id'])
            #print("got player info")
            player_info = {
                'blizzard_id': player['blizzard_id'],
                'roles': {}
            }
            for role in ["tank", "damage", "support"]:
                role_data = response.get('competitive', {}).get('pc', {}).get(role)
                if role_data:
                    player_info['roles'][role] = {
                        'season': role_data.get('season', 'Unknown'),
                        'division': role_data.get('division', 'Unknown'),
                        'tier': role_data.get('tier', 'Unknown')
                    }
                else:
                    player_info['roles'][role] = 'No data'
            results.append(player_info)
        except Exception as e:
            #print("player info failed")
            results.append({'blizzard_id': player['blizzard_id'], 'roles': {'error': str(e)}})
    return results

if __name__ == '__main__':
    app.run(debug=True)
