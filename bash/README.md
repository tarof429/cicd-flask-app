# Bash

## Introduction

While most people will tell you to create CI/CD pipelines using a specialized tool such as Jenkins, Bash can be used to create a rudimentary CI/CD pipeline.

Below is a list of some of the actions performed by CI/CD pipelines:

1. Check for changes in git
2. Pull changes from git
3. Build the docker image
4. Push the image to docker registry
5. Update containers on the deployment server

## Pre-requisites

You should have two servers or VMs that have docker installed; see [Vaults and ansible.cfg](../ansible/README.md#vaults_and_ansible_cfg).

## Build pipeline (1)

The `build_pipeline.sh` script is a first attempt at a CI/CD pipeline. This script runs the web application on the Rocky VM. Below is a breakdown of what it does:

1. Check for changes in git
2. Pull changes from git
3. Build the docker image
5. Run the web application

To demonstrate how this script works copy this entire repository to the Rocky VM under ~admin using SSH.

```sh
tar cf ~/Downloads/cicd-flask-app.tar cicd-flask-app
scp ~/Downloads/cicd-flask-app.tar admin@<ip.of.rocky.vm>
ssh admin@<ip.of.rocky.vm>
tar xf ~/Downloads/cicd-flask-app.tar

In order to be able to run this pipeline, make sure of the following:

- The docker-compose-plugin package should be installed
- The admin user has private/public SSH keys
- The admin's public key is uploaded to git
- As admin user, login to docker hub

After running the script, you should be able to access the web application from http://<ip.of.rocky.vm>:5000.

## Build pipeline (2)

In this version of the build pipeline, we now deploy the application from the CI/CD server to a remote server. Below is a breakdown of this pipeline:

1. Check for changes in git
2. Pull changes from git
3. Build the docker image
4. Tag the image so that it can be uploaded to a remote docker registry
5. Push this image to the remote docker registry
6. Copy an enhanced version of the docker compose file to the deployment server
7. Copy the `deployment.sh` script to the deployment server
8. Run `deployment.sh`

At the end of a successful run, you should be able to access the web application from http://<ip.of.ubuntu.vm>:5000.

## Testing the pipeline

Now let's test the robustness of our pipeline. Let's add a new route in the Flask application like this:

```python
    @app.route('/test')
    def test():
        return "<p>Hello, World!</p>"
```

We can make the change directly on the Rocky server. Next, we run the pipeline again, and after deployment try http://<ip.of.ubuntu.vm>:5000/test. Did it work?

If not, a quick workaround is to go to the Ubuntu server and delete the tarof429/events-app:latest image. Run the pipeline again and test the URL. Hopefully it worked. But there's a better way. 

## Build pipeline (3)

In `build_pipeline3.sh`, we capture the git revision hash into a variable and use it to push a unique image name to docker registry. When we invoke deployment.sh on the deployment server, we pass in the revision hash as the first argument. This allows the deployment server to pull a unique image name instead of latest. 

```sh
Container admin-app-1 Stopping 
Container admin-app-1 Stopped 
Container admin-app-1 Removing 
Container admin-app-1 Removed 
Container admin-db-1 Stopping 
Container admin-db-1 Stopped 
Container admin-db-1 Removing 
Container admin-db-1 Removed 
Network admin_default Removing 
Network admin_default Removed 
Image tarof429/events-app:a714168 Pulling
 ...
Image tarof429/events-app:a714168 Pulled 
 ```

We can also confirm this image on the deployment server.

 ```sh
 admin@ubuntu-server:~$ docker images
                                                                                                                                             i Info →   U  In Use
IMAGE                         ID             DISK USAGE   CONTENT SIZE   EXTRA
postgres:14.24-alpine3.23     cb5f94ef6a4b        413MB          115MB    U   
tarof429/events-app:a714168   cb1dd3cc15a8        248MB         57.1MB    U   
tarof429/events-app:latest    8d8c0f95e6ed        248MB         57.1MB        
```