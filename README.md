# Getting Started

**Create python3 virtual environment**

`python3 -m venv venv3`

**Activate virtual environment**

`. venv3/bin/activate`

**Install required dependencies**

`pip install -r requirements.txt`

**Install Redis**

Follow [Redis quickstart instructions](https://redis.io/topics/quickstart)

**Start Redis locally**

`redis-server`

**Start the URLShortenerService**

`mod_wsgi-express start-server urlshortenerservice.wsgi`

# Design Considerations

- The service generates random shortened keys with length 6 and base62 (small and capital alphabet and digits) is used, which allows us to generate 50M+ unique combinations.
- Shortened URLs expire after 1 week

These 2 design decisions combined allow the API server to have few key collisions when generating the random shortened keys.

# Scaling up the Service

Currently, we deploy both the Apache HTTP server and the Redis server on the same host, but for scaling up the service we would need to:

- Deploy the Apache API server and the Redis server to separate hosts
- Deploy Redis on machines with large memory
- Deploy Apache on machines with fast CPUs 
- Create a Redis cluster (multiple Redis hosts/nodes) for data redundancy
- Create a load balancer to distribute the load among the Apache server hosts
- Use separate service to pre-generate random keys to be used by the API servers because currently the API server will try to generate another random key if the key already exists (collision)

This design would ensure that we can scale up the Apache API servers independently from the Redis fleet and vice versa. This would also ensure that we can scale both Apache and Redis horizontally by adding mode hosts to either pools.

## URL Shortener Service System Design at Scale
![URL Shortener Service System Design Diagram](/resources/UrlShortenerServiceSystemDiagram.png)