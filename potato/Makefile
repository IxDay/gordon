CMD = "psql -U potato -h potato"
TRAVIS_CMD = "psql -U postgres"

help:
	@echo "Usage: make [COMMAND]"
	@echo ""
	@echo "help     print this message"
	@echo ""
	@echo "init     initialize the database and fill it with datas"
	@echo "         NOTE: it removes the old database if it exists"
	@echo ""
	@echo "empty    remove entries from database"
	@echo ""
	@echo "clean    remove entries from database and re-fill it with data"
	@echo ""
	@echo "connect  connect to the database directly, if a \"file\" is "
	@echo "         provided it is executed against the database"
	@echo ""

clean_log:
	@rm -f /tmp/make.log

init: clean_log
	@echo "--> Removing old db if exists"
	@eval "$(CMD) -d template1 -c 'DROP DATABASE IF EXISTS potato' \
		>> /tmp/make.log"
	@eval "$(CMD) -d template1 -c 'DROP DATABASE IF EXISTS potato_test' \
		>> /tmp/make.log"
	@echo "--> Creating databases"
	@eval "$(CMD) -d template1 -c 'CREATE DATABASE potato' >> /tmp/make.log"
	@eval "$(CMD) -d template1 -c 'CREATE DATABASE potato_test' \
		>> /tmp/make.log"
	@echo "--> Creating tables "
	@eval "$(CMD) -d potato -a -f utils/create_tables.sql >> /tmp/make.log"
	@eval "$(CMD) -d potato_test -a -f utils/create_tables.sql \
		>> /tmp/make.log"
	@echo "--> Initializing datas"
	@eval "$(CMD) -d potato -a -f utils/init.sql >> /tmp/make.log"

empty: clean_log
	@echo "--> Emptying the database"
	@eval "$(CMD) -d potato -a -f utils/clean_all.sql >> /tmp/make.log"

clean: clean_log
	@echo "--> Cleaning database"
	@eval "$(CMD) -d potato -a -f utils/clean_all.sql >> /tmp/make.log"
	@eval "$(CMD) -d potato -a -f utils/init.sql >> /tmp/make.log"

connect:
	@FILE_OPT=""; \
	if [ ! -z "$(file)" ]; then \
		echo "--> Executing file: $(file)"; \
		FILE_OPT="-a -f $(file)"; \
	else \
		echo "--> Connecting to database"; \
	fi; \
	eval "$(CMD) -d potato $$FILE_OPT"

travis_init:
	@eval "$(TRAVIS_CMD) -c 'CREATE DATABASE potato_test'"
	@eval "$(TRAVIS_CMD) -d potato_test -a -f \
		$(CURDIR)/utils/create_tables.sql"
