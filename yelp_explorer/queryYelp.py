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

# OAuth credentials
CLIENT_ID = "MVOMdRmFhEvQPa_ApLujOA"
CLIENT_SECRET = "hWt7uMeAmeYuN8IudUzrSTPFvEV0VF2lXoNE831XYGVbH63jWgaqWlc6AucTgA2l"

# API constants
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

# Defaults for our simple example.
DEFAULT_TERM = 'restaurant'
DEFAULT_LOCATION = '95148'
SEARCH_LIMIT = 50

def get_search_params(term, location):
	params = {}
	params['term'] = DEFAULT_TERM
	params['location'] = DEFAULT_LOCATION
	# params["ll"] = "{}, {}".format(str(lat), str(long))
	params["radius_filter"] = "2000"
	params["limit"] = "10"
	return params

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

def request(host, path, token, url_params=None):
	url_params = url_params or {}
	url = '{0}{1}'.format(host, quote(path.encode('utf8')))
	headers = {
	'Authorization': 'Bearer %s' % token,
	}
	print(u'Querying {0} ...'.format(url))
	response = requests.request('GET', url, headers=headers, params=url_params)
	return response.json()	

def search(token, term, location):
	url_params = {
		'term': term.replace(' ', '+'),
		'location': location.replace(' ', '+'),
		'limit': SEARCH_LIMIT
	}
	return request(API_HOST, SEARCH_PATH, token, url_params=url_params)

def get_business(token, business_id):
	business_path = BUSINESS_PATH + business_id
	return request(API_HOST, business_path, token)


def query_api(term, location):
	token = obtain_token(API_HOST, TOKEN_PATH)
	params = get_search_params(term, location)
	response = search(token, params['term'], params['location'])

	businesses = response.get('businesses')

	if not businesses:
		print(u'No businesses for {0} in {1} found.'.format(term, location))
		return

	print(u'{0} businesses found'.format(len(businesses)))

	# print(u'{0} businesses found, querying business info ' \
	# 	'for the top result "{1}" ...'.format(len(businesses), business_id))
	
	ratings = {}
	num_reviews = {}
	for i in range(0, len(businesses)):
		business_name = businesses[i]['name']
		ratings[business_name] = businesses[i]['rating']
		num_reviews[business_name] = businesses[i]['review_count']
		# print(business_name + ' has a {0} rating'.format(business_rating))
	
	return ratings, num_reviews
	# response = get_business(token, business_id)

	# print(u'Result for business "{0}" found:'.format(business_id))
	# pprint.pprint(response, indent=2)


# def main():
# 	parser = argparse.ArgumentParser()

# 	parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
# 						type=str, help='Search term (default: %(default)s)')
# 	parser.add_argument('-l', '--location', dest='location',
# 						default=DEFAULT_LOCATION, type=str,
# 						help='Search location (default: %(default)s)')

# 	input_values = parser.parse_args()

# 	try:
# 		query_api(input_values.term, input_values.location)
# 	except HTTPError as error:
# 		sys.exit(
# 			'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
# 				error.code,
# 				error.url,
# 				error.read(),
# 			)
# 		)


# if __name__ == '__main__':
# 	main()