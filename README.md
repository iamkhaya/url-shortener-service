# url shortener service
This is a simple url shortener service. We make use of Make to abstract away some of the
complicated commands for managing the service.

To get a close look at what is happening under the hood, take a look at the Makefile.

## Run the service locally

```bash
cd url-shortener-service
python3 -m venv venv
make deps
make run
```

## Run project's tests.

```bash
make lint
make test
```

## Deployment

For container orchestration, we use [docker-compose](https://docs.docker.com/compose/install/).

```bash
docker-compose build
docker-compose up
```

This should start the service, and it should be ready to start receiving requests.

## Using the service
For an easy guide of how to get started with the service, there is an included
postman collection file included.
```bash
scripts/url-shortener-service-postman-collection.postman_collection.json
```

Simply import that file into postman and experiment with the service endpoints against the running service.

## Architecture
I use a basic MVC approach with the main goas of separating out the concerns of the service. Pyramid swagger allows for api definition while internally the modules are separated into:

```
views -> controllers -> clients -> adapters
```

## Scale and security
I went with docker-compose because it is one the simplest orchestration tools to set up, however I would propbably use Kubernetes for container orchestration as it comes fully featured with load balancing, security
and can scale the service up and down as traffic increases/decreases. In this case we have a single instance running.

NB: There is also a token exposed in the repo (BIG NO NO in real world) Would consider using K8s secret management or a tool like Vault.

## CI/CD
I am using Github actions. In realife would using fully fledged like Jenkins.

## Why Bitly
The actual url shortening is done by [bitly](https://dev.bitly.com/). I chose this service because they have a clear api and you dont have to jump through hoops of fire to get started.

However, The code is designed that if we were to use a different 3rd part service, we would only swap out the client module and everything else shpould remain (fairly) the same.

## Things I wish I had done
* add unit tests , especially around the controllers and views
* add better file handlind around the csv upload view
* if I had to do it again, I was going to use a full-stack framework like Django to cut down on the time for the frontend work, but in realife sometimes it servces you well to separate the frontend and the backend.
* add authenitication, authorization, rate limiting, metrics, audit logging
