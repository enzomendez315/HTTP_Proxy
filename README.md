# HTTP Proxy
This program is an HTTP proxy that sits between the client and the server.
Instead of sending requests directly to the server, the client sends all 
its requests to the proxy. Upon receiving a client’s request, the proxy 
opens a connection to the server and passes on the request. The proxy receives 
the reply from the server and then sends that reply back to the client.

# Why use a proxy?
- Performance: By saving copies of the objects that it fetches, a proxy can 
  reduce the need to create connections to remote servers. This can reduce the 
  overall delay involved in retrieving an object, particularly if a server is 
  remote or under heavy load.
- Content filtering: While in the simplest case the proxy merely fetches an object 
  without inspecting it, the proxy could also be used to inspect the requested URL 
  and selectively block access to certain domains, reformat web pages (for instances, 
  by stripping out images to make a page easier to display on a handheld or other 
  limited-resource client), or perform other transformations and filtering.
- Privacy: Web servers generally log all incoming requests. This information typically 
  includes at least the IP address of the client, the browser or other client program 
  that they are using (called the User-Agent), the date and time, and the requested URL. 
  If a client does not want to have this personally identifiable information recorded, 
  routing HTTP requests through a proxy is one solution. All requests coming from clients 
  using the same proxy appear to come from the IP address and User-Agent of the proxy 
  itself, rather than the individual clients. If many clients use the same proxy 
  (say an entire business or university), it becomes much harder to link a particular HTTP 
  transaction to a single computer or individual. 
  
# Implementation
## Building a basic proxy
The first step was to build a basic proxy that was capable of accepting HTTP
requests, forwarding requests to remote (origin) servers, and returning response data to a client. For simplicity, only the GET method is implemented. Methods that are formatted correctly but that try to implement a method other than GET (like POST or HEAD) will make the proxy return a '501 Not Implemented' error to the client.

When the proxy starts, it establishes a socket that it can use to listen for incoming connections. The proxy listens on a port specified on the command line and wait for incoming client connections. Once a client has connected, the proxy reads data from the client and checks for a properly formatted HTTP request. The request needs to be in its absolute URI form:
```
<METHOD> <URL> <HTTP VERSION>
```
If there are more headers, they need to have the following format:
```
<HEADER NAME>: <HEADER VALUE>
```
Any request that does not follow these specifications will generate a '400 Bad Request' error.

Once the proxy receives and parses the URL, it makes a connection to the web server (using the appropriate remote port, or the default of 80 if none is specified) and sends the HTTP request for the appropriate object. The proxy sends the request in the relative URL + host header format regardless of how the request was received from the client.

For example, this is a request that the proxy receives from the client:
```
GET http://www.google.com/ HTTP/1.0
```
And this is the request that is sent to the web server:
```
GET / HTTP/1.0
Host: www.google.com
Connection: close
(Additional client-specified headers, if any.)
```

After the response from the server is received, the proxy sends the response message as-is to the client via the appropriate socket.

## Handling multiple clients
I used Python's `threading` module so that the proxy can handle multiple clients at the same time. The proxy sits and waits for new connections, and once it accepts a new client it uses another socket that is then passed as an argument in the `Thread.start()` function. This way every new client is handled in a separate thread.

## Caching and filtering
When the proxy receives a request, it checks if the requested object is cached. If the object is stored locally, it returns the object from the cache, without contacting the origin server. If the object is not cached, the proxy retrieves the object from the origin server, returns it to the client and caches a copy for future requests.

The cache can be enabled or disabled. When it is enabled, the proxy will check if it is stored locally. If not, the proxy requests the object from the server using a GET request. Otherwise, the proxy verifies that its cached copy is up to date ussing a "conditional GET" to the origin server. 
If the server's response indicates that the object has not been modified since it was cached, the proxy sends its current version. If the proxy's version is not updated, the server's response contains the updated version of the object, which is cached by the proxy and then sent to the client.

The proxy's blocklist can also be enabled or disabled. When it is enabled, if a proxy receives a request that refers to a blocked site, the proxy does not make the request to the server. Instead, it returns a '403 Forbidden' error to the client.

The blocklist is simply a list of strings to check against the host portion of the URI in the client’s request. If any string in the blocklist is a substring of the host portion of the URI, the client’s request is blocked.

The initial state of both the cache and the blocklist is disabled. These are the following commands that will alter the state of these two objects:
`/proxy/cache/enable`  
Enables the proxy’s cache; if it is already enabled, it does nothing. This request does not affect the contents of the cache. Future requests will consult the cache.

`/proxy/cache/disable`  
Disables the proxy’s cache; if it is already disabled, it does nothing. This request does not affect the contents of the cache. Future requests will not consult the cache.

`/proxy/cache/flush`  
Flushes (empties) the proxy’s cache. This request does not affect the enabled/disabled state of the cache.

`/proxy/blocklist/enable`  
Enables the proxy’s blocklist; if it is already enabled, it does nothing. This request does not affect the contents of the blocklist. Future requests will consult the blocklist.

`/proxy/blocklist/disable`  
Disables the proxy’s blocklist; if it is already disabled, it does nothing. This request does not affect the contents of the blocklist. Future requests will not consult the blocklist.

`/proxy/blocklist/add/<string>`  
Adds the specified string to the proxy’s blocklist; if it is already in the blocklist, it does nothing.

`/proxy/blocklist/remove/<string>`  
Removes the specified string from the proxy’s blocklist; if it is not already in the blocklist, it does nothing.

`/proxy/blocklist/flush`  
Flushes (empties) the proxy’s blocklist. This request does not affect the enabled/disabled state of the blocklist.
