import requests
import json

#
# This file contains helper functions that make it easier to manage blue alliance function calls. 
# All calls to information in the blue alliance should use the support methods located here. This
# class contians hardcoded api keys and access tokens. This code should not be shared publicly.
#

API_URL = 'https://www.thebluealliance.com/api/v3'
AUTH_KEY = ''

previous_requests = {}
previous_responses = {}


# Returns whether the system has access to the Blue Alliance
def check_connection():
    try:
        get('/status')
        return True
    except:
        return False

# Helper method to add headers to blue alliance request, this will automatically if TBA has not
# updated the data since the last call.
def get(endpoint, force_new_request=False):
    if endpoint in previous_requests and endpoint in previous_responses and not force_new_request:
        last_modified = previous_requests[endpoint]
        header = {'X-TBA-Auth-Key':AUTH_KEY,'If-Modified-Since':last_modified}
    else:
        header = {'X-TBA-Auth-Key':AUTH_KEY}
    
    response = requests.get(API_URL+endpoint, headers=header)
    if 'Last_Modified' in response.headers:
        previous_requests[endpoint] = response.headers['Last-Modified']
    if response.status_code == 200:
        response_data = response.json()
        previous_responses[endpoint] = response_data
        return response_data, True
    elif response.status_code == 304:
        return previous_responses[endpoint], False
    else:
        print('Unable To Query Endpoint', endpoint, 'Received Response:', response.status_code)
        return None, False
