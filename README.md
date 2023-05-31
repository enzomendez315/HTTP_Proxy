# HTTP_Proxy
This program is an HTTP proxy that sits between the client and the server.
Instead of sending requests directly to the server, the client sends all 
its requests to the proxy. Upon receiving a client’s request, the proxy 
opens a connection to the server and passes on the request. The proxy receives 
the reply from the server and then sends that reply back to the client.

## Why use a proxy?
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
