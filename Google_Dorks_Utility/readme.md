### Google dorks utility

### To Do

1.  Enabled Proxy.
    * Scraping Proxies from a request
    * Checking if those Proxies are alive/not
    * Check Blacklist - https://bulkblacklist.com
    * If any pass these tests - Check for 1st stage of TCP.
    * If any pass the 1st stage , then we will add those proxies into the database model.
    * User agent change , Sending the request with no cookies or cache , remove tracking ( learn ).
    * check for blacklisted proxies and delete them from the proxy list.
---
2.  Dorking files/data/downloads which are accidentally published onto the network.
    * Sending requests to google search engine. - Check the rate limit and set it.
    * Crawl the requests and get the links and information about the links.
      * Requests need to be sorted for weeks time.
    * Turn into a RSS feeder or a slow drip of logs - set the timings for each request.
    * rotate User-Agent and Proxy for every request or till the proxy dies.
    * Maintain a Database for Dorks , Proxies , Logs , Data.
    * Dorks will be maintained and checked manually before inputting it into the feeder.
    * Handle encryption on the Database.
---
3.  Spider
    * Running requests on a bucket system where when the bucket is full , the requests are filled and it will send out the requests
    call.
    * How the requests are dripped out of the bucket -> By Time,By Number,Batch size.

### dorks

inurl:Proxy.txt
