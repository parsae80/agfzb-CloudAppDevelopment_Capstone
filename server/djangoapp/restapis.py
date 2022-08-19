import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
             # Basic authentication GET
            response = requests.get(
                url,
                params=kwargs,
                headers={'Content-Type': 'application/json'},
                auth=HTTPBasicAuth('X6P3ju5jmbYRBeQD3KyOgK2dCLJW8aMhdOPy8kD7yiPe', api_key))
        else:
            response = requests.get(
                url,
                headers={'Content-Type': 'application/json'},
                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print("Payload: ", json_payload, ". Params: ", kwargs)
    print("POST to {} ".format(url))
    try:
        response = requests.post(
            url,
            params=kwargs,
            json=json_payload)
    except: 
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results



# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["body"]["data"]
        review_docs = reviews["docs"]
        for review_doc in review_docs: 
            review_obj = DealerReview(
                dealership=review_doc["dealership"],
                name=review_doc["name"],
                purchase=review_doc["purchase"],
                review=review_doc["review"])
            if "id" in review_doc:
                review_obj.id = review_doc["id"]
            if "purchase_date" in review_doc:
                review_obj.purchase_date = review_doc["purchase_date"]
            if "car_make" in review_doc:
                review_obj.car_make = review_doc["car_make"]
            if "car_model" in review_doc:
                review_obj.car_model = review_doc["car_model"]
            if "car_year" in review_doc:
                review_obj.car_year = review_doc["car_year"]
            sentiment=analyze_review_sentiments(review_doc["review"])
            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/8ef4dad0-e720-4571-9298-731e8d652388"
    api_key = "X6P3ju5jmbYRBeQD3KyOgK2dCLJW8aMhdOPy8kD7yiPe"
 
    version = '2021-08-01'
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(
        version=version, authenticator=authenticator)
    nlu.set_service_url(url)

    # get sentiment of the review

    try:
        response = nlu.analyze(text=review_text, features=Features(
            sentiment=SentimentOptions())).get_result()
        print(json.dumps(response))
        # sentiment_score = str(response["sentiment"]["document"]["score"])
        sentiment_label = response["sentiment"]["document"]["label"]
    except:
        print("Review is too short for sentiment analysis. Assigning default sentiment value 'neutral' instead")
        sentiment_label = "neutral"

    print(sentiment_label)
    return sentiment_label

