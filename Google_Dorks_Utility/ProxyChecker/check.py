import logging
logging.getLogger("proxyChecker").setLevel(logging.INFO)
from fake_useragent import UserAgent
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib3
from os import system as term
from time import sleep
from tinydb import TinyDB, Query
import random


db = TinyDB('proxy_db.json')
ua = UserAgent()
urls = ['http://hiddenx.online']

class checker(object):
    user_agent = ua.random
    url=random.choice(urls)

    def check(self):
        with requests.Session() as r :
            r.headers = {'User-Agent': self.user_agent}
            proxies = {"http":self.proxy_ip+":"+self.proxy_port.strip('\n'), "https":self.proxy_ip+":"+self.proxy_port.strip('\n')}
            # retry = Retry(connect=2, backoff_factor=0.5)
            # adapter = HTTPAdapter(max_retries=retry)
            # r.mount('http://', adapter)
            # r.mount('https://', adapter)


            try:
                response = r.get(self.url,proxies=proxies,timeout=(3.05,27))
                sleep(0.1)
                logging.info(f"Added IP : {proxies} , Response : {response}")

                return response
            except requests.ConnectionError as e:
                logging.error("Connection Error.")
                print(str(e))
            except requests.Timeout as e:
                logging.error("Timeout Error")
                print(str(e))
            except requests.RequestException as e:
                logging.error("General Error")
                print(str(e))
            except KeyboardInterrupt:
                logging.error("Someone closed the program")

    def assign_ip():
        result = db.get(Query()['ip'] & Query()['port'])
        return result['ip'],result['port']

    def update_ip():
        proxy_file = open('proxy.txt')
        proxy_file = list(proxy_file)
        for item in proxy_file:
            ip,port = item.split(':')
        db.insert({'ip':ip,'port':port})

    proxy_ip , proxy_port = assign_ip()

    def print_all(self):
        print(f"Proxy IP : {self.proxy_ip} \n Proxy Port : {self.proxy_port} \n User-Agent : {self.user_agent} \n "
        + f"Url : {self.url}")


checker = checker()
if checker.check():
    print("Good Proxy")
else:
    print("Bad Proxy")
