import rauth

def get_search_params(lat, long);
	params = {}
	params["term"] = "restaurant"
	params["ll"] = "{}, {}".format(str(lat), str(long))
	params["radius_filter"] = "2000"
	params["limit"] = "10"

	return params

def get_results(params):
	consumer_key = "MVOMdRmFhEvQPa_ApLujOA"
	consumer_secret = "hWt7uMeAmeYuN8IudUzrSTPFvEV0VF2lXoNE831XYGVbH63jWgaqWlc6AucTgA2l"


# GOALS:
# send POST request to access token
# play around with output of Yelp API
# plot data for San Francisco on static chart
