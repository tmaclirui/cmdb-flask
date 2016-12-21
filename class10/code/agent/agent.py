#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
import time
import psutil
import datetime
import requests
import sys
import logging,os

URL = 'http://%s:%s/monitor/host/create/'
INTERVAL = 60

logger = logging.getLogger(__name__)

def get_addr():
	addr = '0.0.0.0'
	nics = psutil.net_if_addrs().get('eth1')
	for nic in nics:
		if nic.address.find('.') != -1:
			addr = nic.address
			break
	return addr 
def monitor(server_ip,server_port):
	url = URL % (server_ip,server_port)
	ip_addr = get_addr()
	while True:
		try:
			usage = {}
			usage['ip'] = ip_addr
			usage['disk'] = psutil.disk_usage('/').percent
			usage['cpu'] = psutil.cpu_percent()
			usage['mem'] = psutil.virtual_memory().percent
			usage['m_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			logger.debug(usage)
			response = requests.post(url,data=usage)
			if response.ok:
			    logger.debug(response.json())
			else:
			 	logger.error('server error')
		except BaseException as e:
		    logger.error(e)
		time.sleep(INTERVAL)

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print '请传入 ip地址 和 端口号'
		sys.exit(-1)
	logging.basicConfig(level=logging.DEBUG,filename='agent.log')

	pid = os.getpid()
	logger.info('PID:%s',pid)

 	with open('agent.pid','wb') as fh:
 		fh.write(str(pid))

	monitor(sys.argv[1],sys.argv[2])
