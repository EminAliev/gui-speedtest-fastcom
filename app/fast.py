import asyncio
import json
import time
import urllib.parse
import urllib.request

import aiohttp

URL = 'https://fast.com'
API_URL = "https://api.fast.com"


class Fast(object):
    async def test_speed(self, session: aiohttp.ClientSession, url):
        result = 0
        async with session.get(url) as response:
            while True:
                chunk = await response.content.read(56)
                if not chunk:
                    break
                else:
                    result += len(chunk)
        return result

    async def create_session(self):
        return aiohttp.ClientSession()

    def script_find_text(self, text, start, finish):
        start_f = text.find(start)
        start_l = len(start)
        end_find = text.find(finish, start_f + start_l)
        if -1 in (start_f, end_find):
            return ""
        else:
            return text[start_f + start_l:end_find]

    def get_token(self):
        request = urllib.request.Request(URL)
        response_file = urllib.request.urlopen(request)
        response = response_file.read().decode()
        script = self.script_find_text(response, '<script src="', '"')
        script_request = urllib.request.Request(URL + script)
        script_request_file = urllib.request.urlopen(script_request)
        script_response = script_request_file.read().decode()
        token = self.script_find_text(script_response, 'token:"', '"')
        return token

    def download(self, token='', timeout=None):
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        token = token or self.get_token()
        api_params = {
            'https': True,
            'urlCount': 5,
            'token': token
        }
        query = urllib.parse.urlencode({i: str(j) for i, j in api_params.items()})
        url = API_URL + '/netflix/speedtest?' + query
        request = urllib.request.Request(url)
        request_file = urllib.request.urlopen(request)
        response = request_file.read().decode()
        response_json = json.loads(response)
        start = time.time()
        with aiohttp.ClientSession() as session:
            urls_param = [self.test_speed(session, url['url']) for url in response_json]
            futures = asyncio.gather(*urls_param)
            try:
                event_loop.run_until_complete(asyncio.wait_for(futures, timeout=timeout))
            except asyncio.TimeoutError:
                event_loop.run_until_complete(futures)
            finally:
                event_loop.close()
        end = time.time()
        speed_const = sum(futures.result()) * 8 / 1024 / 1024
        return round(speed_const / (end - start), 1)


if __name__ == '__main__':
    fc = Fast()
    print('Start')
    print('Download Speed: ')
    x = round(fc.download(), 2)
    print(str(x) + 'MB/s')
