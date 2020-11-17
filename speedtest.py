import bisect
import platform
import re
import timeit
from http.client import HTTPConnection
from math import sqrt, radians, sin, cos, asin
import time

from bs4 import BeautifulSoup
from requests import Session


class SpeedTestObject(object):
    def __init__(self, server=None, http=0, r=2):
        self.server = server
        self.http = http
        self.r = r

    user_agents = {
        'Linux': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
        'Windows': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
    }

    @property
    def server(self):
        if not self._server:
            self._server = self.get_better_server()
        return self._server

    @server.setter
    def server(self, server):
        self._server = server

    def client_connection(self, url):
        try:
            connection = HTTPConnection(url)
            connection.set_debuglevel(self.http)
            connection.connect()
            return connection
        except:
            pass

    def get_servers(self):
        with Session() as s:
            page_src = s.get(
                "https://c.speedtest.net/speedtest-servers-static.php",
                headers=self.user_agents
            )

        soup = BeautifulSoup(page_src.content, "lxml")
        servers = soup.select("servers server")

        return servers

    def ping(self, server=None):
        if not server:
            server = self.server
        connect = self.client_connection(server)
        seconds = []
        lowest = 0
        stamp = int(timeit.time.time() * 1000)
        for _ in range(5):
            start = time.time()
            connect.request('GET',
                            '/speedtest/latency.txt?x=%d' % stamp, None,
                            {'Connection': 'Keep-Alive'})
            response = connect.getresponse()
            response.read()
            current_ping = time.time() - start
            seconds.append(current_ping)
            if current_ping > lowest:
                lowest = current_ping
        seconds.remove(lowest)
        current_ping = sum(seconds) * 1000 / 4
        connect.close()
        return current_ping

    def get_better_server(self):
        connect = self.client_connection('c.speedtest.net')
        headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': self.user_agents.get(platform.system(), self.user_agents['Linux'])
        }
        connect.request('GET', '/speedtest-config.php?x=%d' % int(time.time() * 1000), None, headers)
        response = connect.getresponse()
        reply = response.read().decode('utf-8')
        match = re.search(
            r'<client ip="([^"]*)" lat="([^"]*)" lon="([^"]*)"', reply)
        location = None
        if match is None:
            return None
        location = match.groups()
        connect.request('GET', '/speedtest-servers.php?x=%d' % int(time.time() * 1000), None, headers)
        response = connect.getresponse()
        reply = response.read().decode('utf-8')
        list = re.findall(r'<server url="([^"]*)" lat="([^"]*)" lon="([^"]*)"', reply)
        client_lat = float(location[1])
        client_lon = float(location[2])
        list_servers = []
        for server in list:
            server_lat = float(server[1])
            server_lon = float(server[2])
            distance = self.distance(client_lon, client_lat, server_lon, server_lat)
            bisect.insort_right(list_servers, (distance, server[0]))
        better_host = (999999, '')
        for server in list_servers[:10]:
            match = re.search(r'http://([^/]+)/speedtest/upload\.php', server[1])
            if match is None:
                continue
            server_host = match.groups()[0]
            latency = self.ping(server_host)
            if latency < better_host[0]:
                better_host = (latency, server_host)
        if not better_host[1]:
            pass
        return better_host[1]

    def distance(self, lon1, lat1, lon2, lat2):
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km
