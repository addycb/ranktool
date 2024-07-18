import requests

def get_linked_accounts(tournament_slug, set_id,API_KEY):
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
    
    result = execute_query(query, variables,API_KEY)
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

# Function to execute a GraphQL query
def execute_query(query, variables,API_KEY):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post('https://api.start.gg/gql/alpha', json={'query': query, 'variables': variables}, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def testkey(key):
    """
    Test if the given API key works on Start.gg.

    Parameters:
    api_key (str): The API key to test.

    Returns:
    bool: True if the API key is valid, False otherwise.
    """
    url = "https://api.start.gg/gql/alpha"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    query = {
        "query": """
        query {
            currentUser {
                id
            }
        }
        """
    }

    response = requests.post(url, json=query, headers=headers)
    
    if response.status_code == 200:
        return True
    else:
        print("API Key is invalid.\nCreate or retrieve a personal access token at:\nhttps://www.start.gg/admin/user/rgbattack/developer\nClick On Developer Settings->Personal Access Tokens->Create Token")
        return False

def setkey(key):
    """
    Save the given key to a file named 'startggapikey'.

    Parameters:
    key (str): The API key to save.
    """
    with open("startggapikey", "w") as file:
        file.write(key)

def getkey():
    """
    Read the API key from the file named 'startggapikey'.

    Returns:
    str: The API key read from the file.
    """
    try:
        with open("startggapikey", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def getplayerinfo(blizzard_id):
    response = requests.get(f"https://overfast-api.tekrop.fr/players/"+str(blizzard_id)+"/summary")
    return response.json()