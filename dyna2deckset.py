#!/usr/bin/env python3
#coding:utf-8
# Dynalist to Markdown for Deckset2

import requests
import json
import os
import sys
import copy
import time

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


def get_body(file_id):
    API_URL = Dynalist_API + '/doc/read'

    header = {"Content-Type" : "application/json"}
    payload = {
		'token': API_secret_token,
		'file_id': file_id
	}
    res = requests.post(API_URL, json.dumps(payload), headers=header)
    json_data = res.json()
    return json_data

#
# root（file_data['nodes'])からtext_listを生成する[(id, text), ...]
#
def build_element_list(root):
    element_list = []
    for node in root:
        if 'children' in node:
            children =  node['children']
        else:
            children = None
        element_list.append((node['id'], node['content'], node['checked'], node['note'], children))
        #print((node['id'], node['content']))
    return element_list


#
# text_listとidからtextを抽出
#
def lookup_element(element_list, id):
    for t in element_list:
        if id == t[0]:
                return t
    return ''


#
# 順序でリストを作る
#
def each_list_order(element_list, text_list, id, children, indent_lv):
    for l in children:
        element = lookup_element(element_list, l)
        #print(element)
        text = element[1].strip()
        if text == '':
            pass
        elif text.startswith('---'):
            pass
        else:
            text_list.append((indent_lv, text, element[2], element[3]))

        if element[4] is not None:
            #print(element[4], indent_lv + 1)
            each_list_order(element_list, text_list, element[0], element[4], indent_lv + 1)


def do_list_order(element_list, file_data):
    indent_lv = 0
    text_list =  []
    text_list.append((indent_lv,file_data['nodes'][0]['content'].strip(), file_data['nodes'][0]['checked'], file_data['nodes'][0]['note']))
    #print(indent_lv, file_data['nodes'][0]['content'])

    each_list_order(element_list, text_list, file_data['nodes'][0]['id'], file_data['nodes'][0]['children'], indent_lv + 1)

    return text_list


def export_text(text):
    if text.startswith('#'):
        return '\\' + text
    elif text.startswith('!['):
        return text + '\n' + '\n'
    elif text.startswith('---'):
        return '\n'
    elif text.startswith('- '):
        return text + '\n'
    elif text.startswith('1. '):
        return text + '\n'
    else:
        return text

def text_list_to_markdown(file, text_list):

    file.write('# '  + export_text(text_list[0][1]))
    file.write('\n')

    h2_done = False
    for n in range(1, len(text_list) -1):
        prev_lv    = text_list[n - 1][0]
        current_lv = text_list[n    ][0]
        next_lv    = text_list[n + 1][0]

        #print(n, 'Lv = ', prev_lv, current_lv, next_lv)

        if current_lv == 1:
            if h2_done:
                file.write('\n')
                file.write('---\n')
                file.write('\n')
                file.write('#' * next_lv + ' '  + export_text(text_list[n][1]) + '\n')
                file.write('\n')
            else:
                file.write(export_text(text_list[n][1]))
                file.write('\n')
            h2_done = True

        elif current_lv < next_lv:
            file.write('\n')
            file.write('#' * next_lv + ' '  + export_text(text_list[n][1]) + '\n')
            file.write('\n')

        elif current_lv == next_lv:
            file.write(export_text(text_list[n][1]))

        else:
            file.write(export_text(text_list[n][1]))
            file.write('\n')
    file.write(export_text(text_list[n + 1][1]) + '\n')


def main(id, out_file):
    SLEEP_TIME = 15

    try:
        prev_json = {}
        while True:
            file_data = get_body(id)
            if file_data is None:
                print("Can't find file")
                sys.exit(1)

            if prev_json != file_data:
                #print("making .md file!")
                #print(file_data)
                prev_json = copy.deepcopy(file_data)

                element_list = build_element_list(file_data['nodes'])
                text_list = do_list_order(element_list, file_data)

                file = open(out_file, 'w')
                text_list_to_markdown(file, text_list)
                file.close()
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":

    #FILE = "./hogehoge.md"
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
        sys.exit(0)

    else:
        print(sys.argv[0] + "'file_id target.md' -> convert to markdown")
        sys.exit(1)
