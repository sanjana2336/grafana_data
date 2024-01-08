#!/usr/bin/env python

"""Grafana dashboard exporter"""
from github import Github
import json
import os
import requests
import base64
import gc

# Grafana API URL
HOST = "xxxxxxxxxxxxxxx"

# Service account credentials (API Key or Token)
API_KEY = "xxxxxxxxxxxxxxxxxxxx"

DIR = '/Users/sanjana.jasud/Documents/graf/'
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
# GitHub access token
    access_token = 'xxxxxxxxxxxxxxxx'

    # Repository information
    repository_owner = 'xxxxx'
    repository_name = 'xxxxxx'

    #folder name in the github repo
    folder_file_path = 'grafana-backup/'
    github_base_url = "https://github.com/api/v3"
    api_base_url = f'{github_base_url}/repos/{repository_owner}/{repository_name}/contents'

    # Get the current working directorycd 
    #current_directory = os.getcwd()

    # List all files in the mentioned directory
    all_files = os.listdir(DIR)

    # Filter .json files
    json_files = [f for f in all_files if f.endswith('.json')]

    # Create an array of local file paths
    file_name = [os.path.join(DIR, filename) for filename in json_files]

    headers = {
        'Authorization': f'token {access_token}'
    }

    for local_file_path in file_name:
        file_name = os.path.basename(local_file_path)

        with open(local_file_path, 'rb') as file:
            file_content = file.read()

        # Create a file content base64 encoded
        content_base64 = base64.b64encode(file_content).decode('utf-8')

        # API endpoint URL for creating a new file
        api_url = f'{api_base_url}{folder_file_path}{file_name}'

        # Data for the API request
        data = {
            "message": f"Add {file_name}",
            "content": content_base64
        }

        # Make the API request to create the file
        response = requests.put(api_url, json=data, headers=headers)

        if response.status_code == 201:
            print(f'File {file_name} created successfully in {folder_file_path} of {repository_name}.')
       
        else  :       
            print(f'Already Exists {file_name}. Status code: {response.status_code}')

if __name__ == '__main__':
    main()
