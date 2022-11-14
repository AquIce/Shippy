'''
 > Code by Icy
 > CPPackager Project
 > Main file
'''

import os
import shutil
import requests
import json
import datetime


class Shippy:

	def __init__(self):
		self.shippy_content = self.get_shippy()
		self.packages = self.get_packages(self.shippy_content)
		self.path_to_src = '../' + self.get_src_folder() + '/'
		self.path_to_package = '../' + self.get_package_folder() + '/'
		self.path_to_bin = '../' + self.get_bin_folder() + '/'
		self.to_replace_back = {
		 self.path_to_src + i: {}
		 for (i) in os.listdir(self.path_to_src)
		}

	def get_shippy(self) -> dict:
		with open('../SHIPPY.json', 'r') as f:
			content = json.loads(f.read())
		return content

	def get_package_folder(self) -> str:
		return self.shippy_content['package-folder']

	def get_packages(self, content) -> dict:
		return content['packages']

	def get_package(self, name) -> str:
		self.name = name
		return self.packages[self.name]

	def get_filename(self) -> str:
		return self.name

	def get_raw_github_url(self, url: str) -> str:
		return url.replace("https://github.com",
		                   "https://raw.githubusercontent.com").replace('/blob', '')

	def download_package(self, url: str):
		pth = self.path_to_package + self.get_filename()
		if not os.path.exists(pth):
			with open(pth, 'x'):
				...
		with open(self.path_to_package + self.get_filename(), 'w') as f:
			f.write(requests.get(self.get_raw_github_url(url)).text)

	def delete_package(self, name: str):
		os.remove(self.path_to_package + name)

	def clear_packages(self):
		for i in os.listdir(self.path_to_package):
			self.delete_package(i)

	def get_src_folder(self):
		return self.shippy_content['src-folder']

	def update_packages(self):
		for i in os.listdir(self.path_to_src):
			file = self.path_to_src + i
			content = ''
			with open(file, 'r') as f:
				content = f.read()
			for j in self.packages:
				content = content.replace('#include "' + j + '"',
				                          '#include "' + self.path_to_package + j + '"')
				self.to_replace_back[file]['#include "' + self.path_to_package + j +
				                           '"'] = '#include "' + j + '"'
			with open(file, 'w') as f:
				f.write(content)

	def replace_back(self):
		for i in self.to_replace_back:
			with open(i, 'r') as f:
				content = f.read()
			for j in self.to_replace_back[i]:

				content = content.replace(j, self.to_replace_back[i][j])
			with open(i, 'w') as f:
				f.write(content)
		self.to_replace_back = {}

	def get_bin_folder(self):
		return self.shippy_content['bin-folder']

	def get_binaries_dates(self):
		return os.listdir(self.path_to_bin)

	def save_bin(self):
		os.chdir(self.path_to_bin)
		pth = datetime.datetime.now().strftime("%Y.%m.%d")
		if not os.path.exists(pth):
			os.mkdir(pth)
		os.chdir(pth)
		with open(
		  self.shippy_content['package-name'] + '_' +
		  datetime.datetime.now().strftime("%H_%M_%S.txt"), 'x') as f:
			f.write('OK')
		os.chdir('../../shippy')

	def delete_bin(self, date: str):
		os.chdir(self.path_to_bin)
		if date == '*':
			for i in os.listdir():
				shutil.rmtree(os.getcwd() + '/' + i)
		else:
			try:
				shutil.rmtree(os.getcwd() + '/' + date)
			except:
				print('Invalid package')

	def get_entry_point(self):
		return self.path_to_src + self.shippy_content['entry-point']

	def add_compiler_to_path(self):
		os.environ['PATH'] += os.pathsep + '/'.join(
		 self.shippy_content['compiler'].split('/')[:-1])


if __name__ == '__main__':
	# ''' Example Config
	shp = Shippy()
	shp.download_package(shp.get_package('memory.cpp'))
	shp.download_package(shp.get_package('memory.hpp'))
	shp.update_packages()
	shp.save_bin()
	input('...')
	shp.replace_back()
	shp.clear_packages()
	# '''