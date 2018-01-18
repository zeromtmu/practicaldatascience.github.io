
# coding: utf-8

# # Web Scraper (45 pts)

# In[1]:

# setup library imports
import io, time, json
import requests
from bs4 import BeautifulSoup

# import yelp client library
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator


# #### Library Documentation
# 
# * Standard Library: 
#     * [io](https://docs.python.org/2/library/io.html)
#     * [time](https://docs.python.org/2/library/time.html)
#     * [json](https://docs.python.org/2/library/json.html)
# 
# * Third Party
#     * [requests](http://docs.python-requests.org/en/master/)
#     * [Beautiful Soup (version 4)](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
#     * [yelp-python](https://github.com/Yelp/yelp-python)
# 
# To install `yelp-python` (not in Anaconda by default): `pip install yelp`

# ## Introduction
# 
# Welcome to the homework on web scraping. While many people might view working with data (including scraping, parsing, storing, etc.) a necessary evil to get to the "fun" stuff (i.e. modeling), I think that if presented in the right way this munging can be quite empowering. Imagine you never had to worry or ask those _what if_ questions about data existing or being accessible... but that you can get it yourself!
# 
# By the end of this exercise hopefully you should look at the wonderful world wide web without fear, comforted by the fact that anything you can see with your human eyes, a computer can see with its computer eyes...
#  
# ### Objectives
# 
# But more concretely, this homework will teach you (and test you on):
# 
# * HTTP Requests (and lifecycle)
# * ReSTful APIs
#     * Authentication (OAuth)
#     * Pagination
#     * Rate limiting
# * JSON vs. HTML (and how to parse each)
# * HTML traversal (CSS selectors)

# ## Working with APIs
# 
# Since everyone loves food (presumably), the ultimate end goal of this homework will be to acquire the data to answer some questions and hypotheses about the restaurant scene in Pittsburgh (which we will get to later). We will download __both__ the metadata on restaurants in Pittsburgh from the Yelp API and with this metadata, retrieve the comments/reviews and ratings from users on restaurants.
# 
# But first things first, let's do the "hello world" of making web requests with Python to get a sense for how to programmatically access web pages: an (unauthenticated) HTTP GET to download a web page.

# ---

# ## Q0: Basic HTTP Requests (2 pts)
# 
# Fill in the funtion to use `requests` to download and return the raw HTML content of the URL passed in as an argument. As an example try the following NYT article (on Facebook's algorithmic news feed): [http://www.nytimes.com/2016/08/28/magazine/inside-facebooks-totally-insane-unintentionally-gigantic-hyperpartisan-political-media-machine.html](http://www.nytimes.com/2016/08/28/magazine/inside-facebooks-totally-insane-unintentionally-gigantic-hyperpartisan-political-media-machine.html)
# 
# > Your function should return a tuple of: (`<status_code>`, `<raw_html>`)
# 
# ```python
# >>> facebook_article = retrieve_html('http://www.nytimes.com/2016/08/28/magazine/inside-facebooks-totally-insane-unintentionally-gigantic-hyperpartisan-political-media-machine.html')
# >>> print(facebook_article)
# (200, u'<!DOCTYPE html>\n<!--[if (gt IE 9)|!(IE)]> <!--> <html lang="en" class="no-js section-magazine...')
# ```
# 

# In[2]:

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
    return (r.status_code, r.text)
    pass

#facebook_article = retrieve_html('http://www.nytimes.com/2016/08/28/magazine/inside-facebooks-totally-insane-unintentionally-gigantic-hyperpartisan-political-media-machine.html')
#print(facebook_article)


# ---

# Now while this example might have been fun, we haven't yet done anything more than we could with a web browser. To really see the power of programmatically making web requests we will need to interact with a API. For the rest of this homework we will be working with the [Yelp API](https://www.yelp.com/developers/documentation/v2/overview) and Yelp data (for an extensive data dump see their [Academic Dataset Challenge](https://www.yelp.com/dataset_challenge)). The reasons for using the Yelp API are 3 fold:
# 
# 1. Incredibly rich dataset that combines:
#     * entity data (users and businesses)
#     * preferences (i.e. ratings)
#     * geographic data (business location and check-ins)
#     * temporal data
#     * text in the form of reviews
#     * and even images.
# 2. Well [documented API](https://www.yelp.com/developers/documentation/v2/overview) with thorough examples and a [web console](https://www.yelp.com/developers/api_console) for quick exploration.
# 3. Extensive data coverage so that you can find data that you know personally (from your home town/city or account). This will help with understanding and interpreting your results.

# ## Authentication
# 
# To access the Yelp API however we will need to go through a few more steps than we did with the first NYT example. Most large web scale companies use a combination of authentication and rate limiting to control access to their data to ensure that everyone using it abides. The first step (even before we make any request) is to setup a Yelp account if you do not have one and get API credentials.

# ## Yelp API Access
# 
# 1. Create a Yelp account (if you do not have one already)
# 2. [Generate API keys](https://www.yelp.com/developers/manage_api_keys) (if you haven't already).
# 

# Now that we have our accounts setup we can start making requests! There are various authentication schemes that APIs use, listed here in relative order of complexity:
# 
# * No authentication
# * [HTTP basic authentication](https://en.wikipedia.org/wiki/Basic_access_authentication)
# * Cookie based user login
# * OAuth (v1.0 & v2.0, see this [post](http://stackoverflow.com/questions/4113934/how-is-oauth-2-different-from-oauth-1) explaining the differences)
# * Custom Authentication
# 
# For the NYT example, since it is a publicly visible page we did not need to authenticate. HTTP basic authentication isn't too common for consumer sites/applications that have the concept of user accounts (like Facebook, LinkedIn, Twitter, etc.) but is simple to setup quickly and you often encounter it on with individual password protected pages/sites. I'm sure you have seen this before somewhere:
# 
# ![http-basic](http://i.stack.imgur.com/QnUZW.png)
# 
# Cookie based user login is what the majority of services use when you login with a browser (i.e. username and password). Once you sign in to a service like Facebook, the response stores a cookie in your browser to remember that you have logged in (HTTP is stateless). Each subsequent request to the same domain (i.e. any page on `facebook.com`) also sends the cookie that contains the authentication information to remind Facebook's servers that you have already logged in.
# 
# Many ReST APIs however use OAuth (authentication using tokens) -- either OAuth 1.0 or OAuth 2.0 (Yelp uses 1.0) -- which can be thought of a programmatic way to "login" _another_ user. Using tokens, a user (or application) only needs to send the login credentials once in the initial authentication and as a response from the server gets a special signed token. This signed token is then sent in future requests to the server (in place of the user credentials). From [Wikipedia](https://en.wikipedia.org/wiki/OAuth):
# 
# >  OAuth provides to clients a "secure delegated access" to server resources on behalf of a resource owner
# 
# For example, an application built on top of the Yelp API has its own accounts that are distinct from Yelp's user accounts, even though one person owns both accounts. In this sense, the API can be thought of a way for a "guest" application to access Yelp user data. And now hopefully authentication with OAuth makes a little more sense.
# 
# The tradeoff of security is one of convenience and to use OAuth we need to authenticate the requests we will send by _signing_ them with our keys. But thankfully many libraries exist to make working with OAuth much more developer friendly. And many providers have their own wrapper libraries (including Yelp). Also, one of ways you can keep these keys private while still somewhat convenient to use programmatically is to store them in environment variables or an external file outside of version control (this has the nice side effect that your code can also work in a remote execution environment like the autograder).
# 

# ---

# ## Q1: Authenticated HTTP Request with the Yelp API (3 pts)
# 
# > First, store your Yelp credentials in a local file (kept out of version control) which you can read in to authenticate with the API. This file can be any format/structure since you will fill in the function stub below but the documentation for `yelp-python` has a good example of how to do this. The reason for this is 
# 
# **KEEP THIS FILE PRIVATE AND OUT OF VERSION CONTROL**

# Using the [yelp-python](https://github.com/Yelp/yelp-python) client, fill in the following function stubs to:
# 
# 1. [Authenticate](https://github.com/Yelp/yelp-python#basics) with your keys
# 2. Make an authenticated request to the [search](https://github.com/Yelp/yelp-python#search-api) endpoint. 
# 
# You should create an authenticated client outside of the `yelp_search()` function using the `authenticate()` function you fill in and pass it as an argument.
# 
# > As a test, search for businesses in Pittsburgh. You should find ~6600 total depending on when you search (but this will actually differ from the number of actual Business objects returned... more on this in the next section)
# 
# ```python
# >>> num_records, data = yelp_search('Pittsburgh')
# >>> print num_records
# 6634
# >>> print data
# [<yelp.obj.business.Business at 0x10443a978>,
#  <yelp.obj.business.Business at 0x10443a9b0>,
#  <yelp.obj.business.Business at 0x10443aa20>,
#  <yelp.obj.business.Business at 0x10443aac8>,
# ...
# ]
# ```

# In[3]:

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
        return Client(auth)
    pass


# In[4]:

#client = authenticate('config_secret.json')

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
    result = client.search(query)
    return result.total, result.businesses
    pass

#num_records, data = yelp_search(client, 'Pittsburgh')
#print num_records
#print data


# ---

# Now that we have completed the "hello world" of working with the Yelp API, we are ready to really fly! The rest of the exercise will have a bit less direction since there are a variety of ways to retrieve the requested information but you should have all the component knowledge at this point to work with the API. Yelp being a fairly general platform actually has many more business than just restaurants, but by using the flexibility of the API we can ask it to only return the restaurants.

# ## Parameterization and Pagination
# 
# And before we can get any reviews on restaurants, we need to actually get the metadata on ALL of the restaurants in Pittsburgh. Notice above that while Yelp told us that there are ~6600, the response contained far fewer actual `Business` objects. This is due to pagination and is a safeguard against returning __TOO__ much data in a single request (what would happen if there were 100,000 restaurants?) and can be used in conjuction with _rate limiting_ as well as a way to throttle and protect access to Yelp data.
# 
# > If an API has 1,000,000 records, but only returns 10 records per page and limits you to 5 requests per second... how long will it take to acquire ALL of the records contained in the API?
# 
# One of the ways that APIs are an improvement over plain web scraping is the ability to make __parameterized__ requests. Just like the Python functions you have been writing have arguments (or parameters) that allow you to customize its behavior/actions (an output) without having to rewrite the function entirely, we can parameterize the queries we make to the Yelp API to filter the results it returns.

# ---

# ## Q2: Aquire all of the restaurants in Pittsburgh (on Yelp) (15 pts)
# 
# Using the [API documentation](https://www.yelp.com/developers/documentation/v2/search_api) for the `search` endpoint, fill in the following function to retrieve all of the _Restuarants_ (using categories) for a given query. Again you should use your `authenticate()` function outside of the `all_restaurants()` stub to create a client to use for the requests. You will need to account for __pagination__ and __[rate limiting](https://www.yelp.com/developers/faq)__ to:
# 
# 1. Retrieve all of the Business objects (# of business objects should equal `total` in the response)
# 2. Pause slightly (at least 200 milliseconds) between subsequent requests so as to not overwhelm the API (and get blocked).  
# 
# As always with API access, make sure you follow all of the [API's policies](https://www.yelp.com/developers/api_terms) and use the API responsibly and respectfully.
# 
# ** DO NOT MAKE TOO MANY REQUESTS TOO QUICKLY OR YOUR KEY MAY BE BLOCKED **
# 
# > Again, you can test your function with an individual neighborhod in Pittsburgh (I recommend Polish Hill). Pittsburgh itself has a lot of restaurants... meaning it will take a lot of time to download them all.

# ```python
# >>> data = all_restaurants(client, 'Polish Hill, Pittsburgh')
# >>> print len(data)
# 289
# >>> print data
# [<yelp.obj.business.Business at 0x10443a978>,
#  <yelp.obj.business.Business at 0x10443a9b0>,
#  <yelp.obj.business.Business at 0x10443aa20>,
#  <yelp.obj.business.Business at 0x10443aac8>,
# ...
# ]
# ```

# In[6]:

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
        'term': 'Restaurants',
        'offset': 0
    }
    
    response = client.search(query, **params)
    count = response.total
    print(response.total)
    businesses = response.businesses
    count -= len(businesses)
    
    while(count > 0):
        time.sleep(.200)
        params['offset'] += len(response.businesses)
        response = client.search(query, **params)
        businesses += response.businesses
        count -= len(response.businesses)
        
    return businesses
    pass

# data = all_restaurants(client, 'Polish Hill, Pittsburgh')
# print len(data)
# print data


# ---

# Now that we have the metadata on all of the restaurants in Pittsburgh (or at least the ones listed on Yelp), we can retrieve the reviews and ratings. The Yelp API gives us aggregate information on ratings but it doesn't give us the review text or individual users' ratings for a restaurant. For that we need to turn to web scraping, but to find out what pages to scrape we first need to parse our JSON from the API to extract the URLs of the restaurants.
# 
# While we already have the results as Business objects (since we are using the Yelp client), this is not a general solution and many APIs don't have a nice wrapper library in your language of choice. Also, it is a best practice to seperate the act of __downloading__ data and __parsing__ data. This ensures that your data processing pipeline is modular and extensible (and autogradable ;). This decoupling also solves the problem of expensive downloading but cheap parsing (in terms of computaion and time).

# ---

# ## Q 2.5: Parse the API Responses and Extract the URLs (3 pts)
# 
# Because we want to seperate the __downloading__ from the __parsing__, fill in the following function to parse the URLs pointing to the restaurants on `yelp.com`. As input your function should expect a string of [properly formatted JSON](http://www.json.org/) (which is similar to __BUT__ not the same as a Python dictionary) and as output should return a Python list of strings. The input JSON will be structured as follows (same as the [sample](https://www.yelp.com/developers/documentation/v2/search_api#sampleResponse) on the Yelp API page):
# 
# ```json
# {
#     "businesses": [
#         {
#             "categories": [
#                 [
#                     "Local Flavor",
#                     "localflavor"
#                 ],
#                 [
#                     "Mass Media",
#                     "massmedia"
#                 ]
#             ],
#             "display_phone": "+1-415-908-3801",
#             "id": "yelp-san-francisco",
#             "image_url": "http://s3-media3.fl.yelpcdn.com/bphoto/nQK-6_vZMt5n88zsAS94ew/ms.jpg",
#             "is_claimed": true,
#             "is_closed": false,
#             "location": {
#                 "address": [
#                     "140 New Montgomery St"
#                 ],
#                 "city": "San Francisco",
#                 "coordinate": {
#                     "latitude": 37.7867703362929,
#                     "longitude": -122.399958372115
#                 },
#                 "country_code": "US",
#                 "cross_streets": "Natoma St & Minna St",
#                 "display_address": [
#                     "140 New Montgomery St",
#                     "Financial District",
#                     "San Francisco, CA 94105"
#                 ],
#                 "geo_accuracy": 9.5,
#                 "neighborhoods": [
#                     "Financial District",
#                     "SoMa"
#                 ],
#                 "postal_code": "94105",
#                 "state_code": "CA"
#             },
#             "mobile_url": "http://m.yelp.com/biz/yelp-san-francisco",
#             "name": "Yelp",
#             "phone": "4159083801",
#             "rating": 2.5,
#             "rating_img_url": "http://s3-media4.fl.yelpcdn.com/assets/2/www/img/c7fb9aff59f9/ico/stars/v1/stars_2_half.png",
#             "rating_img_url_large": "http://s3-media2.fl.yelpcdn.com/assets/2/www/img/d63e3add9901/ico/stars/v1/stars_large_2_half.png",
#             "rating_img_url_small": "http://s3-media4.fl.yelpcdn.com/assets/2/www/img/8e8633e5f8f0/ico/stars/v1/stars_small_2_half.png",
#             "review_count": 7140,
#             "snippet_image_url": "http://s3-media4.fl.yelpcdn.com/photo/YcjPScwVxF05kj6zt10Fxw/ms.jpg",
#             "snippet_text": "What would I do without Yelp?\n\nI wouldn't be HALF the foodie I've become it weren't for this business.    \n\nYelp makes it virtually effortless to discover new...",
#             "url": "http://www.yelp.com/biz/yelp-san-francisco"
#         }
#     ],
#     "total": 2316
# }
# ```

# In[7]:

def parse_api_response(data):
    """
    Parse Yelp API results to extract restaurant URLs.
    
    Args:
        data (string): String of properly formatted JSON.

    Returns:
        (list): list of URLs as strings from the input JSON.
    """
    
    # Write solution here
    url = []
    result = json.loads(data)
    for business in result['businesses']:
        url.append(business['url'])
    return url
    pass


# ---

# As we can see, JSON is quite trivial to parse (which is not the case with HTML as we will see in a second) and work with programmatically. This is why it is one of the most ubiquitous data serialization formats (especially for ReSTful APIs) and a huge benefit of working with a well defined API if one exists. But APIs do not always exists or provide the data we might need, and as a last resort we can always scrape web pages...

# ## Working with Web Pages (and HTML)
# 
# I like to think of APIs as similar to accessing a application's database itself (something you can interactively query and receive structured data back). But the results are usually in a somewhat raw form with no formatting or visual representation (like the results fro ma database query). This is a benefit _AND_ a drawback depending on the end use case. For data science and _programatic_ analysis this raw form is quite ideal, but for an end user requesting information from a _graphical interface_ (like a web browser) this is very far from ideal since it takes some cognitive overhead to interpret the raw information. And vice versa, if we have HTML it is quite easy for a human to visually interpret it, but to try to perform some type of programmatic analysis we first need to parse the HTML into a more structured form.
# 
# > As a general rule of thumb, if the data you need can be accessed or retrieved in a structured form (either from a bulk download or API) prefer that first. But if the data you want (and need) is not as in our case we need to resort to alternative (messier) means.
# 
# Going back to the "hello world" example of question 1 with the NYT, we will do something similar to retrieve the HTML of the Yelp site itself (rather than going through the API) programmatically as text. 

# ---

# ## Q3: Parse a Yelp restaurant Page (15 pts)
# 
# Using `BeautifulSoup`, parse the HTML of a single Yelp restaurant page to extract the reviews in a structured form as well as the URL to the next page of reviews (or `None` if it is the last page). Fill in following function stubs to parse a single page of reviews and return:
# * the reviews as a structured Python dictionary
# * the HTML element containing the link/url for the next page of reviews (or None).
# 
# For each review be sure to structure your Python dictionary as follows (to be graded correctly). The order of the keys doesn't matter, only the keys and the data type of the values:
# 
# ```python
# {
#     'review_id': str
#     'user_id': str
#     'rating': float
#     'date': str ('yyyy-mm-dd')
#     'text': str
# }
# 
# # Example
# {
#     'review_id': '12345'
#     'user_id': '6789'
#     'rating': 4.7
#     'date': '2016-01-23'
#     'text': "Wonderful!"
# }
# ```
# 
# > There can be issues with Beautiful Soup using various parsers, for maximum conpatibility (and fewest errors) initialize the library with the default (and Python standard library parser): `BeautifulSoup(markup, "html.parser")`

# In[9]:

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
    review_dict = []
    
    soup = BeautifulSoup(html, 'html.parser')
    reviews = soup.select('div.review-list > ul > li > div[itemprop="review"]')
    
    
    for review in reviews:
        review_id = review['data-review-id']
        user_id = review['data-signup-object'][8:]
        rating = float(review.select('meta[itemprop="ratingValue"]')[0]['content'])
        date = review.select('meta[itemprop="datePublished"]')[0]['content']
        text = review.select('p[itemprop="description"]')[0].text
        review_dict.append(
            {'review_id': review_id, 
             'user_id': user_id, 
             'rating': rating, 
             'date': date, 
             'text': text
            })
    
    next_button = soup.select('div.review-pager a.next.pagination-links_anchor')
    next_url = ""
    if len(next_button) > 0:
        next_url = next_button[0]['href']
    else:
        next_url = None
    
    return (review_dict, next_url)
    pass

# data = parse_page(retrieve_html('https://www.yelp.com/biz/spirit-lodge-pittsburgh-2')[1])
# print(len(data[0]))
# print(data)


# ---

# ## Q 3.5: Extract all of the Yelp reviews for a Single Restaurant (7 pts)
# 
# So now that we have parsed a single page, and figured out a method to go from one page to the next we are ready to combine these two techniques and actually crawl through web pages! 
# 
# Using `requests`, programmatically retrieve __ALL__ of the reviews for a __single__ restaurant (provided as a parameter). Just like the API was paginated, the HTML paginates its reviews (it would be a very long web page to show 300 reviews on a single page) and to get all the reviews you will need to parse and traverse the HTML. As input your function will receive a URL corresponding to a Yelp restaurant. As output return a list of dictionaries (structured the same as question 3) containing the relevant information from the reviews.
# 
# ```python
# >>> data = extract_reviews('https://www.yelp.com/biz/the-porch-at-schenley-pittsburgh')
# >>> print len(data)
# 385
# >>> print data[0]
# [{'date': u'2016-08-17',
#   'rating': 4.0,
#   'review_id': u'hI0KV-CzZo4TEtPkDv4ncQ',
#   'text': u'So let me say that I have driven past many many times, longing to enter. \xa0I\'ve made excuses like... "Do I really want to deal with street parking today?" \xa0etc. \xa0Well, I finally had the opportunity and went. \xa0It is kind of cute. \xa0You enter, order/ pay at the register and then pick a table and claim it with the numbered sign you were given. \xa0To start I was in the group setting many of whom had just met me. \xa0Let me just say this is a mini celiac nightmare (at least for me), mostly because you have probably gotten roped into going somewhere that you know nothing about. \xa0Well, I got lucky this time. \xa0I asked the individual behind the register and he informed me that most of the salads were fine and he seemed knowledgeable. \xa0I ordered a chopped salad sans dressing just in case. \xa0It was wonderful with moist, flavorful pulled chicken. \xa0It was a nice light lunch with no contamination issues. \xa0The waiters were friendly and made a point of loudly announcing my "gluten free allergy" chopped salad\'s arrival.As I surveyed my colleagues meals I have to say that everyone finished their plate and stopped short of licking the plate clean. \xa0Also the tiramisu appeared rather enjoyable.The only mini negatives.... well at lunch time it can get pretty tight and the waiters often have to skirt the edges of the tables to get to other tables with orders. \xa0I was mildly concerned for a second that i was going to have someones dish raining down upon me at some point. \xa0However, the waiter appeared accustomed to this and his balance was on point. \xa0Overall nice experience and I didn\'t get sick. \xa0No complaints. \xa0I\'d be tempted to go again, maybe next time in a smaller group so I could spend more time asking about the menu to see if options other than salad exist.',
#   'user_id': u'O__X_Mr0pHGcG7l1zK7h2g'},
#  {'date': u'2016-08-13',
#   'rating': 4.0,
#   'review_id': u'UV56dSWzNDgydyehWGapEg',
#   'text': u"I finally ate here...This is a really nice upscale restaurant near the college campuses, most of the other restaurants consist of fast food.It's very clean and modern with a wrap around outside porch to eat in... and lots of Pokestops.The menu changes seasonally and they have daily food specials.I ordered the corn fritter wraps. It was homemade corn fritter patties, with lettuce that you hand wrap and a spicy sauce that had a meaty taste with a kick. The flavors were not what I \xa0expected but it was interesting. \xa0It tasted like spicy sausage.I also tried their spring chicken pizza which was descent, had good dough and you can add your own spices. I would have liked more chicken and toppings. It also tasted meaty and earthy, would have liked more garlicky flavor.This was a good place to eat, I'd like to stop back again. I would like to see stronger flavors.",
#   'user_id': u'HgeE8guC565OELCyWLmY6w'},
#   ...
# ]
# ```

# In[10]:

def extract_reviews(url):
    """
    Retrieve ALL of the reviews for a single restaurant on Yelp.

    Parameters:
        url (string): Yelp URL corresponding to the restaurant of interest.

    Returns:
        reviews (list): list of dictionaries containing extracted review information
    """
    
    # Write solution here
    all_reviews = []
    (reviews, next_url) = parse_page(retrieve_html(url)[1])
    all_reviews += reviews
    
    while next_url != None:
        (reviews, next_url) = parse_page(retrieve_html(next_url)[1])
        all_reviews += reviews
    return all_reviews
    pass


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



