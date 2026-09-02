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

The `build_pipeline.sh` script is a first attempt at a CI/CD pipeline. This script runs the web application on the web server. Below is a breakdown of what it does:

1. Check for changes in git
2. Pull changes from git
3. Build the docker image
5. Run the web application

Copy this entire repository to the Rocky Linux VM under ~admin.

In order to be able to run this pipeline, make sure of the following:

- The docker-compose-plugin package should be installed
- The admin user has private/public SSH keys
- The admin's public key is uploaded to git
- As admin user, login to docker hub

After running the script, you should be able to access the web application from http://<ip.of.web.server>:5000.

