# Todo Docker

Todo Docker aims to build a collection of Todo Applications that can be used not only as a reference project for various technologies, but also a starting point other projects.  If you would like to commit your stack for inclusion in this project, fork and open a PR.

## Getting Started

This project relies heavily on Docker, so the first step is to install docker and create an account on hub.docker.com.

  * Go to https://hub.docker.com/ and create a free account.
  * Log into your new account on the command line with `docker login`
  * Go to https://www.docker.com/products/overview and install the right version of docker for your OS.

This project exposes a handful of scripts that are based on make and unix shell commands.  If you are on a non-unix based OS, it is recommended to perform these steps in a unix based VM.

## Running the Server

In the root of the checkout (this directory) run `make init`.  This will create any bootstrapping files needed to get things running.  After this, running `make up` will call the appropriate commands to bring up the entire system.  If you are interested in the actually docker or docker-compose commands reference the right section in the Makefile.  At this point in time, you can hit the AngularJS app at http://127.0.0.1 and the API at http://127.0.0.1:9090.

To log into the system, you can log into the default account (created by flask/db/sample.sql).  The credentials are as follows:

  * __email:__ demo@tododocker.com
  * __password:__ password
  
## Resetting the Server
 
To stop the server press ctrl-c.  This will still keep the containers around, so if you run `make up` you will still have the same state as before.  If you would like to reset the database and any other data stored in the containers you can run `make down` followed by `make up`.  There are also a couple of files that are created the first time a container is run.  These items are usually stored in the container and don't need to be dealt with separately, but in development mode the local directory is mounted into the container causing these files to live independently of the container.  To clean up these extra files locally you can run `make reset`.
