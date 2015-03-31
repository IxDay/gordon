# RulzUrKitchen Architecture

This repo contains the tools for the RulzUrKitchen project

The deployement of the RulzUrKitchen development architecture is based on
Docker Compose.

## How to

* install docker [link here](https://docs.docker.com/installation/),
  and docker compose [link here](https://docs.docker.com/compose/install/)
* clone the repo
* clone RulzUrAPI, and RulzUrDB into the RulzUrArch folder
* run the following command `docker-compose -f rulzurkitchen-dev.yml up` for
  development environment and `docker-compose -f rulzurkitchen.yml` for the
  prod environment

## Attach to development container

Development containers will not launch the API so you have to attach the
container then run whatever you want
(application, tests, python interpreter, ...)

```bash
docker attach $(docker ps | awk '/rulzurkitchen_rulzurapi/ { print $1 }')
```

You can also attach a watcher to directly interact with the database container

```bash
docker attach $(docker ps | awk '/rulzurkitchen_rulzurdbwatcher/ { print $1 }')
```

You will be attached into the `/mnt` directory which will contains the
[RulzUrDB utils scripts]
(https://github.com/RulzUrLife/RulzUrDB/tree/master/utils)

To send instruction to the RulzUrDB database just follow the instructions
[here](https://github.com/RulzUrLife/RulzUrDB#connect-to-database)


To detach from a container without stopping it press `^p^q`
(ctrl-p then ctrl-q)

