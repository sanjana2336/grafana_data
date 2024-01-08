#!/usr/bin/env python

"""Grafana dashboard exporter"""
import json
import os
import requests
import shutil
import datetime

# Grafana API URL
HOST = "xxxxxxxxxxxxxxxx"

# Service account credentials (API Key or Token)
API_KEY = "xxxxxxxxxxxxxxxxx"

DIR = '/Users/sanjana.jasud/Documents/git/graf/'

def main():
    headers = {'Authorization': 'Bearer %s' % (API_KEY,)}
    response = requests.get('%s/api/search?query=&' % (HOST,), headers=headers)
    response.raise_for_status()
    dashboards = response.json()

    if not os.path.exists(DIR):
        os.makedirs(DIR)

    for d in dashboards:
        print("Saving: " + d['title'])
        response = requests.get('%s/api/dashboards/uid/%s' % (HOST, d['uid']), headers=headers)
        data = response.json()['dashboard']
        dash = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        name = data['title'].replace(' ', '').replace('/', '').replace(':', '').replace('[', '').replace(']', '')
        print(DIR + name + '.json')
        tmp = open(DIR + name + '.json', 'w')
        tmp.write(dash)
        tmp.write('\n')
        tmp.close()

    #initialize the git repo via terminal
    now = datetime.datetime.today() 
    nTime = now.strftime("%d-%m-%Y %H:%M:%S")
    src_path = "graf/"
    dst_path = "status-dashboard/grafana_bkp:"
    dest = os.path.join(dst_path+nTime)
    shutil.copytree(src_path, dest ,dirs_exist_ok=True)

    #execute git add,commit and push via terminal to upload the files



if __name__ == '__main__':
    main()
