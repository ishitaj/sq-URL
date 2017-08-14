# sqURL - a URL squeezer

The project has been built in python with Django and hosted on heroku servers. There are 2 ways to use the project. 



A. First way:

1. Query the webservice as an API to send a request object with Custom Header and get a response object.

2. 'http://ijain89.herokuapp.com/api' receives a POST request with JSON body containing key 'url' and value as the URL to shorten.


```
#!python
 
>>> import requests
>>> r = requests.post("http://ijain89.herokuapp.com/api", json = {'url' : 'http://www.google.com'}, headers = {'CLIENTNAME' : 'guest'})
>>> r.content
>>> b'{"squrl": "http://ijain89.herokuapp.com/cvpo", "target": "http://www.google.com", "creation_date": "2017-08-14T11:02:57.981Z", "access_date": "2017-08-14T11:04:34.255Z", "visits": 2, "message": "This target url was already shortened!"}'
```


3. 'http://ijain89.herokuapp.com/api' receives a POST request with JSON body containing key 1 'url' and value as the URL to shorten and key 2 as 'desired_squrl' and value as the preferred string or slug.


```
#!python
 
>>> import requests
>>> r = requests.post("http://ijain89.herokuapp.com/api", json = {'url' : 'https://www.python.org/', 'desired_squrl' : 'python' }, headers = {'CLIENTNAME' : 'guest'})
>>> r.content
>>> b'{"squrl": "http://ijain89.herokuapp.com/python", "target": "https://www.python.org", "creation_date": "2017-08-14T11:45:09.737Z", "access_date": "2017-08-14T11:45:09.737Z", "visits": 0, "error": "This target url is being shortened now!"}'
```


4. GET request to sqURL returns contents of the original URL and increments visits by one.


```
#!python

>>> import requests
>>> r = requests.get("http://ijain89.herokuapp.com/cvpo", headers = {'CLIENTNAME' : 'guest'})
>>> r.content
(returns HTML DOM)
```


5. Validatation on the URL to be shortened has been done using the Django's UrlField and urllib.parse method to check for existence of the URL given by visiting it. Another way to do this would have been through regex matching.


```
#!python

>>> import requests
>>> r = requests.post('http://ijain89.herokuapp.com/api', json = {'url':'abc'}, headers = {'CLIENTNAME' : 'guest'})
>>> r.content
>>> b'{"error": "The url given to shorten does not exist"}'
```


B. Second way:

1. Hit http://ijain89.herokuapp.com to reach the front end of the project.

2. You can enter the URL to be shortened into the first form field. Form validations on URLField ensure well-formed URLs.

3. Get the resulting sqURL with messages, if any.

4. http://ijain89.herokuapp.com/db gives a database view of which URLs have been stored in the database till date along with the number of times the sqURLs have been visited.

5. When you click on any code corresponding to a URL, you are redirected to the page on the original URL.

6. The visit count of the sqURL already existing in the database is incremented.

7. The app has been integrated with Google+ via OAuth2.
TODO: Linking user information with sqURL creation. 


C. URL Shortening algorithm:

Check whether the target URL has already been entered. If it has, return the same code generated earlier. Else, check whether the preferred short sqURL has already been entered. If yes, returns an error telling the user to choose another sqURL. Else, generates sqURL with user preferred string. If the target and sqURL both donot exist in the database, generate new slug using the primary key of the new sqURL in the database and converting it to base 62 (Upper case + Lower case + Digits). If length of the slug is less than four, add random characters from the same character set of upper case alphabets, lower case alphabets and digits to generate a code of given length (atleast 4 in this case). Before returning the slug, check for existence in the database to maintain uniqueness.



D. Optimization & Future improvement:

1. Asynchronous catering/Multithreading - Python uses GIL to share same set of resources among multiple threads. Hence, the pseudo threading does not promise exceptional improvement as it would in, say, C Language.

2. Database Indexing - During each call to the API, the target url is checked for validity and then searched for existence in the database. This database search can be made faster by indexing based on the column containing the target url. Similarly, indexing shortened url should also help.

3. Modifying the function using generators and yield statements instead of for during computation of the slugs to reduce load created on the memory by for loop.

4. Code refactoring to do better code reuse.

5. Implementing Class-Based views to enable separation of concerns for views implementing get and post calls separately.

6. Writing extensive parameterized pytests to cover many possible url inputs.



E. Configuring backend to be scalable:

1. Distributing the Application and Database on multiple different servers. That will allow usage of independent resources by calls for URL-parsing and checking URL for existence in database.

2. No-Sql DB - In this scenario, as updates to the data will not be required extensively, the persistent data can be stored in memory in No-Sql databases like Redis. These databases also provide in-built features like clutering, sharding and caching and will therefore fare better than their SQL counterparts.

3. Caching - Recently searched URLs can be cached at the database level, which can help avoid database searches.

4. Load Balancing - Distributing the requests across multiple servers and managing the load distribution on each server using some service like nginx. This allows for spawning new servers as load increases and killing them when load is less, leading to better performance and response time as we are able to increase available resources on demand.



F. Test cases:
Some test cases have been written only to demonstrate unit testing using Django's TestCase Class built over python's unittest package. Please note that the test cases are not exhaustive. We can do many more unit tests to achieve better code coverage, Selenium browser tests to check front-end, integration testing to check results via queries to the database w.r.t the front-end, etc.
