from utils import *
import pandas as pd

"""
Get game stat and review from Steamspy. I only select columns  
['appid', 'name', 'developer', 'publisher', 'positive', 'negative'],
you can modify it and please read all available column in Steamspy
documentation.
"""

def steamspy_request(appid, keys=None):
    url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
    json_app_data = get_request(url)
    if keys:
            data = {}
            for key in keys:
                data[key] = str(json_app_data.get(key, ''))
                if data[key] == 'None':
                    data[key] = ''
            return data
    data = json_app_data
    for key in data.keys():
        if data[key] is None or data[key]=='None':
            data[key]=''
    return data

def get_steamspy():
    # Create initial csv
    directories = ['apps_stats']
    [create_dir(directory) for directory in directories]
    apps_stats_csv = "apps_stats/apps_stats_initial.csv"
    
    # Reads csv
    app_detail = pd.read_csv('apps_detail/apps_details_initial.csv')['steam_appid'].to_list()
    try:
        app_stat = pd.read_csv('apps_stats/apps_stats_initial.csv')['appid'].to_list()
    except:
        app_stat = []

    appid = set(app_detail)-set(app_stat)
    column = [
            'appid', 'name', 'developer', 'publisher', 'positive', 'negative'
        ]
    
    t0 = time.time()
    for id in appid:
        stats = [steamspy_request(id,keys=column)]
        create_csv_from_dict(apps_stats_csv, stats, column)
        t1 = time.time()
        print(f"Elapsed time {t1-t0:.2f} seconds.", end="\r")
        print(end='\x1b[2K')
        time.sleep(0.5)

if __name__ == "__main__":
    get_steamspy()