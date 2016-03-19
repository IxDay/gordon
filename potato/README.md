RulzUrDB
========

The application database, this database will be available internally,
external functions will be provided by the API.

# Technologies

* PostgreSQL: an object-relational database management system,
[official website](http://www.postgresql.org/).

# Running the database

This application use docker as a development environment, so that nothing will
be installed on your system except docker itself. It also allow to develop on
every OS without troubles.

* Install docker on your distro https://docs.docker.com/
* Check if docker is correctly install by running: `docker run hello-world`
* Copy the password.example file into password to customize the password used
by your container: <br/>
`cp password.example password && echo "mynewpassword" > password`
* Build the development container: `docker build -t rulzurdb .`
* Run it! `docker run --rm -P --name rulzurdb rulzurdb`

# Connect to database

It is possible to interact directly with the database through a shell,
by running the following commands.

* Launch a postgres container linked to the running rulzurdb container
`docker run --rm -t -i --link rulzurdb:rulzurdb rulzurdb bash`
* Inside the container, connect to the postgres server
`psql -h $RULZURDB_PORT_5432_TCP_ADDR -p $RULZURDB_PORT_5432_TCP_PORT
-d rulzurdb -U rulzurdb`

for further information on managing the db look at [BDD.md](./BDD.md)

# Consult volumes (logs, config)

To consult volumes we only have to connect the rulzurdb volumes to a simple
container: `docker run --rm --volumes-from rulzurdb -ti busybox sh`

The files will be available in the place where volumes were mounted in
[Dockerfile](./Dockerfile), e.g:

* `/etc/postgresql`
* `/var/log/postgresql`
* `/var/lib/postgresql`

