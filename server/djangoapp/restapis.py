import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    try:
        if 'cp_cl_api_key' in kwargs:
            # Cloudant service rest api request
            cp_cl_api_key = kwargs['cp_cl_api_key']
            # prepare payload
            del kwargs['cp_cl_api_key']
            # prepare header
            headers = {'Content-Type': 'application/json', 'cp_api_key': cp_cl_api_key}
            # call get method
            response = requests.get(url=url,headers=headers,params=kwargs)
        elif 'cp_wnlu_api_key' in kwargs:
            # WNLU service request
            cp_wnlu_api_key = kwargs['cp_wnlu_api_key']
            # prepare payload
            params = dict()
            params['text'] = kwargs['text']
            params['version'] = kwargs['version']
            params['features'] = kwargs['features']
            params['return_analyzed_text'] = kwargs['return_analyzed_text']
            if 'language' in kwargs:
                params['language'] = kwargs['language']
            # prepare header
            headers = {'Content-Type': 'application/json'}
            response = requests.get(url=url,headers=headers,params=kwargs,\
                    auth=HTTPBasicAuth('apikey',cp_wnlu_api_key))
        else:
            # no service key has been specified
            print("neither cp_cl_api_key nor cp_wnlu_api_key has been specified")
            return {}
    except:
        # if any error occurs print it
        print("Network exception occurred with GET request!!!")
        return {}
    status_code = response.status_code
    print("get_request: received response with status code {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data



# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        if 'cp_cl_api_key' in kwargs:
            # prepare url to send a post request
            url = url + "/post"
            # prepare headers
            headers = {'Content-Type': 'application/json', 'cp_api_key': kwargs['cp_cl_api_key']}
            # send request
            print(json_payload)
            response = requests.post(url=url, headers=headers, json=json_payload)
        else:
            # no service key has been specified
            print("no cp_cl_api_key has been specified")
            return {}
    except:
        # if any error occurs print it
        print("Network exception occurred with POST request!!!")
        return {}
    status_code = response.status_code
    print("post_request: received response with status code {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data  



# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def parse_dealers(json_data):
    car_dealers_list = []
    if not 'docs' in json_data:
        return car_dealers_list
    for dealership in json_data['docs']:
        dealer_obj = CarDealer(
           dealership['address'],
           dealership['city'],
           dealership['full_name'],
           dealership['id'],
           dealership['lat'],
           dealership['long'],
           dealership['state'],
           dealership['st'],
           dealership['zip']
        )
        car_dealers_list.append(dealer_obj)
    return car_dealers_list


def get_dealers_from_cf(url,cp_cl_api_key):
    json_data = get_request(url=url,cp_cl_api_key=cp_cl_api_key)
    return parse_dealers(json_data)

def get_dealers_by_state(url,cp_cl_api_key,state):
    json_data = get_request(url,cp_cl_api_key=cp_cl_api_key,state=state)
    return parse_dealers(json_data)

def get_dealer_by_id(url,cp_cl_api_key,dealer_id):
    json_data = get_request(url,cp_cl_api_key=cp_cl_api_key,dealer_id=dealer_id)
    dealer = parse_dealers(json_data)
    if len(dealer) != 1:
        return None
    return dealer[0]



# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def parse_dealer_reviews(json_data):
    dealer_reviews = []
    if not 'docs' in json_data:
        return dealer_reviews
    for review in json_data['docs']:
        if review['purchase']:
            review_obj = DealerReview(
                review['id'],
                review['dealership'],
                review['name'],
                review['purchase'],
                review['review'],
                review['purchase_date'],
                review['car_make'],
                review['car_model'],
                review['car_year']
            )
        else:
            review_obj = DealerReview(
                review['id'],
                review['dealership'],
                review['name'],
                review['purchase'],
                review['review']
            )
        print("analyzing review sentiments...")
        review_obj.sentiment = analyze_review_sentiments(review_obj.review)
        dealer_reviews.append(review_obj)
    return dealer_reviews


def get_dealer_reviews_from_cf(url,cp_cl_api_key,dealer_id):
    json_data = get_request(url,cp_cl_api_key=cp_cl_api_key,dealerId=dealer_id)
    return parse_dealer_reviews(json_data)



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealer_review):
    json_data = get_request(
        url=settings.WNLU_API_URL + "v1/analyze",
        cp_wnlu_api_key=settings.WNLU_API_KEY,
        version="2021-03-25",
        text=dealer_review,
        features="sentiment",
        return_analyzed_text=True,
        # language to be specified in order to deal with short reviews
        language='en'
    )
    return json_data['sentiment']['document']['label']


