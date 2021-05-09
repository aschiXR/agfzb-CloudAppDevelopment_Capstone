import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import os


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    try:
        api_key = None
        if 'api_key' in kwargs:
            params = {
                'text': kwargs['text'],
                'version': '2021-05-09',
                'features': 'sentiment',
                'return_analyzed_text': True
            }
            api_key = kwargs['api_key']
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=params, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs)
        status_code = response.status_code
        if status_code == 200:
            json_data = json.loads(response.text)
            return json_data
        else:
            print('Response Status Code = ', status_code)
            return None
    except Exception as e:
        print('Error occurred', e)
        return None

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, json=json_payload, params=kwargs)
        status_code = response.status_code
        if status_code == 200:
            json_data = json.loads(response.text)
            return json_data
        else:
            print('Response Status Code = ', status_code)
            return None
    except Exception as e:
        print('Error occurred', e)
        return None

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        if 'entries' in json_result:
            dealers = json_result['entries']
            results = [CarDealer(id=dealer['id'], full_name=dealer['full_name'], short_name=dealer['short_name'], city=dealer['city'], address=dealer['address'], state=dealer['state'], st=dealer['st'], zip=dealer['zip'], lat=dealer['lat'], long=dealer['long']) for dealer in dealers]
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        if 'entries' in json_result:
            reviews = json_result['entries']
            results = [DealerReview(id=review['id'], car_make=(review['car_make'] if 'car_make' in review else None), car_model=(review['car_model'] if 'car_model' in review else None), car_year=(review['car_year'] if 'car_year' in review else None), dealership=review['dealership'], name=review['name'], purchase=(review['purchase'] if 'purchase' in review else None), purchase_date=(review['purchase_date'] if 'purchase_date' in review else None), review=review['review'], sentiment=analyze_review_sentiments(review['review'])) for review in reviews]
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    kwargs = {
        'text': text,
        'api_key': os.getenv('API_KEY')
    }
    url = os.getenv('API_URL')
    result = get_request(url + '/v1/analyze', **kwargs)
    return result['sentiment']['document']['label']

def add_review_to_cf(url, json_payload):
    return post_request(url, json_payload)