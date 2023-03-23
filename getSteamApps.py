import json
from operator import itemgetter
import pandas as pd
from utils import *

"""
Fetch all steam_appid and its name in json then convert it to csv.
"""

def get_steam_applist(applist_filename):
    url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json"
    applist = get_request(url)
    with open(applist_filename, 'w') as f:
        json.dump(applist, f)


# Fetch json and save to local
applist = "applist.json"
get_steam_applist(applist)

# Create initial csv
directory = "apps"
create_dir(directory)
apps_csv = f"{directory}/apps_initial.csv"

with open(applist, 'r') as f:
    applist_temp = json.loads(f.read())

apps = pd.DataFrame(applist_temp['applist']['apps']).drop_duplicates().to_dict('records')
apps = sorted(apps, key=itemgetter('appid'))
create_csv_from_dict(apps_csv, apps)

df = pd.read_csv(apps_csv).drop_duplicates().sort_values('appid')
df.to_csv(apps_csv,index=False)
