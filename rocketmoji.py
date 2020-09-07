XAUTHTOKEN = ''
XUSERID = ''
TOKEN_FILE = 'token.txt'
"""
use emoji yaml files like the ones found here:
https://github.com/lambtron/emojipacks
"""

"""
Example curl API call to be replicated
#/bin/bash
curl -H "X-Auth-Token: " \
     -H "X-User-Id: " \
     http://localhost:3000/api/v1/emoji-custom.list


curl -H "X-Auth-Token: " \
     -H "X-User-Id: " \
     -F "emoji=@7zYM751.png" \
     -F "name=bender" \
     -F "alias=" \
     http://localhost:3000/api/v1/emoji-custom.create
"""

import yaml
import os
from urllib.request import urlopen
from requests import get

#set tokens from file
def get_tokens(tokenf = TOKEN_FILE):
    f = open(tokenf)
    lines = f.read().split('\n')
    f.close()
    auth = lines[0].split(',')[1]
    uid = lines[1].split(',')[1]
    return (auth, uid)

#retrieve emoji yaml file
def get_emoji_yaml( emoji_url ):
    emoji_response = urlopen(emoji_url)
    emoji_yaml = yaml.load(emoji_response.read())
    return emoji_yaml

def batch_save_emojis( emoji_yaml ):
    #make dir for temp saving files
    tmpdir = "/tmp/" + emoji_yaml['title']
    os.mkdir(tmpdir)

    emojis = emoji_yaml['emojis']
    print(emojis)
    for emoji in emojis:
        name = emoji['name']
        url = emoji['src']
        filename = name + url[url.rfind('.'):]
        # print(name)
        # print(url)
        # print(filename)
        filename = tmpdir + '/' + filename
        f = open(filename, 'wb')
        response = get(url)
        f.write(response.content)
        emoji_create_api_call(filename, name)

    #get rid of emoji files
    os.system('rm -rf ' + tmpdir)

'''
ideally, should be able to make API call using requests.
Have not succedded, should look something like:

headers = {'X-Auth-Token': '',
           'X-User-Id': ''}
data = {'emoji': open('bender.png', 'rb'),
        'name': 'bender' }
r = requests.post('http://localhost:3000/api/v1/emoji-custom.create', data=data, headers = headers)
r.txt

until that is working, using os.system instead
'''

def emoji_create_api_call(emojifile, emojiname):
    cmd = 'curl -H "X-Auth-Token: %s" '%XAUTHTOKEN
    cmd+= '-H "X-User-Id: %s" '%XUSERID
    cmd+= '-F "emoji=@'
    cmd+= emojifile + '" '
    cmd+= '-F "name=' + emojiname + '" '
    cmd+= 'http://localhost:3000/api/v1/emoji-custom.create'
    print(emojiname)
    print(cmd)
    print()
    os.system(cmd)

(XAUTHTOKEN, XUSERID) = get_tokens()
emoji_yaml_url = input("URL for YAML file: ")
emoji_yaml = get_emoji_yaml(emoji_yaml_url)
batch_save_emojis( emoji_yaml )
