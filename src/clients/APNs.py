import os
import time
import httpx
from typing import Optional

import jwt

# APNs mandates that tokens live at most 1 hour
# 50 minutes in seconds
TOK_LIFE = 3300
ALGO = 'ES256'

DEV_SRV = 'https://api.sandbox.push.apple.com'
LIVE_SRV = 'https://api.push.apple.com'

DEFAULT_PORT = 443
ALTERNATIVE_PORT = 2197

key_id = os.environ.get('APNS_KEYID', 'secret')
team_id = os.environ.get('APPLE_TEAMID', 'secret')
key_path = os.environ.get('SECRET_PATH', 'secret')

class TokenCreds(object):
    def __init__(self,
                 key_id: str,
                 key_path: str,
                 team_id: str,
                 algo: str = ALGO,
                 tok_life: int = TOK_LIFE,
                 ) -> None:
        self._key = self._load_key(key_path)
        self._key_id = key_id
        self._team_id = team_id
        self._algo = algo
        self._tok_life = tok_life
        self._last_issued = None
        self._token = None
    
    @staticmethod
    def _load_key(key_path: str) -> str:
        secret = ''
        if key_path:
            with open(key_path, 'r') as f:
                secret = f.read()
        return secret

    def _is_tok_dead(self) -> bool:
        return time.time() > (self._last_issued + self._tok_life)

    def _get_token(self) -> str:
        if self._token is None or self._is_tok_dead():
            # Mint a new tokecoin NFT
            self._last_issued = time.time()
            tok_dict = {
                'iss': self._team_id,
                'iat': self._last_issued,
            }
            headers = {
                'alg': self._algo,
                'kid': self._key_id,
            }
            self._token = jwt.encode(tok_dict, self._key, algorithm=self._algo, headers=headers)
        return self._token
    
    def authorize(self) -> str:
        return f"bearer {self._get_token()}"


class APNsClient(object):
    def __init__(self):
        self._serv = LIVE_SRV
        self._port = DEFAULT_PORT
        self._credentials = TokenCreds(key_id, key_path, team_id)
        self._init_client()

    def _init_client(self):
        # TODO: close clients after some amount of time?
        # TODO: detect network interruptions and attempt reconnects
        self._client = httpx.AsyncClient(http2=True)

    async def send_noti(self,
                        topic: str,
                        push_type: str,
                        device_hex: str,
                        payload: str,
                        expiry: Optional[int] = None,
                        priority: Optional[str] = None,
                        collapse_id: Optional[str] = None):
        headers = {}
        headers['authorization'] = self._credentials.authorize()
        headers['apns-topic'] = topic
        headers['apns-push-type'] = push_type
        if expiry:
            headers['apns-expiration'] = expiry
        if priority:
            headers['apns-priority'] = priority
        if collapse_id:
            headers['apns-collapse-id'] = collapse_id

        url = f"{self._serv}/3/device/{device_hex}"
        r = await self._client.post(url, headers=headers, content=payload)
        print(r.http_version)
        print(r.status_code)
        print(r.content)
