#! /usr/local/bin/python3
#   Copyright (c) 2020.
#   You can freely change the code part, but you must follow the MIT protocol
#   You cannot delete any information about UTS
#   You cannot use this program to disrupt social order.

import sys
import json
import os
import shelve
import requests

file_lists = os.listdir(os.path.expanduser('~'))
if 'mop.json' in file_lists:
    file = open(os.path.expanduser('~/mop.json'), 'r')
    mop_db_path = json.load(file)
    file.close()
    mop_db = shelve.open(mop_db_path + 'mop')
    LANGUAGE = mop_db['language']
    mop_db.close()
else:
    sys.exit()

URL = 'https://api.github.com/repos/underthestars-zhy/MacOS-Plugins/releases'

if sys.argv[1] == 'token':
    token = input()
    mop_db = shelve.open(mop_db_path + 'mop')
    mop_db['update_token'] = '?access_token=' + token
    mop_db.close()
    print('Done.')
else:
    mop_db = shelve.open(mop_db_path + 'mop')
    token = mop_db['update_token']
    mop_db.close()

    URL += token

    main_json_r = requests.get(URL)
    main_json_r.raise_for_status()
    main_json = main_json_r.json()

    update_dict = dict(main_json[0])

    print('NodeID: ' + update_dict['node_id'])
    print('TagName: ' + update_dict['tag_name'])
    print('Name: ' + update_dict['name'])

    update_assets = dict(update_dict['assets'][0])
    down_url = update_assets['browser_download_url']
    print('DownURL: ' + down_url)
    main_json_r.close()

    update_r = requests.get(down_url)
    update_r.raise_for_status()
    with open(mop_db_path + 'mop.py', "wb") as code:
        code.write(update_r.content)
    update_r.close()

    os.system('mop -init update')

    print('Done.')
