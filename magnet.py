#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Modulos

import libtorrent as lt
import time, threading
import os
import re

PATH = "/tmp/data_m/"


def temporal():
	os.system("mkdir -p "+PATH)
	
def abrevideo():
	

	print "Abriendo video..."	
#	lectura_temp = os.popen("ls "+PATH).read() #utilizo popen porque no necesito conocer si ha finalizado correctamente y asi me ahorra el 0 o el 1
	lectura_temp = os.listdir(PATH)
	lectura_path = ''.join(lectura_temp)
	print lectura_temp 
	if re.search('.*\.mp4', ''.join(lectura_temp)) or re.search('.*\.avi', ''.join(lectura_temp)):
		os.system ('mplayer -fs -framedrop "'+PATH+''.join(lectura_temp)+'"')
		
	else:
		print "directorio superior"
		r2 = os.popen('ls '+'"'+PATH+''.join(lectura_temp)+'"').read()
		if re.search('.*\.mp4', r2) or re.search('.*\.avi', r2):
			os.system('mplayer -fs -framedrop  "'+PATH+lectura_path+"/"+re.search('.*\.mp4',r2).group()+'"')
			

	

def main():
	
	count = 0
	
	ses = lt.session()
	
	params = { 'save_path': PATH}
	
	print "Introduce el magnet :"
	link = raw_input()
	handle = lt.add_magnet_uri(ses, link, params)
	handle.set_sequential_download(True)
	salida = 0
	print 'Descargando metadatos'
	while (not handle.has_metadata()): time.sleep(1)
	print 'Cargando'
	print "0%"
	while (handle.status().state != lt.torrent_status.seeding):
		porcen_ini = handle.status().progress
		time.sleep(1)
		if handle.status().progress*100 > porcen_ini*100:
			salida = handle.status().progress*100
			print ("%.2f %%" % salida)
		if salida >= 5 and count < 1: #buffer
			hilo =  threading.Thread(target = abrevideo)
			hilo.start()
			count += 1
		
	os.system("rm -rf "+PATH)
	return 0

if __name__ == '__main__':
	main()
