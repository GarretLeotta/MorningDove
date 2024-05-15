#!/usr/bin/env python

import os
import time
import asyncio

import httpx
import jwt

#only for dev environment
if not os.environ.get('APNS_KEYID'):
    from dotenv import load_dotenv
    load_dotenv()

key_id = os.environ.get('APNS_KEYID', 'secret')
team_id = os.environ.get('APPLE_TEAMID', 'secret')
with open(os.path.join('.', f"secrets/AuthKey_{key_id}.p8"), 'r') as f:
    secret = f.read()

my_device = os.environ.get('TEST_DEVICETOKEN', 'secret')

payload = '{"aps":{"alert":{"title":"Notification Title","subtitle":"New Message","body":"Message Content"}},"navigation":"chat:1"}'
topic = os.environ.get('APNS_TOPIC', 'secret')

DEV_SERV = 'https://api.sandbox.push.apple.com'
LIVE_SERV = 'https://api.push.apple.com'
SERV = LIVE_SERV

def create_token():
    # TODO: iat only valid for 1 hour, method to check expiry
    issued_at = time.time()
    tok_dict = {
        'iss': team_id,
        'iat': issued_at,
    }
    headers = {
        'alg': 'ES256',
        'kid': key_id,
    }
    return jwt.encode(tok_dict, secret, algorithm='ES256', headers=headers)

async def send_noti(client, token):
    headers = {}
    headers['authorization'] = f"bearer {token}"
    headers['apns-topic'] = topic
    headers['apns-push-type'] = 'alert'
    # TODO: apns-expiration
    headers['apns-priority'] = '5'
    
    # TODO: for chats, this is "chat{chatId}"
    # headers['apns-collapse-id'] = 4

    url = f"{SERV}/3/device/{my_device}"
    r = await client.post(url, headers=headers, content=payload)
    print(r.http_version)
    print(r.status_code)
    print(r.content)

async def main():
    client = httpx.AsyncClient(http2=True)
    token = create_token()
    await send_noti(client, token)
    

if __name__ == '__main__':
    asyncio.run(main())
