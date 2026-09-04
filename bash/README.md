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

## Build pipeline (4)

Pipeline scripts should run unit tests. The `build_pipeline4.sh` script takes care of running pytest within a test container; if they fail then we do not continue to build the production image and pushing it to the deployment server.

Below is a successful run (tests passed):

```sh
$ sh ./build_pipeline4.sh 
Running tests...
[+] Building 0.5s (12/12) FINISHED                               docker:default
 => [internal] load build definition from Dockerfile.test                  0.0s
 => => transferring dockerfile: 408B                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.10.21-alpine3  0.4s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => [1/7] FROM docker.io/library/python:3.10.21-alpine3.24@sha256:6e67d89  0.0s
 => => resolve docker.io/library/python:3.10.21-alpine3.24@sha256:6e67d89  0.0s
 => [internal] load build context                                          0.1s
 => => transferring context: 369.89kB                                      0.1s
 => CACHED [2/7] WORKDIR /app                                              0.0s
 => CACHED [3/7] COPY flask/requirements.txt .                             0.0s
 => CACHED [4/7] RUN pip install --no-cache-dir -r requirements.txt        0.0s
 => CACHED [5/7] COPY flask .                                              0.0s
 => CACHED [6/7] COPY docker/entrypoint_test.sh ./entrypoint.sh            0.0s
 => CACHED [7/7] RUN chmod +x entrypoint.sh                                0.0s
 => exporting to image                                                     0.0s
 => => exporting layers                                                    0.0s
 => => writing image sha256:d4df97dda071cd2ff39e8b18dc867d068cd869ee2b276  0.0s
 => => naming to docker.io/library/events-app-test                         0.0s
[+] up 1/1
 ✔ Container docker-compose-app-1 Recreated                                 0.0s
Attaching to app-1, db-1
Container docker-compose-db-1 Waiting 
db-1  | 
db-1  | PostgreSQL Database directory appears to contain a database; Skipping initialization
db-1  | 
db-1  | 2026-09-04 17:07:59.219 UTC [1] LOG:  starting PostgreSQL 14.24 on x86_64-pc-linux-musl, compiled by gcc (Alpine 15.2.0) 15.2.0, 64-bit
db-1  | 2026-09-04 17:07:59.219 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
db-1  | 2026-09-04 17:07:59.219 UTC [1] LOG:  listening on IPv6 address "::", port 5432
db-1  | 2026-09-04 17:07:59.220 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db-1  | 2026-09-04 17:07:59.222 UTC [27] LOG:  database system was shut down at 2026-09-04 17:06:27 UTC
db-1  | 2026-09-04 17:07:59.226 UTC [1] LOG:  database system is ready to accept connections
Container docker-compose-db-1 Healthy 
app-1  | ============================= test session starts ==============================
app-1  | platform linux -- Python 3.10.21, pytest-9.1.1, pluggy-1.6.0
app-1  | rootdir: /app
app-1  | collected 2 items
app-1  | 
app-1  | tests/test_event_db.py ..                                                [100%]
app-1  | 
app-1  | ============================== 2 passed in 0.45s ===============================
app-1 exited with code 0
Aborting on container exit...
Container docker-compose-app-1 Stopping 
Container docker-compose-app-1 Stopped 
Container docker-compose-db-1 Stopping 
db-1   | 2026-09-04 17:08:05.682 UTC [1] LOG:  received fast shutdown request
db-1   | 2026-09-04 17:08:05.683 UTC [1] LOG:  aborting any active transactions
db-1   | 2026-09-04 17:08:05.685 UTC [1] LOG:  background worker "logical replication launcher" (PID 33) exited with exit code 1
db-1   | 2026-09-04 17:08:05.685 UTC [28] LOG:  shutting down
db-1   | 2026-09-04 17:08:05.694 UTC [1] LOG:  database system is shut down
Container docker-compose-db-1 Stopped 
db-1 exited with code 0
Building image...
$ echo $?
0 Enable Watch   d Detach
```

Below is a failure run (tests failed); as a result, the image is not even pushed to the registry.

```sh
$ sh ./build_pipeline4.sh 
Already up to date.
Running tests...
[+] Building 0.5s (12/12) FINISHED                               docker:default
 => [internal] load build definition from Dockerfile.test                  0.0s
 => => transferring dockerfile: 408B                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.10.21-alpine3  0.4s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => [1/7] FROM docker.io/library/python:3.10.21-alpine3.24@sha256:6e67d89  0.0s
 => => resolve docker.io/library/python:3.10.21-alpine3.24@sha256:6e67d89  0.0s
 => [internal] load build context                                          0.1s
 => => transferring context: 369.93kB                                      0.1s
 => CACHED [2/7] WORKDIR /app                                              0.0s
 => CACHED [3/7] COPY flask/requirements.txt .                             0.0s
 => CACHED [4/7] RUN pip install --no-cache-dir -r requirements.txt        0.0s
 => CACHED [5/7] COPY flask .                                              0.0s
 => CACHED [6/7] COPY docker/entrypoint_test.sh ./entrypoint.sh            0.0s
 => CACHED [7/7] RUN chmod +x entrypoint.sh                                0.0s
 => exporting to image                                                     0.0s
 => => exporting layers                                                    0.0s
 => => writing image sha256:47b1f943a245e986df5667124db8098d698f811cd1012  0.0s
 => => naming to docker.io/library/events-app-test                         0.0s
[+] up 1/1
 ✔ Container docker-compose-app-1 Recreated                                 0.0s
Attaching to app-1, db-1
Container docker-compose-db-1 Waiting 
db-1  | 
db-1  | PostgreSQL Database directory appears to contain a database; Skipping initialization
db-1  | 
db-1  | 2026-09-04 17:12:59.596 UTC [1] LOG:  starting PostgreSQL 14.24 on x86_64-pc-linux-musl, compiled by gcc (Alpine 15.2.0) 15.2.0, 64-bit
db-1  | 2026-09-04 17:12:59.596 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
db-1  | 2026-09-04 17:12:59.596 UTC [1] LOG:  listening on IPv6 address "::", port 5432
db-1  | 2026-09-04 17:12:59.597 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db-1  | 2026-09-04 17:12:59.599 UTC [27] LOG:  database system was shut down at 2026-09-04 17:11:38 UTC
db-1  | 2026-09-04 17:12:59.602 UTC [1] LOG:  database system is ready to accept connections
Container docker-compose-db-1 Healthy 
app-1  | ============================= test session starts ==============================
app-1  | platform linux -- Python 3.10.21, pytest-9.1.1, pluggy-1.6.0
app-1  | rootdir: /app
app-1  | collected 3 items
app-1  | 
app-1  | tests/test_event_db.py .F.                                               [100%]
app-1  | 
app-1  | =================================== FAILURES ===================================
app-1  | __________________________________ test_false __________________________________
app-1  | 
app-1  |     def test_false():
app-1  | >       assert False
app-1  | E       assert False
app-1  | 
app-1  | tests/test_event_db.py:33: AssertionError
app-1  | =========================== short test summary info ============================
app-1  | FAILED tests/test_event_db.py::test_false - assert False
app-1  | ========================= 1 failed, 2 passed in 0.49s ==========================
app-1 exited with code 1
Aborting on container exit...
Container docker-compose-app-1 Stopping 
Container docker-compose-app-1 Stopped 
Container docker-compose-db-1 Stopping 
db-1   | 2026-09-04 17:13:06.116 UTC [1] LOG:  received fast shutdown request
db-1   | 2026-09-04 17:13:06.116 UTC [1] LOG:  aborting any active transactions
db-1   | 2026-09-04 17:13:06.118 UTC [1] LOG:  background worker "logical replication launcher" (PID 33) exited with exit code 1
db-1   | 2026-09-04 17:13:06.118 UTC [28] LOG:  shutting down
db-1   | 2026-09-04 17:13:06.127 UTC [1] LOG:  database system is shut down
Container docker-compose-db-1 Stopped 
db-1 exited with code 0

Tests failed
$ 
```

