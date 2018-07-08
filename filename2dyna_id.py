#!/usr/bin/env python3
# Dynalist to Markdown

import requests
import json
import os
import sys

#
# const
#
Dynalist_API = 'https://dynalist.io/api/v1'

#
# 環境変数からAPI_secret_tokenを取得
#
API_secret_token = os.getenv("Dynalist_API_KEY", "")
if API_secret_token == "":
    print("You need to set Dynalist_API_KEY in .bashrc!")
    sys.exit(1)

def get_file_list():
    API_URL = Dynalist_API + '/file/list'

    header = {"Content-Type" : "application/json"}
    payload = {'token': API_secret_token}

    res = requests.post(API_URL, json.dumps(payload), headers=header)
    return res.json()


def lookup_file(file_list, file_name):
    for n in file_list['files']:
        if n['type'] == 'document':
            if n['title'] == file_name:
                return n['id']
    return None


def filename_to_fileID(file_name):
    file_list = get_file_list()
    id = lookup_file(file_list, file_name)
    return id


def all_fileID():
    file_list = get_file_list()
    for n in file_list['files']:
        if n['type'] == 'document':
            print(n['id'] + " " + n['title'])


if __name__ == "__main__":

    if len(sys.argv) == 1:
        # 全ファイル出力
        all_fileID()
        sys.exit(0)

    elif len(sys.argv) == 2:
        # 特定ファイル出力
        id = filename_to_fileID(sys.argv[1])
        if id is not None:
            print(id)
            sys.exit(0)
        else:
            print("error")
            sys.exit(1)
    else:
        print(sys.argv[0] + " -> Display all files ID")
        print(sys.argv[0] + "'file_name' -> display ID of specific file")
        sys.exit(1)

