import sys
import pandas as pd
from utils import *

"""
Get app details using Steam API. This API have limits 200 request/5 minutes.
So I make it to get the data in batch (200 request/batch in 5 minutes). 
You can edit batch_size (number of request) but it doesn't make it faster.
I design one batch takes 5 minutes, so can you can run it more than one batch
and it will have no waiting time when process the next batch.
"""

def parse_steam_request(appid, keys=None):
    url = "http://store.steampowered.com/api/appdetails/"
    parameters = {"appids": appid}

    json_data = get_request(url, parameters=parameters)
    json_app_data = json_data[str(appid)]

    if json_app_data['success']:
        if keys:
            data = {}
            for key in keys:
                data[key] = str(json_app_data['data'].get(key, ''))
                if data[key] == 'None':
                    data[key] = ''
            return data
        data = json_app_data['data']
        for key in data.keys():
            if data[key] is None or data[key]=='None':
                data[key]=''
        return data


def get_steam_data(batch_size):
    end = batch_size

    # Create initial csv
    directories = ['apps_detail','apps_dump']
    [create_dir(directory) for directory in directories]
    

    # Reads csv
    app = pd.read_csv('apps/apps_initial.csv')['appid'].to_list()

    try:
        detail = pd.read_csv('apps_detail/apps_details_initial.csv')['steam_appid'].to_list()
    except:
        detail = []

    try:
        unused = pd.read_csv('apps_dump/unused_appid.csv', header=None)[0].to_list()
    except:
        unused = []

    try:
        double = pd.read_csv('apps_dump/double_appid.csv', header=None)[0].to_list()
    except:
        double = []

    appid = sorted(list(set(app) - set(detail).union(set(unused), set(double)))) 
    
    apps_detail_csv = "apps_detail/apps_details_initial.csv"

    column = [
        'type', 'name', 'steam_appid', 'required_age', 'is_free', 'controller_support', 'dlc',
        'detailed_description', 'about_the_game', 'short_description', 'supported_languages', 'header_image', 'website', 'pc_requirements',
        'mac_requirements', 'linux_requirements', 'legal_notice', 'drm_notice', 'developers', 'publishers', 'demos',
        'price_overview', 'platforms', 'metacritic', 'categories', 'genres', 'release_date', 'support_info'
    ]

    cnt = 0
    t0 = time.time()
    if len(appid) != 0:
        for start in range(end):
            detail = parse_steam_request(appid[start], column)
            if detail:
                cnt += 1
                apps_detail = [detail]
                create_csv_from_dict(apps_detail_csv, apps_detail, column)

                if detail['steam_appid'] != appid[start]:
                    create_csv('apps_dump/double_appid.csv', [str(appid[start])])
                
            else:
                create_csv('apps_dump/unused_appid.csv', [str(appid[start])])

            t1 = time.time()
            print(f"Elapsed time {t1-t0:.2f} seconds.", end="\r")
            print(end='\x1b[2K')

        t2 = time.time()
        print(f"Success get {cnt} data.")
        print(f"Completed in {t2-t0:.2f} seconds.")
        return t2-t0
    return 0


if __name__ == "__main__":
    batch = int(sys.argv[1])
    batch_size = 200

    for i in range(batch):
        print(f"========Batch {i}========")
        t0 = get_steam_data(batch_size)
        print('')
        if batch > 1 and i < batch-1:
            t = int(300 - t0)
            if t > 0:
                while t > 0:
                    print(f"Batch {i+1} start in {t} seconds.", end='\r')
                    print(end='\x1b[2K')
                    time.sleep(1)
                    t -= 1
        if t0 == 0:
            print("Done.")
            break

    df = pd.read_csv('apps_detail/apps_details_initial.csv').drop_duplicates().sort_values('steam_appid')
    df.to_csv('apps_detail/apps_details_initial.csv',index=False) 