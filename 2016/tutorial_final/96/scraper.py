import requests, time, json
from bs4 import BeautifulSoup
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

def retrieve_html(url):
    """
    Return the raw HTML at the specified URL.

    Args:
        url (string): 

    Returns:
        status_code (integer):
        raw_html (string): the raw HTML content of the response, properly encoded according to the HTTP headers.
    """
    res = requests.get(url)
    return res.status_code, res.text

def authenticate(config_filepath):
    """
    Create an authenticated yelp-python client.

    Args:
        config_filepath (string): relative path (from this file) to a file with your Yelp credentials

    Returns:
        client (yelp.client.Client): authenticated instance of a yelp.Client
    """
    with open(config_filepath) as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        return Client(auth)

def yelp_search(client, query):
    """
    Make an authenticated request to the Yelp API.

    Args:
        query (string): Search term

    Returns:
        total (integer): total number of businesses on Yelp corresponding to the query
        businesses (list): list of yelp.obj.business.Business objects
    """
    res = client.search(query)
    return res.total, res.businesses

def all_restaurants(client, query):
    """
    Retrieve ALL the restaurants on Yelp for a given query.

    Args:
        query (string): Search term

    Returns:
        results (list): list of yelp.obj.business.Business objects
    """
    results = []
    offset = 0
    
    while True:
        res = client.search(query, **{
            'category_filter': 'restaurants',
            'limit': 20,
            'offset': offset
        })

        total = res.total

        if len(results) >= total:
            break

        new_records = res.businesses
        results += new_records
        offset += len(new_records)

        # yelp api restricts requests to 1000 results
        if offset >= 1000:
            break

        time.sleep(0.2)

    return results


def parse_api_response(data):
    """
    Parse Yelp API results to extract restaurant URLs.
    
    Args:
        data (string): String of properly formatted JSON.

    Returns:
        (list): list of URLs as strings from the input JSON.
    """
    return [ business['url'] for business in json.loads(data)['businesses'] ]

def parse_page(html):
    """
    Parse the reviews on a single page of a restaurant.
    
    Args:
        html (string): String of HTML corresponding to a Yelp restaurant

    Returns:
        tuple(list, string): a tuple of two elements
            first element: list of dictionaries corresponding to the extracted review information
            second element: URL for the next page of reviews (or None if it is the last page)
    """
    # def parse_review(review):
    #     formatted = {}

    #     formatted['review_id'] = review['data-review-id']
    #     formatted['user_id'] = review['data-signup-object'].split(':')[-1]

    #     content = review.find('div', class_='review-content')
    #     rating = content.find('div', itemprop='reviewRating') \
    #                     .find('meta', itemprop='ratingValue')
    #     formatted['rating'] = float(rating['content'])
    #     formatted['date'] = content.find('span', class_='rating-qualifier') \
    #                                .find('meta', itemprop='datePublished')['content']
    #     formatted['text'] = content.p.text

    #     return formatted

    # soup = BeautifulSoup(html, 'html.parser')
    # reviews = soup.find('ul', class_='reviews').find_all('div', itemprop='review')
    # next_link = soup.select('a.next.pagination-links_anchor')
    # structured = [ parse_review(review) for review in reviews ]
    # next_page = next_link[0]['href'] if len(next_link) > 0 else None
    # return structured, next_page

    bs = BeautifulSoup(html, "html.parser")
    reviews = bs.find_all(class_="review")
    res = []
    for review in reviews:
        review_id = review.get("data-review-id")
        if review_id is not None:
            try:
                user_id = review.get("data-signup-object").replace("user_id:", "")
                rating = review.find(class_="star-img").get("title").split(" ")[0]
                date = review.find(class_="rating-qualifier").getText()
                text = review.find("p").getText()
                
                review_data = {
                    "review_id": review_id,
                    "user_id": user_id.strip(),
                    "rating": float(rating),
                    "date": date,
                    "text": text
                }
                res.append(review_data)
            except Exception as e:
                print("got an error while parsing review: {}".format(e))
    next_page = bs.find("a", class_="next")
    if next_page is not None:
        next_page = next_page.get("href")
    
    return res, next_page

def extract_reviews(url):
    """
    Retrieve ALL of the reviews for a single restaurant on Yelp.

    Parameters:
        url (string): Yelp URL corresponding to the restaurant of interest.

    Returns:
        reviews (list): list of dictionaries containing extracted review information
    """
    reviews = []
    page = 0

    while url:
        html = requests.get(url).text
        formatted, url = parse_page(data.text)
        reviews += formatted
        
    return reviews

