import os
import re
from http.client import HTTPConnection
from math import sqrt, radians, sin, cos, asin
from xml import etree
import time
import sys
from io import BytesIO
import urllib.request
from urllib.request import urlopen

from lxml import etree
import gzip


class SpeedTestObject(object):
    def __init__(self, server=None, http=0, r=3):
        self.server = server
        self.http = http
        self.r = r

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; OS X; rv:10.0.2) Gecko/20100101 Firefox/10.0.2',
        'Connection': 'keep-alive',
    }

    DOWNLOAD_FILES = ['500x500' '1500x1500', '2000x2000', '3000x3000', '4000x4000']

    @property
    def server(self):
        if not self._server:
            self._server = self.get_address_ping(self.get_best())
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

    def get_address_ping(self, list):
        servers = []
        for server in list:
            match = re.search(r'http://([^/]+)/speedtest/', server['url'])
            server_host = match.groups()[0]
            servers.append(server_host)
        return servers[0]

    def ping(self, server=None):
        """Ping server"""
        return round(self.get_best()[0]['latency'])

    def distance(self, lon1, lat1, lon2, lat2):
        """Calculating the distance between server and client"""
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km

    def zip_response(self, response):
        """Compressing the response"""
        fileobj = BytesIO(response.read())
        gzip_file = gzip.GzipFile(fileobj=fileobj)
        try:
            return gzip_file.read()
        except Exception as e:
            return fileobj.getvalue()

    def get_config(self):
        """Config about user information"""
        uri = "http://speedtest.net/speedtest-config.php?x=" + str(time.time())
        request = urllib.request.Request(uri, headers=self.headers)
        try:
            response = urlopen(request)
        except:
            sys.exit(1)
        config = etree.fromstring(self.zip_response(response))
        ip = config.find("client").attrib['ip']
        lat = float(config.find("client").attrib['lat'])
        lon = float(config.find("client").attrib['lon'])
        return {'ip': ip, 'lat': lat, 'lon': lon}

    def get_servers(self, servers):
        """List servers with lowest latency"""
        list_servers = []
        for server in servers:
            latency_now = self.check_latency(server['url'] + "latency.txt?x=" + str(time.time())) * 1000
            latency_now /= 2
            if latency_now == -1 or latency_now == 0:
                continue
            print("%0.0f ms TO %s (%s, %s) [%0.2f kylometers]" %
                  (
                      latency_now, server['url'], server['name'], server['country'],
                      server['distance']))
            server['latency'] = latency_now
            # 5 servers with latency
            if int(len(list_servers)) < int(5):
                list_servers.append(server)
            else:
                largest = -1
                for x in range(len(list_servers)):
                    if largest < 0:
                        if latency_now < list_servers[x]['latency']:
                            largest = x
                    elif list_servers[largest]['latency'] < list_servers[x]['latency']:
                        largest = x
                if largest >= 0:
                    list_servers[largest] = server
        return list_servers

    def check_latency(self, address):
        """Checking latency for server"""
        average = 0
        all = 0
        for i in range(10):
            error = 0
            start = time.time()
            try:
                request = urllib.request.Request(address, headers=self.headers)
                response = urlopen(request)
            except:
                error = 1
            if error == 0:
                average = average + (time.time() - start)
                all += 1
            if all == 0:
                return False
        return average / all

    def get_best(self):
        """Get list best servers"""
        try:
            url = "http://speedtest.net/speedtest-servers.php"
            request = urllib.request.Request(url, headers=self.headers)
            response = urlopen(request)
            servers_xml = etree.fromstring(self.zip_response(response))
            servers = servers_xml.find("servers").findall("server")
            server_list = []
        except Exception as e:
            url = "http://c.speedtest.net/speedtest-servers-static.php"
            request = urllib.request.Request(url, headers=self.headers)
            response = urlopen(request)
            servers_xml = etree.fromstring(self.zip_response(response))
            servers = servers_xml.find("servers").findall("server")
            server_list = []
        for server in servers:
            server_list.append({
                'lat': float(server.attrib['lat']),
                'lon': float(server.attrib['lon']),
                'url': server.attrib['url'].rsplit('/', 1)[0] + '/',
                'name': server.attrib['name'],
                'country': server.attrib['country'],
                'id': server.attrib['id'],
            })
        config = self.get_config()
        for server in server_list:
            server['distance'] = self.distance(config['lon'], config['lat'], server['lon'], server['lat'])
        server_list_sorted = sorted(server_list, key=lambda k: k['distance'])
        best_servers = self.get_servers(server_list_sorted[:5])
        best_servers = sorted(best_servers, key=lambda k: k['latency'])
        return best_servers

    def download(self):
        """Download speed test"""
        all_speed = []
        best_server = self.get_best()
        for i in range(0, len(self.DOWNLOAD_FILES)):
            url = "random" + self.DOWNLOAD_FILES[i] + ".jpg?x=" + str(time.time())
            all_url = best_server[i]['url'] + url
            # measuring connection duration
            duration = os.popen('curl -m 60 -w "%{speed_download}" -O ' + all_url).read()
            speed = str(str(round((float(duration.split(',')[0]) / 1024 / 1024) * 1.048576 * 8, 2)))
            all_speed.append(speed + "MB/s")
            try:
                os.remove(url)
            except BaseException:
                pass
        url = "random" + self.DOWNLOAD_FILES[-1] + ".jpg"
        all_url = best_server[0]['url'] + url
        if os.path.isfile(url):
            pass
        else:
            duration = os.popen('curl -m 90 -w "%{speed_download}" -O ' + all_url).read()
            speed = str(str(round((float(duration.split(',')[0]) / 1024 / 1024) * 1.048576 * 8, 2)))
            all_speed.append(speed+ "MB/s")
        return max(all_speed)

    def upload(self):
        """Upload speed test"""
        uploads_speed = []
        url = "upload.php"
        all_url = self.get_best()[0]['url'] + url
        files = [filename for filename in os.listdir('.') if filename.startswith("random3")]
        filename = files[0]
        for i in range(0, len(self.DOWNLOAD_FILES)):
            all_url = self.get_best()[i]['url'] + url
            duration_echo = str(
                'echo "scale=2; `curl -m 30 -w "%{speed_upload}" --data-binary @' + filename + ' ' + all_url + '`"')
            duration = os.popen(duration_echo).read()
            if 'unavailable.' in str(duration):
                continue
            if 'Too Large' in str(duration):
                print('Bad server')
            else:
                if 'size=500' in str(duration):
                    speed = str(str(round(
                        (float(duration.strip().split('size=500')[-1].split(',')[0]) / 1024 / 1024) * 1.048576 * 8,
                        2))) + "MB/s"
                    uploads_speed.append(speed)
                elif 'size=' not in str(duration):
                    speed = str(str(
                        round((float(duration.strip().split(' ')[1].split(',')[0]) / 1024 / 1024) * 1.048576 * 8,
                              2))) + "MB/s"
                    uploads_speed.append(speed)
                elif 'size=' in str(duration):
                    speed = str(str(
                        round((int(duration.strip().split('size=')[-1].split(',')[0][9:]) / 1024 / 1024) * 1.048576 * 8,
                              2))) + "MB/s"
                    uploads_speed.append(speed)
        return max(uploads_speed)


def cli() -> None:
    s = SpeedTestObject()
    print(s.download())


if __name__ == "__main__":
    cli()
