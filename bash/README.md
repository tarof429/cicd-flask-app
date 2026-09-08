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

Pipeline scripts should run unit tests before pushing images and deployment. The `build_pipeline4.sh` script takes care of running pytest within a test container; if they fail then we do not continue to build the production image and pushing it to the deployment server.

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

This script also includes comments for the different stages of our pipeline:

- Checkout
- Build
- Test
- Push
- Deploy

Although not well implemented, the idea is that control flow should stop if a stage fails.

## Build pipeline (5)

A real pipeline should trigger activity based on changes in a code repository. In some cases we can actively trigger the pipeline in what's called a *push*. A more simple method, useful for test environments, is to *poll* code repositories for changes.

One way to poll for changes is to create a cron job on the build server to run the pipeline at regular intervals. To implement this:

1. SSH to the build server as *admin*
2. Type crontab -e
3. Add the following:
    ```sh
    # For details see man 4 crontabs

    # Example of job definition:
    # .---------------- minute (0 - 59)
    # |  .------------- hour (0 - 23)
    # |  |  .---------- day of month (1 - 31)
    # |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
    # |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
    # |  |  |  |  |
    */5 * * * * cd /home/admin/cicd-flask-app/bash; ./build_pipeline5.sh
    ```
4. Make sure /home/admin/cicd-flask-app/bash//build_pipeline5.sh is executable

To check the crontab logs, as root, run:

```sh
tail -f /var/log/cron
```

Now make a change in Flask code and push it to github. Every 5 minutes, the script will check for remote changes. If there are remote changes, then the local repository will be synced, a new image will be built, pushed to docker hub, and go through the steps to deploy it to the deployment server. Below is an excerpt from crontab.

```sh
Sep  8 12:35:01 web-server crond[1098]: (admin) RELOAD (/var/spool/cron/admin)
Sep  8 12:35:01 web-server CROND[5815]: (admin) CMD (cd /home/admin/cicd-flask-app/bash; ./build_pipeline5.sh)
Sep  8 12:35:02 web-server CROND[5813]: (admin) CMDEND (cd /home/admin/cicd-flask-app/bash; ./build_pipeline5.sh)

Sep  8 12:40:01 web-server CROND[6431]: (admin) CMD (cd /home/admin/cicd-flask-app/bash; ./build_pipeline5.sh)
Sep  8 12:40:02 web-server CROND[6429]: (admin) CMDOUT (From github.com:tarof429/cicd-flask-app)
Sep  8 12:40:02 web-server CROND[6429]: (admin) CMDOUT (   bb9401e..27ba1bf  main       -> origin/main)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (Updating bb9401e..27ba1bf)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (Fast-forward)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT ( flask/app.py | 4 ++++)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT ( 1 file changed, 4 insertions(+))
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (Running tests...)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#0 building with "default" instance using docker driver)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#1 [internal] load build definition from Dockerfile.test)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#1 transferring dockerfile: 467B done)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#1 DONE 0.0s)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#2 [auth] library/python:pull token for registry-1.docker.io)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#2 DONE 0.0s)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#3 [internal] load metadata for docker.io/library/python:3.10.21-alpine3.24)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#3 DONE 0.6s)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#4 [internal] load .dockerignore)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#4 transferring context: 2B done)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#4 DONE 0.0s)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#5 [1/7] FROM docker.io/library/python:3.10.21-alpine3.24@sha256:6e67d897508774ad8f2250bbf0c414e029d3bc612b565017fba334b6193a798d)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#5 resolve docker.io/library/python:3.10.21-alpine3.24@sha256:6e67d897508774ad8f2250bbf0c414e029d3bc612b565017fba334b6193a798d 0.0s done)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#5 DONE 0.0s)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#6 [internal] load build context)
Sep  8 12:40:04 web-server CROND[6429]: (admin) CMDOUT (#6 transferring context: 598.37kB 0.1s done)
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT (#6 DONE 0.1s)
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT (#7 [2/7] WORKDIR /app)
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT (#7 CACHED)
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT (#8 [3/7] COPY flask/requirements.txt .)
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT (#8 CACHED)
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT (#9 [4/7] RUN pip install --no-cache-dir -r requirements.txt)
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT (#9 CACHED)
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT (#10 [5/7] COPY flask .)
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT (#10 DONE 0.6s)
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT (#11 [6/7] COPY docker/entrypoint_test.sh ./entrypoint.sh)
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT (#11 DONE 0.1s)
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT (#12 [7/7] RUN chmod +x entrypoint.sh)
Sep  8 12:40:05 web-server CROND[6429]: (admin) CMDOUT (#12 DONE 0.2s)
Sep  8 12:40:06 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:06 web-server CROND[6429]: (admin) CMDOUT (#13 exporting to image)
Sep  8 12:40:06 web-server CROND[6429]: (admin) CMDOUT (#13 exporting layers)
Sep  8 12:40:07 web-server CROND[6429]: (admin) CMDOUT (#13 exporting layers 2.0s done)
Sep  8 12:40:08 web-server CROND[6429]: (admin) CMDOUT (#13 exporting manifest sha256:d9c04594f13bc673457048a7ff6dd22d667af514d5a0cf23624d2dfceda1656c 0.0s done)
Sep  8 12:40:08 web-server CROND[6429]: (admin) CMDOUT (#13 exporting config sha256:0023c2c3b56ee9340a0035083ed42b720e0e364ae93223513138b31d8193d445 0.0s done)
Sep  8 12:40:08 web-server CROND[6429]: (admin) CMDOUT (#13 exporting attestation manifest sha256:43ea58abae38df4e3f410f147b6234b51f3c010b5701558d036e8a30d0657f12 0.0s done)
Sep  8 12:40:08 web-server CROND[6429]: (admin) CMDOUT (#13 exporting manifest list sha256:5bd8ba84577b26358a8d4fe1a15f1c8bff58215da3539521dba3fe74e93c70ba 0.0s done)
Sep  8 12:40:08 web-server CROND[6429]: (admin) CMDOUT (#13 naming to docker.io/library/events-app-test:latest done)
Sep  8 12:40:08 web-server CROND[6429]: (admin) CMDOUT (#13 unpacking to docker.io/library/events-app-test:latest)
Sep  8 12:40:08 web-server CROND[6429]: (admin) CMDOUT (#13 unpacking to docker.io/library/events-app-test:latest 0.6s done)
Sep  8 12:40:08 web-server CROND[6429]: (admin) CMDOUT (#13 DONE 2.7s)
Sep  8 12:40:08 web-server CROND[6429]: (admin) CMDOUT ( Container docker-compose-db-1 Running )
Sep  8 12:40:08 web-server CROND[6429]: (admin) CMDOUT ( Container docker-compose-app-1 Recreate )
Sep  8 12:40:19 web-server CROND[6429]: (admin) CMDOUT ( Container docker-compose-app-1 Recreated )
Sep  8 12:40:19 web-server CROND[6429]: (admin) CMDOUT (Attaching to app-1, db-1)
Sep  8 12:40:19 web-server CROND[6429]: (admin) CMDOUT ( Container docker-compose-db-1 Waiting )
Sep  8 12:40:20 web-server CROND[6429]: (admin) CMDOUT ( Container docker-compose-db-1 Healthy )
Sep  8 12:40:20 web-server CROND[6429]: (admin) CMDOUT ( Container docker-compose-app-1 Starting )
Sep  8 12:40:20 web-server CROND[6429]: (admin) CMDOUT ( Container docker-compose-app-1 Started )
Sep  8 12:40:20 web-server CROND[6429]: (admin) CMDOUT (app-1  | ============================= test session starts ==============================)
Sep  8 12:40:20 web-server CROND[6429]: (admin) CMDOUT (app-1  | platform linux -- Python 3.10.21, pytest-9.1.1, pluggy-1.6.0)
Sep  8 12:40:20 web-server CROND[6429]: (admin) CMDOUT (app-1  | rootdir: /app)
Sep  8 12:40:20 web-server CROND[6429]: (admin) CMDOUT (app-1  | collected 2 items)
Sep  8 12:40:20 web-server CROND[6429]: (admin) CMDOUT (app-1  | )
Sep  8 12:40:20 web-server CROND[6429]: (admin) CMDOUT (app-1  | tests/test_event_db.py ..                                                [100%])
Sep  8 12:40:20 web-server CROND[6429]: (admin) CMDOUT (app-1  | )
Sep  8 12:40:20 web-server CROND[6429]: (admin) CMDOUT (app-1  | ============================== 2 passed in 0.52s ===============================)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#033[Kapp-1 exited with code 0)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ( Compose Stopping Aborting on container exit...)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ( Container docker-compose-app-1 Stopping )
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ( Container docker-compose-app-1 Stopped )
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ( Container docker-compose-db-1 Stopping )
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (db-1   | 2026-09-08 19:40:21.197 UTC [1] LOG:  received fast shutdown request)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (db-1   | 2026-09-08 19:40:21.201 UTC [1] LOG:  aborting any active transactions)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (db-1   | 2026-09-08 19:40:21.202 UTC [1] LOG:  background worker "logical replication launcher" (PID 62) exited with exit code 1)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (db-1   | 2026-09-08 19:40:21.203 UTC [57] LOG:  shutting down)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (db-1   | 2026-09-08 19:40:21.212 UTC [1] LOG:  database system is shut down)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ( Container docker-compose-db-1 Stopped )
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#033[Kdb-1 exited with code 0)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (Building image...)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#0 building with "default" instance using docker driver)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#1 [internal] load build definition from Dockerfile)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#1 transferring dockerfile: 444B done)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#1 DONE 0.0s)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#2 [internal] load metadata for docker.io/library/python:3.10.21-alpine3.24)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#2 DONE 0.2s)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#3 [internal] load .dockerignore)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#3 transferring context: 2B done)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#3 DONE 0.0s)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#4 [1/7] FROM docker.io/library/python:3.10.21-alpine3.24@sha256:6e67d897508774ad8f2250bbf0c414e029d3bc612b565017fba334b6193a798d)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#4 resolve docker.io/library/python:3.10.21-alpine3.24@sha256:6e67d897508774ad8f2250bbf0c414e029d3bc612b565017fba334b6193a798d 0.0s done)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#4 DONE 0.0s)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#5 [internal] load build context)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#5 transferring context: 594.33kB 0.1s done)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#5 DONE 0.1s)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#6 [2/7] WORKDIR /app)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#6 CACHED)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#7 [3/7] COPY flask/requirements.txt .)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#7 CACHED)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#8 [4/7] RUN pip install --no-cache-dir -r requirements.txt)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#8 CACHED)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#9 [5/7] COPY flask .)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#9 CACHED)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#10 [6/7] COPY docker/entrypoint.sh .)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#10 DONE 0.0s)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#11 [7/7] RUN chmod +x entrypoint.sh)
Sep  8 12:40:21 web-server CROND[6429]: (admin) CMDOUT (#11 DONE 0.1s)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT ()
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (#12 exporting to image)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (#12 exporting layers 0.1s done)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (#12 exporting manifest sha256:dbc0d060e28fb91acb56767c04a247a3369b26b8fa8787700eeaa149d5853b8a 0.0s done)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (#12 exporting config sha256:8cd00cf8e245cac3d23c93def386528c84524f722b7d971280de3e2c223e9c68 0.0s done)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (#12 exporting attestation manifest sha256:bfcf6438ef97408c0680f2ca527bc7d9b9fa20b6541692240135316b1e1e4b94 0.0s done)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (#12 exporting manifest list sha256:82332edf46ce8be465c8e28846cbaf89ce3a2b60fcdbd58938c4f6dae37156f5 0.0s done)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (#12 naming to docker.io/library/events-app:latest done)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (#12 unpacking to docker.io/library/events-app:latest 0.0s done)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (#12 DONE 0.2s)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (The push refers to repository [docker.io/tarof429/events-app])
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (55afa1ecc21d: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (65b3e29755da: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (44136fa355b3: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (c1aca9005329: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (65b3e29755da: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (44136fa355b3: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (c1aca9005329: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (55afa1ecc21d: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (c1aca9005329: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (55afa1ecc21d: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (65b3e29755da: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (44136fa355b3: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (44136fa355b3: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (c1aca9005329: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (55afa1ecc21d: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (65b3e29755da: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (65b3e29755da: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (44136fa355b3: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (c1aca9005329: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (55afa1ecc21d: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (65b3e29755da: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (44136fa355b3: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (c1aca9005329: Waiting)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (55afa1ecc21d: Layer already exists)
Sep  8 12:40:22 web-server CROND[6429]: (admin) CMDOUT (46958db24bed: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (46958db24bed: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (65b3e29755da: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (44136fa355b3: Already exists)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (c1aca9005329: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (e872d8403654: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (823c447f50bc: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (aa34bacb5a66: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (65b3e29755da: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (ac5139085299: Layer already exists)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (c1aca9005329: Layer already exists)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (e872d8403654: Layer already exists)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (46958db24bed: Layer already exists)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (1568f7417c2d: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (bfb95cc155cc: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (8f7d7fc9e342: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (1568f7417c2d: Layer already exists)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (823c447f50bc: Layer already exists)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (aa34bacb5a66: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (bfb95cc155cc: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (8f7d7fc9e342: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (aa34bacb5a66: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (8f7d7fc9e342: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (aa34bacb5a66: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (bfb95cc155cc: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (8f7d7fc9e342: Waiting)
Sep  8 12:40:23 web-server CROND[6429]: (admin) CMDOUT (aa34bacb5a66: Waiting)
Sep  8 12:40:24 web-server CROND[6429]: (admin) CMDOUT (65b3e29755da: Pushed)
Sep  8 12:40:24 web-server CROND[6429]: (admin) CMDOUT (bfb95cc155cc: Pushed)
Sep  8 12:40:24 web-server CROND[6429]: (admin) CMDOUT (8f7d7fc9e342: Pushed)
Sep  8 12:40:39 web-server CROND[6429]: (admin) CMDOUT (aa34bacb5a66: Pushed)
Sep  8 12:40:41 web-server CROND[6429]: (admin) CMDOUT (27ba1bf: digest: sha256:82332edf46ce8be465c8e28846cbaf89ce3a2b60fcdbd58938c4f6dae37156f5 size: 856)
Sep  8 12:40:42 web-server CROND[6429]: (admin) CMDOUT ( Container admin-app-1 Stopping )
Sep  8 12:40:52 web-server CROND[6429]: (admin) CMDOUT ( Container admin-app-1 Stopped )
Sep  8 12:40:52 web-server CROND[6429]: (admin) CMDOUT ( Container admin-app-1 Removing )
Sep  8 12:40:52 web-server CROND[6429]: (admin) CMDOUT ( Container admin-app-1 Removed )
Sep  8 12:40:52 web-server CROND[6429]: (admin) CMDOUT ( Container admin-db-1 Stopping )
Sep  8 12:40:52 web-server CROND[6429]: (admin) CMDOUT ( Container admin-db-1 Stopped )
Sep  8 12:40:52 web-server CROND[6429]: (admin) CMDOUT ( Container admin-db-1 Removing )
Sep  8 12:40:52 web-server CROND[6429]: (admin) CMDOUT ( Container admin-db-1 Removed )
Sep  8 12:40:52 web-server CROND[6429]: (admin) CMDOUT ( Network admin_default Removing )
Sep  8 12:40:52 web-server CROND[6429]: (admin) CMDOUT ( Network admin_default Removed )
Sep  8 12:40:52 web-server CROND[6429]: (admin) CMDOUT ( Image tarof429/events-app:27ba1bf Pulling )
Sep  8 12:40:55 web-server CROND[6429]: (admin) CMDOUT ( 44136fa355b3 Already exists 0B)
Sep  8 12:40:55 web-server CROND[6429]: (admin) CMDOUT ( 8f7d7fc9e342 Pulling fs layer 0B)
Sep  8 12:40:55 web-server CROND[6429]: (admin) CMDOUT ( bfb95cc155cc Pulling fs layer 0B)
Sep  8 12:40:55 web-server CROND[6429]: (admin) CMDOUT ( aa34bacb5a66 Pulling fs layer 0B)
Sep  8 12:40:55 web-server CROND[6429]: (admin) CMDOUT ( bfb95cc155cc Download complete 0B)
Sep  8 12:40:55 web-server CROND[6429]: (admin) CMDOUT ( 65b3e29755da Download complete 0B)
Sep  8 12:40:55 web-server CROND[6429]: (admin) CMDOUT ( 8f7d7fc9e342 Download complete 0B)
Sep  8 12:40:56 web-server CROND[6429]: (admin) CMDOUT ( aa34bacb5a66 Downloading 2.097MB)
Sep  8 12:40:56 web-server CROND[6429]: (admin) CMDOUT ( aa34bacb5a66 Downloading 5.243MB)
Sep  8 12:40:56 web-server CROND[6429]: (admin) CMDOUT ( aa34bacb5a66 Downloading 10.49MB)
Sep  8 12:40:56 web-server CROND[6429]: (admin) CMDOUT ( aa34bacb5a66 Downloading 15.73MB)
Sep  8 12:40:56 web-server CROND[6429]: (admin) CMDOUT ( aa34bacb5a66 Downloading 18.94MB)
Sep  8 12:40:56 web-server CROND[6429]: (admin) CMDOUT ( aa34bacb5a66 Download complete 0B)
Sep  8 12:40:56 web-server CROND[6429]: (admin) CMDOUT ( aa34bacb5a66 Extracting 1B)
Sep  8 12:40:57 web-server CROND[6429]: (admin) CMDOUT ( aa34bacb5a66 Extracting 1B)
Sep  8 12:40:57 web-server CROND[6429]: (admin) CMDOUT ( aa34bacb5a66 Extracting 1B)
Sep  8 12:40:57 web-server CROND[6429]: (admin) CMDOUT ( aa34bacb5a66 Extracting 1B)
Sep  8 12:40:57 web-server CROND[6429]: (admin) CMDOUT ( bfb95cc155cc Pull complete 0B)
Sep  8 12:40:57 web-server CROND[6429]: (admin) CMDOUT ( 8f7d7fc9e342 Extracting 1B)
Sep  8 12:40:57 web-server CROND[6429]: (admin) CMDOUT ( aa34bacb5a66 Pull complete 0B)
Sep  8 12:40:57 web-server CROND[6429]: (admin) CMDOUT ( 8f7d7fc9e342 Pull complete 0B)
Sep  8 12:40:57 web-server CROND[6429]: (admin) CMDOUT ( Image tarof429/events-app:27ba1bf Pulled )
Sep  8 12:40:57 web-server CROND[6429]: (admin) CMDOUT ( Network admin_default Creating )
Sep  8 12:40:57 web-server CROND[6429]: (admin) CMDOUT ( Network admin_default Creating )
Sep  8 12:40:57 web-server CROND[6429]: (admin) CMDOUT ( Network admin_default Created )
Sep  8 12:40:57 web-server CROND[6429]: (admin) CMDOUT ( Network admin_default Created )
Sep  8 12:40:57 web-server CROND[6429]: (admin) CMDOUT ( Container admin-db-1 Creating )
Sep  8 12:40:58 web-server CROND[6429]: (admin) CMDOUT ( Container admin-db-1 Created )
Sep  8 12:40:58 web-server CROND[6429]: (admin) CMDOUT ( Container admin-app-1 Creating )
Sep  8 12:40:58 web-server CROND[6429]: (admin) CMDOUT ( Container admin-app-1 Created )
Sep  8 12:40:58 web-server CROND[6429]: (admin) CMDOUT ( Container admin-db-1 Starting )
Sep  8 12:40:58 web-server CROND[6429]: (admin) CMDOUT ( Container admin-db-1 Started )
Sep  8 12:40:58 web-server CROND[6429]: (admin) CMDOUT ( Container admin-db-1 Waiting )
Sep  8 12:41:03 web-server CROND[6429]: (admin) CMDOUT ( Container admin-db-1 Healthy )
Sep  8 12:41:03 web-server CROND[6429]: (admin) CMDOUT ( Container admin-app-1 Starting )
Sep  8 12:41:03 web-server CROND[6429]: (admin) CMDOUT ( Container admin-app-1 Started )
Sep  8 12:41:06 web-server CROND[6429]: (admin) CMDOUT (  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current)
Sep  8 12:41:06 web-server CROND[6429]: (admin) CMDOUT (                                 Dload  Upload   Total   Spent    Left  Speed)
Sep  8 12:41:06 web-server CROND[6429]: (admin) CMDOUT (  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0Application is running)
Sep  8 12:41:06 web-server CROND[6429]: (admin) CMDOUT (100  1533  100  1533    0     0   150k      0 --:--:-- --:--:-- --:--:--  166k)
Sep  8 12:41:06 web-server CROND[6429]: (admin) CMDEND (cd /home/admin/cicd-flask-app/bash; ./build_pipeline5.sh)
^C
root@web-server:/var/log# tail -f cron

```

You should also be able to verify the new docker image on the deployment server.

```sh
admin@ubuntu-server:~$ docker ps
CONTAINER ID   IMAGE                         COMMAND                  CREATED         STATUS                   PORTS                                         NAMES
9327c9f157ba   tarof429/events-app:7180ba9   "./entrypoint.sh"        2 minutes ago   Up 2 minutes             0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp   admin-app-1
ff7bd04fa021   postgres:14.24-alpine3.23     "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   admin-db-1
admin@ubuntu-server:~$ docker ps
CONTAINER ID   IMAGE                         COMMAND                  CREATED          STATUS                    PORTS                                         NAMES
ad9b77f88f2f   tarof429/events-app:27ba1bf   "./entrypoint.sh"        25 minutes ago   Up 25 minutes             0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp   admin-app-1
faaa3eb27e67   postgres:14.24-alpine3.23     "docker-entrypoint.s…"   25 minutes ago   Up 25 minutes (healthy)   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   admin-db-1
```