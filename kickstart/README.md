# Kickstart

## Introduction

Kickstart can be used to automate Linux installation and is often used to install Linux on bare-metal servers in data centers. Kickstart can also be used to automate installations for KVM. In this example, we install RockyLinux with docker and run our Flask application on it.

## Pre-requisites

Perform manual installation of Linux and download /root/anaconda-ks.cfg to this location. A sample has been provided.

## Usage

Run the HTTP server and host the kickstart file.

```sh
python -m http.server
```

Run the install.sh script to install the web server. 

```sh
sh ./install.sh -n web-server -s 20 -p verysecret
```

The `-p` parameter is the password for the root user (superuser). In a kickstart file this is usually stored as an encrypted string. However since storing passwords, even encrypted ones, isn't a good git practice, the install.sh script will copy `anaconda-ks-template.cfg` to `anaconda-ks.cfg` with the unencrypted password; this is never checked into git.

Once installation has completed, the VM will reboot. This behavior is controlled by the kickstart file. In production environments with many VMs running on a server, changing reboot to shutdown may be a preferable.

## How to use the kickstarted server

Tag the events-app so that we can push it to dockerhub.

### On the VM

Login to the VM. You can use SSH or the console to do this. 

Let's set the hostname to web-server.

```sh
hostnamectl set-hostname web-server
```

Log out and log back in to see updated hostname in the command prompt.

 Next, update all packages for the latest security updates.

```sh
yum update -y
````

Reboot to take advantage of the latest kernel. In data centers, servers often need to be running with the latest kernel for security compliance. 

```sh
reboot.
```

Install Docker per https://docs.rockylinux.org/10/gemstones/containers/docker/.

Login to dockerhub. You may need to use a personal access token (PAT) for the password.

```sh
docker login -u <username>
```

Confirm that you can pull images.

```sh
docker pull hello-world
```

### On the host machine:

```sh
docker tag events-app:latest tarof429/events-app:latest
```

Push the docker image.

```sh
docker push tarof429/events-app:latest
```

Copy docker-compose.yaml to the VM.

```sh
 scp docker-compose.yaml root@<ip.of.vm>:
```

The difference between this file and the one provided by the docker-compose directory is the repository name of the docker image. Instead of

```sh
  app:
    image: events-app
```

We use

```sh
  app:
    image: tarof429/events-app:latest
```

Use the docker-compose script to run the application.

```sh
docker compose -f docker-compose.yaml up -d
```

Now you should be able to access the web application from a browser. If unsure of the IP of the VM, run `ip a`.

## Closing Thoughts

If we were to run the docker container in a server in the cloud, we'll need to deal with rootless docker and firewalls; for a home lab using KVM this is sufficient.