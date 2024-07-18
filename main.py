from urllib.parse import urlparse, unquote
import requests
import sys
import curses

def extract_ids(url):
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.split('/')
    
    tournament_slug = None
    set_id = None
    
    for i, segment in enumerate(path_segments):
        if segment == 'tournament':
            if i + 1 < len(path_segments):
                tournament_slug = path_segments[i + 1]
        if segment == 'set':
            if i + 1 < len(path_segments):
                set_id = path_segments[i + 1]
    
    return tournament_slug, set_id

# Example usage
url=sys.argv[1]
tournament_slug, set_id = extract_ids(url)
print(f"Tournament Slug: {tournament_slug}, Set ID: {set_id}\n")

# Replace 'YOUR_API_KEY' with your actual Start.gg API key
API_KEY = '6ad9e4b35c5ff72f95e0bf3187f8058c'
BASE_URL = 'https://api.start.gg/gql/alpha'

# Function to execute a GraphQL query
def execute_query(query, variables):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(BASE_URL, json={'query': query, 'variables': variables}, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

def get_linked_accounts(tournament_slug, set_id):
    query = '''
    query SetParticipants($setId: ID!) {
        set(id: $setId) {
            slots {
                entrant {
                    participants {
                            connectedAccounts
                    }
                }
            }
        }
    }
    '''
    
    variables = {
        'setId': set_id
    }
    
    result = execute_query(query, variables)
    slots = result['data']['set']['slots']
    
    linked_accounts = []
    team1=[]
    team2=[]
    for slot in slots:
        for participant in slot['entrant']['participants']:
            player_info = {
                'blizzard_id': participant['connectedAccounts']['battlenet']['value'].replace('#', '-')
            }            
            if slot==slots[0]:
                team1.append(player_info)
            else:
                team2.append(player_info)
    return team1,team2
# Example usage
team1,team2 = get_linked_accounts(tournament_slug, set_id)
print("Team 1:", team1,"\n")
print("Team 2:", team2,"\n")
print("Select A Team (1 or 2):")
teamnum = int(input())
#Call overfast api to get the player ranks on competitive pc for the selected team
for player in team1 if teamnum==1 else team2:
    response = requests.get(f"https://overfast-api.tekrop.fr/players/{player['blizzard_id']}/summary")
    response=response.json()
    print("Player BattleNet ID:",player['blizzard_id'],"\n")
    #If (error) or comp is null
    if len(response.keys())==1 or response['competitive']=="null":
        print("Player has not played competitive on PC, or has a private account.")
    else:
        for role in ["tank", "damage", "support"]:
            role_data = response.get('competitive', {}).get('pc', {}).get(role)
            if role_data is None:
                print(f"Player has not played competitive {role} role on PC recently. Historical data may be available.")
            else:
                season = response['competitive']['pc'].get('season', 'Unknown')
                division = role_data.get('division', 'Unknown')
                tier = role_data.get('tier', 'Unknown')
                print(f"Season {season} {role} Rank: {division} {tier}")

    print("https://www.overbuff.com/players/"+player['blizzard_id'],"\n")
