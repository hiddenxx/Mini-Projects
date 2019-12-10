import logging

from fake_useragent import UserAgent
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib3
from os import system as term
from time import sleep
from datetime import date
from tinydb import TinyDB, Query, where
import random
import threading

def logs_local():
    logger = logging.getLogger('__name__')
    c_handler = logging.StreamHandler()
    t = date.today()
    f_handler = logging.FileHandler(f"Logs/{t}.log",mode='a')
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.INFO)
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    logger.setLevel(logging.ERROR)
    return logger

logger = logs_local()
db = TinyDB('proxy_db.json')
ua = UserAgent()
urls = ['http://hiddenx.online']
timeout = 5
#,
class checker(object):
    def __init__(self):
        try:
            self.user_agent = ua.random
            self.url = random.choice(urls)
            self.proxy_ip , self.proxy_port = "",""
            self.alive_dead = 0
            self.response_code = 0
        except Exception as e:
            print(e)


    def generate_random_ip(self):
        ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        return ip

    def check(self):
        self.proxy_ip , self.proxy_port = self.assign_ip()
        with requests.Session() as r :
            r.headers = {'User-Agent': self.user_agent,'X-Forwarded-For':self.generate_random_ip(),'X-Forwarded-For':self.proxy_ip}
            proxies = {"http":self.proxy_ip+":"+self.proxy_port.strip('\n'), "https":self.proxy_ip+":"+self.proxy_port.strip('\n')}
            # retry = Retry(connect=2, backoff_factor=0.5)
            # adapter = HTTPAdapter(max_retries=retry)
            # r.mount('http://', adapter)
            # r.mount('https://', adapter)


            try:
                response = r.get(self.url,proxies=proxies,timeout=(timeout,27))
                sleep(0.5)
                self.response_code = int(response.status_code)
                logger.info(f'Checked IP : {self.proxy_ip} , Response : {response}')

                return response
            except requests.ConnectionError as e:
                logger.error(str(e.args[0].reason))
            except requests.Timeout as e:
                logger.error("Timeout Error")
            except requests.RequestException as e:
                logger.error("General Error")
            except KeyboardInterrupt:
                logger.error(str(e.args[0].reason))
                # logger.error("Someone closed the program")

    def assign_ip(self):
        # Proxy = Query()
        ip_port_table = db.table('ip_port')
        result1 = [e.eid for e in ip_port_table.all()]
        length_db = len(result1)
        random_index = random.randint(0,length_db)
        result2 = ip_port_table.get(eid=random_index)
        print(result2)
        logger.info(f'Assigned Proxy : {result2}')
        return result2['ip'],result2['port']

    def update_ip(self):
        proxy_file = open('proxy.txt')
        proxy_file = list(proxy_file)
        ip_port_table = db.table('ip_port')
        for item in proxy_file:
            ip,port = item.split(':')
            ip_port_table.insert({'ip':ip.rstrip(),'port':port.rstrip(),'alive_dead':'0'})


    def print_all(self):
        print(f"Proxy IP : {self.proxy_ip} \n Proxy Port : {self.proxy_port} \n User-Agent : {self.user_agent} \n "
        + f"Url : {self.url}")

    def alive_dead_process(self,temp_table):
            result = temp_table.get(where('ip') == self.proxy_ip)
            if self.response_code == 200:
                self.alive_dead = int(result['alive_dead']) + 1
                print(table_name,self.alive_dead,int(result['alive_dead']))
            else:
                self.alive_dead = result['alive_dead'] - 1
                print(table_name,self.alive_dead,int(result['alive_dead']))

    def insert_into_table(self,response,table_name):
        temp_table = db.table(table_name)
        if response is None:
            self.response_code = -1
        else :
            self.response_code = response.status_code

        if temp_table:
            alive_dead_process(temp_table)

        if temp_table.contains(where('ip') == self.proxy_ip):
            temp_table.update({'ip':self.proxy_ip,'port':self.proxy_port,'response_code':self.response_code,'alive_dead':self.alive_dead},
            where('ip') == self.proxy_ip)
        else:
            temp_table.insert({'ip':self.proxy_ip,'port':self.proxy_port,'response_code':self.response_code,'alive_dead':self.alive_dead})

        logger.info(f'Processed {table_name.split("_")[0]} Proxy: Proxy IP : {self.proxy_ip} \n Proxy Port : {self.proxy_port}')

    def run(self):
        while True:
            response = self.check()
            if response:
                self.insert_into_table(response,"good_proxy")
            else:
                self.insert_into_table(response,"bad_proxy")

if __name__ == '__main__':

    # Uncomment for Updating the IP's
    # check = checker()
    # check.update_ip()

    # Main Application run
    try:
        check = checker()
        check.run()
        del check
        c = raw_input("Type to Exit")
    except Exception as e:
        pass
