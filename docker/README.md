# Docker-based Flask web application

## Usage

To build the image:

```sh
docker build -f docker/Dockerfile -t events-app .
```

To run the container:

```sh
docker run --name events-app --rm -d -p 5000:5000 events-app
```

Access the application at http://localhost:5000.