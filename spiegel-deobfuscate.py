#!/usr/bin/python
# -*- coding: utf-8 -*-

# Logging purposes ...
def log(msg=None, newline=True):
	if(args.verbose):
		if(msg != None):
			if newline:
				print(msg)
			else:
				sys.stdout.write(msg)


def deobfuscate(obfuscated=None):
    if obfuscated == None:
        log('obfuscated=None')
        return ''

    debug = []
    decoded = ""

    try:
        for charObfuscated in obfuscated:
        	intObfuscated = ord(charObfuscated)

        	intDeobfuscated = intObfuscated - 1

        	# http://ascii.cl
        	if intDeobfuscated < 33:
        		debug.append(str(intDeobfuscated))
        		intDeobfuscated = intObfuscated

        	decoded += chr(intDeobfuscated)
    except:
        log('Could not deobfuscate the following string (' + str(len(obfuscated)) + ' chars)')
        log(str(obfuscated))
        decoded = ''

	#log('Chars below ASCII 33:')
    #log(', '.join(debug))

    #f = open('debug.txt', 'a')
    #f.write(decoded)
    #f.close()

    return unicode(decoded,'latin1',errors='ignore')
    #return unicode(decoded,'macroman',errors='ignore')
    #return unicode(decoded,'utf-8',errors='ignore')

import os
import sys

import time
import datetime
import string
import random
import re

import json

import requests
#import requests_cache

from BeautifulSoup import BeautifulSoup

# https://docs.python.org/2/library/argparse.html
# https://docs.python.org/2/howto/argparse.html
import argparse

parser = argparse.ArgumentParser(description='spiegel-deobfuscate')

parser.add_argument('--url', help='The web-site to be parsed', required=True)
parser.add_argument('--output', metavar='[stdout|file]', choices=['stdout','file'], help='The output format for results', action="store", required=False, default="stdout")
parser.add_argument('--verbose', help='Print debug information', action="store_true", required=False)

args = parser.parse_args()

if not args.url:
	log('args.url not set. Aborting.')
	sys.exit(1)

url = str(args.url)

if len(url) < 1:
	log('args.url empty (' + len(url) + '). Aborting.')
	sys.exit(1)

if len(url) < 7:
	log('args.url invalid (' + url + '). Aborting.')
	sys.exit(1)

log('URL is "' + url + '"')

headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36', 'Referer': url} # Delivers Flash Embed
#headers = {'User-agent': 'Mozilla/5.0', 'Referer': url} # Delivers mp4 embed
#headers = {'User-agent': 'Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.17 (KHTML, like Gecko) Version/8.0 Mobile/13A175 Safari/600.1.4'}

r = requests.get(url, headers=headers, verify=False) # http://stackoverflow.com/questions/15445981/how-do-i-disable-the-security-certificate-check-in-python-requests
body = r.content

try:
	soup = BeautifulSoup(body)
except:
	log('ERROR: Could not parse HTML body received from URL "' + url + '". Aborting')
	sys.exit(1)

# Finds all paragraphs spiegel.de marked as obfuscated
paragraphs = soup.findAll('p', { 'class' : 'obfuscated' })

try:
    count = len(paragraphs)
    log('Found ' + str(count) + ' paragraphs. Trying to decode.')
except:
    log('No paragraphs found which match p.obfuscated. Cannot continue, aborting.')
    sys.exit(1)

for paragraph in paragraphs:
    obfuscateds = paragraph.contents

    for obfuscated in obfuscateds:
        deobfuscated = deobfuscate(obfuscated.string)
        obfuscated.replaceWith(BeautifulSoup(deobfuscated))

soup.close()

html = soup.prettify("utf-8")

if args.output == 'stdout':
	print html

if args.output == 'file':
	# http://www.spiegel.de/wirtschaft/immobilien-mit-der-zauberformel-gegen-den-crash-a-1118606.html
	elements = url.rsplit('/',1)
	htmlFilename = elements[-1]

	if not htmlFilename.endswith('.html'):
		htmlFilename = htmlFilename + '.html'

	pathFile = htmlFilename

	with open(pathFile, "wb") as file:
		file.write(html)

	log('File "' + pathFile + '" written (' +  str(len(html)) + ' bytes).')

sys.exit(0)
