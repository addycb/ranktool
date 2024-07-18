 
import sys
import parse
import api
import os


#if windows is os: run color command
if os.name == 'nt':
    os.system('color')




CRED = '\033[91m'
CGREEN = '\033[92m'
CBLUE = '\033[94m'
CORANGE = '\033[93m'
CDARKBLUE = '\033[34m'
CGRAY = '\033[90m'
CYELLOW = '\033[33m'
CSILVER='\033[37m'
CSKYBLUE='\033[36m'
CPURPLE='\033[35m'
CTURQOISE='\033[96m'

CEND = '\033[0m'
CUNDERLINE = '\033[4m'

rolemap={
    "tank":CBLUE,
    "damage":CRED,
    "support":CGREEN
}

rankmap={
    "bronze":CDARKBLUE,
    "silver":CGRAY,
    "gold":CYELLOW,
    "platinum":CSILVER,
    "diamond":CSKYBLUE,
    "master":CORANGE,
    "grandmaster":CTURQOISE,
    "champion":CPURPLE,
    "top500":CRED
}

#for rank in rankmap:
#    print(rankmap[rank]+rank+CEND)

print("Welcome to the Overwatch Team Rank Checker")

API_KEY=api.getkey()
if API_KEY is None:
    API_KEY=0
while not api.testkey(API_KEY) or API_KEY==0:
    print("No Valid API Key Found")
    print("Enter startGG API Key:")
    API_KEY=input()
    api.setkey(API_KEY)
print("API Key Confirmed")

print("Enter match url:")
url=input()
tournament_slug, set_id = parse.extract_ids(url)
#print(f"Tournament Slug: {tournament_slug}, Set ID: {set_id}\n")



team1,team2 = api.get_linked_accounts(tournament_slug, set_id,API_KEY)
print(CRED+"Team 1:", team1,CEND+"\n")
print(CBLUE+"Team 2:", team2,CEND+"\n")
print(CYELLOW+"Select A Team (1 or 2):\n"+CEND)
teamnum = int(input())
print("\n")
#Call overfast api to get the player ranks on competitive pc for the selected team
for player in team1 if teamnum==1 else team2:
    response=api.getplayerinfo(player['blizzard_id'])
    print(CORANGE+"Player BattleNet ID:",player['blizzard_id'],CEND+"\n")
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
                print(rolemap[role]+f"Season {season} {role} Rank: "+rankmap[division]+f" {division} {tier}"+CEND)

    print(CUNDERLINE+"https://www.overbuff.com/players/"+player['blizzard_id'],CEND+"\n")
