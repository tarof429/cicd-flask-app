# Digital Ocean

## Introduction

Digital Ocean droplets can be used to run our CI/CD pipeline to deploy our Flask application. 

## Pre-requisites

Create 2 droplets with Ubuntu and 2GB RAM each; this can be done using the GUI. The droplets should be created in a nearby region.

## Usage for the Bash Pipeline

To configure the droplets we can use Ansible. See [Configuring Droplets](../ansible/README.md#configuring_droplets). For additional security, configure firewalls for the droplets, opening ports 22 and 5000 to each other and to ourselves.

Afterwards, see [Running the Bash pipeline in Digital Ocean](../bash/README.md#digital_ocean).

If desireable, configure an A record in a DNS service such as Route 53 to point to the IP of the droplet running the Flask application. If a reverse proxy isn't used, specify port 5000 after the domain in the URL. 

While working on deploying the application to Digital Ocean, a few things had to be fixed:

- Both application and the docker registry container were both using port 5000. Docker registry since has been changed to run on port 3000.
- The deploy script now explicitly pulls the image because it wasn't getting refreshed.

I find it convenient to create a simple script called *env.sh* with thse variables set:

```sh
export PRIVATE_REGISTRY_SERVER="<ip.of.cicd.server>"
export PRIVATE_REGISTRY_PORT="3000"
export DEPLOYMENT_SERVER="<ip.of.web.server>"
```

After sourcing this script, run *cicd-checklist.sh*. If this passes, then run *pipeline.sh*. 

Afterwards, you should be able to reach the application at *http://<ip.of.web.server>:5000* or *http://<route.53.record.name>:5000*.

To really test the pipeline, make a change in a route (such as /test), commit and push the changes. You can then curl the test page and it should contain the updated text.

<img src="images/test_page.png" />