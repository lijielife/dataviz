import rauth
import argparse
import json
import pprint
import requests
import sys
import urllib
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

### OAuth credentials ###
CLIENT_ID = "MVOMdRmFhEvQPa_ApLujOA"
CLIENT_SECRET = "hWt7uMeAmeYuN8IudUzrSTPFvEV0VF2lXoNE831XYGVbH63jWgaqWlc6AucTgA2l"


### API constants ###
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'
SEARCH_LIMIT = 50


### authorization ###
def obtain_token(host, path):
	url = '{0}{1}'.format(host, quote(path.encode('utf8')))
	assert CLIENT_ID, "Please supply your client_id." 
	assert CLIENT_SECRET, "Please supply your client_secret."
	data = urlencode({
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET,
		'grant_type': GRANT_TYPE,
    })
	headers = {
		'content-type': 'application/x-www-form-urlencoded',
	}
	response = requests.request('POST', url, data=data, headers=headers)
	token = response.json()['access_token']
	return token


### make POST requests ###
def request(host, path, token, url_params=None):
	url_params = url_params or {}
	url = '{0}{1}'.format(host, quote(path.encode('utf8')))
	headers = {
	'Authorization': 'Bearer %s' % token,
	}
	print(u'Querying {0} ...'.format(url))
	response = requests.request('GET', url, headers = headers, params = url_params)
	return response.json()	


### initialize search parameters ###
def set_search_params(term, location):
	params = {}
	params['term'] = term
	params['location'] = location
	params['limit'] = SEARCH_LIMIT
	params['radius_filter'] = "40000"
	return params


def search(token, params):
	params['term'] = params['term'].replace(' ', '+')
	params['location'] = params['location'].replace(' ', '+'),
	return request(API_HOST, SEARCH_PATH, token, url_params = params)


def get_business(token, business_id):
	business_path = BUSINESS_PATH + business_id
	return request(API_HOST, business_path, token)


def query_api(term, location):
	token = obtain_token(API_HOST, TOKEN_PATH)
	params = set_search_params(term, location)
	response = search(token, params)
	restaurants = response.get('businesses')

	if not restaurants: # null check
		print(u'No businesses for {0} in {1} found.'.format(term, location))
		return

	print(u'{0} businesses found'.format(len(restaurants)))	
	return restaurants