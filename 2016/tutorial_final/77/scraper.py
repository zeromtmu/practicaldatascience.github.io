
# coding: utf-8

# # Web Scraper (45 pts)

# In[2]:

# setup library imports
import io, time, json
import requests
from bs4 import BeautifulSoup



def retrieve_html(url):
    """
    Return the raw HTML at the specified URL.

    Args:
        url (string): 

    Returns:
        status_code (integer):
        raw_html (string): the raw HTML content of the response, properly encoded according to the HTTP headers.
    """

    # Write solution here
    r = requests.get(url)
    return (r.status_code, r.content)
    pass



def authenticate(config_filepath):
    """
    Create an authenticated yelp-python client.

    Args:
        config_filepath (string): relative path (from this file) to a file with your Yelp credentials

    Returns:
        client (yelp.client.Client): authenticated instance of a yelp.Client
    """
    
    # Write solution here
    with io.open(config_filepath) as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        client = Client(auth)
        return client
    pass


# In[4]:

def yelp_search(client, query):
    """
    Make an authenticated request to the Yelp API.

    Args:
        query (string): Search term

    Returns:
        total (integer): total number of businesses on Yelp corresponding to the query
        businesses (list): list of yelp.obj.business.Business objects
    """
    
    # Write solution here
    resp = client.search(query)
    return resp.total, resp.businesses
    pass


def all_restaurants(client, query):
    """
    Retrieve ALL the restaurants on Yelp for a given query.

    Args:
        query (string): Search term

    Returns:
        results (list): list of yelp.obj.business.Business objects
    """
    
    # Write solution here
    params = {
    'category_filter': 'restaurants',
    'offset':0
    }
    
    resp = client.search(query, **params)
    respObj = resp.businesses
    respTotal = resp.total
    offset = len(resp.businesses)
    params['offset'] = offset
    
    while offset < respTotal:
        resp = client.search(query, **params)
        respObj = respObj + resp.businesses
        offset = offset + len(resp.businesses)
        params['offset'] = offset
        time.sleep(2)
    
    return respObj
    pass




def parse_api_response(data):
    """
    Parse Yelp API results to extract restaurant URLs.
    
    Args:
        data (string): String of properly formatted JSON.

    Returns:
        (list): list of URLs as strings from the input JSON.
    """
    
    # Write solution here
    pjson = json.loads(data)
    urls = []
    for i in pjson['businesses']:
        urls.append(str(i['url']))
    return urls
    
    pass


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
    
    # Write solution here
    reviews = []
    soup = BeautifulSoup(html, 'html.parser')
    for r in soup.find_all("div", itemprop="review"):
        rev = {}
        #rev["review_id"] = r['data-review-id']
        rev["user_id"] = r.find_next("meta", itemprop="author")['content']
        rev["rating"] = float(r.find_next("meta", itemprop="ratingValue")['content'])
        rev["date"] = r.find_next("meta", itemprop="datePublished")['content']
        rev["text"] = r.find_next("p", itemprop="description").get_text().encode('utf-8')
        reviews.append(rev)
        
    nextpage = None
    pagination = soup.find("div", {"class" : "arrange_unit page-option current"})
    if pagination != None:
        nextpage = pagination.find_next("a", {"class" : "available-number pagination-links_anchor"})
        if nextpage != None:
            nextpage = nextpage['href']
    
    return (reviews, nextpage)
    pass



def extract_reviews(url):
    """
    Retrieve ALL of the reviews for a single restaurant on Yelp.

    Parameters:
        url (string): Yelp URL corresponding to the restaurant of interest.

    Returns:
        reviews (list): list of dictionaries containing extracted review information
    """
    
    # Write solution here
    allreviews = []
    parseurl = url

    while True:
        response = retrieve_html(parseurl)
        #print response[1]
        if response[0] == 200:
            root = parse_page (response[1])
            allreviews = allreviews + root[0]
            if root[1] != None:
                parseurl = root[1]
            else:
                break
        else:
            break
            
    return allreviews
    pass



