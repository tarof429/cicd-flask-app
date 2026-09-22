# Digital Ocean

## Introduction

Digital Ocean droplets can be used to run our CI/CD pipeline to deploy our Flask application. 

## Usage for the Bash Pipeline

To configure the droplets, see [Configuring Droplets](../ansible/README.md#configuring_droplets). If using firewalls, open ports 22 and 5000.

Afterwards, see [Running the Bash pipeline in Digital Ocean](../bash/README.md#digital_ocean).

If desireable, configure an A record in a DNS service such as Route 53 to point to the IP of the droplet running the Flask application. If a reverse proxy isn't used, specify the port after the domain in the URL.

While working on deploying the application in Digital Ocean, several things had to be fixed:

- Both application and docker registry were using port 5000. Docker registry has been changed to run on port 3000.
- The deploy script now explicitly pulls the image because it wasn't getting refreshed.