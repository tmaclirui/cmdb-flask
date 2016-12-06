#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
import time
import psutil
import datetime
import requests

URL = 'http://localhost:5000/monitor/host/create/'
INTERVAL = 10
def get_addr():
	addr = '0.0.0.0'
	nics = psutil.net_if_addrs().get('eth1')
	for nic in nics:
		if nic.address.find('.') != -1:
			addr = nic.address
			break
	return addr 
def monitor():
	ip_addr = get_addr()
	while True:
		usage = {}
		usage['ip'] = ip_addr
		usage['disk'] = psutil.disk_usage('/').percent
		usage['cpu'] = psutil.cpu_percent()
		usage['mem'] = psutil.virtual_memory().percent
		usage['m_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		print usage
		time.sleep(INTERVAL)

		response = requests.post(URL,data=usage)
		if response.ok:
			print response.json()
		else:
		 	print 'error'

if __name__ == '__main__':
	monitor()