#!/usr/bin/python
# ^_^ coding: utf-8 ^_^
import os


def list_files(dir='/data/reboot/',ext=''):
	path_list = []
	if os.path.exists(dir):
		names = os.listdir(dir)
		for name in names:
			path = os.path.join(dir,name)
			if os.path.isdir(path):
				path_list.extend(list_files(path,ext))
			else:
				if not ext or path.endswith(ext):
					path_list.append(path)
	return path_list

if __name__ == '__main__':
	#print list_files('F:\code\cmdb\cmdb')
	list_file = []
	fuhe_file_drop= []
	fuhe_file_truncate = []
	fuhe_file_delete = []
	for  i in ['.py','.sql']:
	    list_file.extend(list_files('F:\liyan',i))

	for  file_match in  list_file:
		file_matchs = open(file_match,'rb')
		s = file_matchs.readlines()
		file_matchs.close()
		for   j in s:
			if 'drop' in j:
				fuhe_file_drop.append(file_match)
			if 'truncate' in j:
				fuhe_file_truncate.append(file_match)
			if 'delete' in j:
				fuhe_file_delete.append(file_match)
				
print 'delete:',fuhe_file_delete
print 'truncate:',fuhe_file_truncate
print 'drop:',fuhe_file_drop



