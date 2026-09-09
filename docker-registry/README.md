# Docker Registries

## Introduction

When we use Docker to publish (push) images, by default the docker client or CLI will publish to the public docker registry hosted by hub.docker.com. 

<img src="images/docker_hub_screenshot.png"/>

However, for various reasons we may want to publish to a private registry or to a registry hosted by a cloud service such as AWS. First, let's visit how images get pushed to hub.docker.com.

## Pushing to hub.docker.com

When we run the command:

```sh
docker tag events-app tarof429/events-app
```

We are specifying the repository *tarof429* on registry-1.docker.io, the actual registry hosted by hub.docker.com. 

If we wanted to explicitly push docker images to registry-1.docker.io, we could run:

```sh
docker login registry-1.docker.io
...
docker tag events-app:latest registry-1.docker.io/tarof429/events-app:latest
docker push registry-1.docker.io/tarof429/events-app:latest
```

A quick review of the docker images on hub.docker.com should show the new image.

If we wnated to push the image to a private registry, we would replace registry-1.docker.io with the IP or hostname of our registry and optionally the port.

## Using a private registry

Let's go through an exercise where we start a private registry on the Rocky VM (build server) and pull it from our Ubuntu VM.

On the build server, run:

```sh
docker run -d -p 5000:5000 --name registry registry:3
```

Next, build and tag the image.

```sh
docker build -f docker/Dockerfile -t localhost:5000/events-app:latest .
```

Push the image. It should be very fast!

```sh
docker push localhost:5000/events-app:latest 
```

If we try to pull the image from the Ubuntu VM, it will fail. This is because the registry is insecure.

```sh
docker pull 192.168.1.133:5000/events-app:latest 
Error response from daemon: failed to resolve reference "192.168.1.133:5000/events-app:latest": failed to do request: Head "https://192.168.1.133:5000/v2/events-app/manifests/latest": http: server gave HTTP response to HTTPS client
```

One simple solution is to allow the docker client to pull from insecure registries. To do this, we can add the following to /etc/docker/daemon.json to the Ubuntu server.

```yaml
{
    "insecure-registries" : [ "192.168.1.133:5000" ]
}
```

Restart the docker daemon and retry pulling the image. Now it should work.

```sh
 docker pull 192.168.1.133:5000/events-app:latest 
latest: Pulling from events-app
Digest: sha256:f6ca5dcece3d40661c04080289f3327958ec265d9c86b41eadc0806d0d5d01d7
Status: Downloaded newer image for 192.168.1.133:5000/events-app:latest
192.168.1.133:5000/events-app:latest
```

## Implications of using a private registry

If we wanted to use a private registry in our CI/CD pipeline, we will need to change how we tag, push and pull images. Additionally, if we wanted to use a secure private registry, we would need to decide how we want to manage certificates. Using an insecure registry is the simplest solution.

Altenatively, we could use AWS ECR, which is convenient if we have other infrastructure already in AWS. Dockerhub also offers paid plans that include unlimited private registries. These services come with a cost.

A private registry may actually be useful for storing images for testing or staging before being pushed to a public repository.

## References

https://hub.docker.com/_/registry
https://distribution.github.io/distribution/
