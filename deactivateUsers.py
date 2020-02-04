#!/usr/bin/env python3

import requests as r
import json
import logging as l
import settings as s
payload = ''

def buildHeader():
	return{
		'Accept': "application/json",
    	'Content-Type': "application/json",
    	'Authorization': 'SSWS ' + s.APITOKEN,
    	'Host': s.HOST
		}

def deactivate_users(userId):
	url = f"https://${s.HOST}/api/v1/users/{userId}/lifecycle/deactivate"
	l.debug(url)
	headers = buildHeader()
	result = r.request("POST", url, data=payload, headers=headers)
	if result.status_code == 200:
		l.info(f"User Deactivated: {userId}")
		return True
	else:
		l.info(f"Unable to deactivate user: {userId}")
		return False
	response = json.loads(result.text)
	l.debug(f"User Deactivated: {userId} - Status: {response['status']}")
	return True

def get_suspended_users():
	url = f'https://{s.HOST}/api/v1/users?filter=status eq "SUSPENDED"'
	l.debug(url)
	headers = buildHeader()
	result = r.request("GET", url, headers=headers)
	if result.status_code != 200:
		l.error(f"Unable to retrieve users")
		return False
	response = json.loads(result.text)
	for user in response:
		deactivate_users(user['id']) 

def main():
	l.basicConfig(level=l.INFO)
	l.info('-- Start')
	get_suspended_users()
	l.info('-- End')

if __name__ == '__main__':
	main()
