# Ansible

## Introduction

Often servers needs to be configured after installation. This includes tasks like installing packages, creating or configuration files, and starting and stopping services. Ansible is a great tool to automate this. All tasks can be written using YAML instead of shell scripting providing consistent coding syntax for all users. Ansible scales very well and can configure servers concurrently. It can also perform tasks based on user-defined states and perform loops. 

On the other hand, Ansible is not perfect. Hosts are defined in either INI or YAML and I think INI can be too simplistic for large scenarios while YAML can be too verbose. Some people who aren't familiar with Ansible may bear an inherit distrust of it because it can become quite complicated and difficult to troubleshoot. Also I think it's notable that Ansible, previously an open-source project, is owned by RedHat. Although Ansible works equally well with RedHat and Ubuntu based Linux distros, I still think it doesn't work well in mixed environments. 

Also because Ansible can make many changes at scale, user error can spell disaster. And if you make a mistake you can't easily reverse the damage. This is why you need to be very careful using Ansible in corporate environments; I suggest some best practices later.

The easiest way to think of Ansible is that it's an automation tool consisting of a list of servers and scripts. The list of servers is called an inventory and the scripts are called playbooks.

Let's see how we can automate some tasks, first on a web server with RockyLinux, then on another server with Ubuntu.

## Setup Webserver (1)

The `setup-webserver-1.yaml` playbook replaces the manual steps we needed to perform to configure a webserver in preparation for running our Flask application as a docker container. It uses an inventory file format called INI and is essentially a flat file, with one server per line. The playbook is in YAML format and has a list of tasks. These are documented on Ansible's website.

To run it:

```sh
ansible-playbook -i inventory.ini setup-webserver-1.yaml 
```

Whenever starting a new Ansible project or adding a new inventory item, I usually test the connection to the server using the `debug` task. What this does ensures that Ansible is able to SSH to the server; obviously if SSH does not work then Ansible can't run any other tasks.

This is followed by tasks to update the yum repository, update all existing packages, installing Docker and starting the Docker Daemon. Note that the `package` task will work with both Ubuntu or RedHat, while yum_repository will only work on RedHat. 

It seems that many people use Ansible with exactly this pattern: hosts in INI format and playbooks with a collection of tasks. However I believe the real power of Ansible is it's roles. 

## Setup Webapp (1)

The `setup-webapp-1.yaml` playbook copies the docker-compose file from the kickstart directory to the server over SSH. Then it runs the docker-compose file and starts the services. The builtin `copy` task is one of the most useful Ansible tasks. While it assumes you want to copy a local file to a remote server, you can also copy a remote file to a different location using `remote_src` or copy a local file to a different location using `delegate_to`. 

To run it:

```sh
ansible-playbook -i inventory.ini setup-webapp-1.yaml 
```

I don't recommend using relative file paths when copying files to remote servers. This is because it'ss easy to lose track which files are used by which playbooks.

In the next example, we'll look at roles which solves this and other limitations of task-based playbooks.

## Setup Webserver 2

In `setup-webserver-2.yaml`, we invoke two roles. In Ansible, roles are like functions in other languages. They are essentially reusable blocks of code that can be called from playbooks. Each role that you define has it's own directory in the `roles` subdirectory; moreover, roles have a very-well defined directory layout that must be followed according to the documentation. 

This playbook has a list of roles that are invoked from top to bottom. The role `docker` installs docker and starts the docker-daemon as before. Meanwhile, the role `webapp-compose` uploads the docker compose file to the server (now located in the files directory), brings up the services, and checks that the URL of the web application is available. 

## Update Webapp 1

The `update-webapp-1.yaml` playbook just invokes the webapp-compose role. This playbook illustrates how roles can be reused across playbooks as if invoking a function. It we were to push a new version of the events-app application, this playbook can be used to update the container on the server with the latest version.

However, simply updating containers to the `latest` version is imprecise. What we really want to do is to update a container to a specific version. Another way to look at the problem is the latest version of a container may have issues and thus we need to run the latest stable version. 

If docker-compose.yaml happened to be a shell script, maybe we would write something like this:

```sh
CONTAINER_VERSION="1.0"

docker pull tarof429/events-app:${CONTAINER_VERSION}
```

## Update Webapp 2

The `update-webapp-2` playbook invokes a modified version of our role, now called `webapp-compose2`. Instead of the `copy` task, we now use `template` to use Jinja2 to make use of the CONTAINER_VERSION variable (defined in the `vars` directory). However, note that CONTAINER_VERSION is defined to have the value of 1.0. If we don't have this version in docker registry, then docker pull will fail. To specify a different version, what we can do is specify it on the command-line.

```sh
ansible-playbook -i inventory.ini update-webapp-2.yaml -e CONTAINER_VERSION=latest
```

I usually specify variables *after* the playbook in case more variables need to be defined.

## Setup Ubuntu Server

Suppose we also have an Ubuntu server that we want to use to run docker containers. Perhaps we want to use this server to perform tasks like building the webapp container. In fact, perhaps it's our CI/CD server that we want to use for the following tasks:

- Poll github for changes
- Build webapp container
- Push the container to dockerhub
- Push the container to our deployment server
- Commit any changes to github

To do any of these tasks, we first need to install docker on it. This leads us to a problem because the playbook that we have for setting up the web server uses Ansible tasks specific to a RedHat-based Linux distro. 

The `docker2` role takes care of this issue by performing tasks conditionally based on the Linux distribution. To accomplish this, we use Ansible facts, which Ansible gathers every time it connects to an inventory item. Ansible facts are an important part of Ansible and include all kinds of information related to the OS and hardware. To access each bit of information, we need to refer to it by its hash name, so in our case `ansible_facts['os_family']`.

## References

https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_vars_facts.html
