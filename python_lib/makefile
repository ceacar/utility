SHELL := /bin/bash
tester_version = 1.0.0
project_name = excalibur
service_port = 35555
server_ip = localhost

run:
	(source setenv;\
	export PORT=$(service_port);\
	export SERVER_IP=$(service_ip);\
	python ./run.py)
install:
	(ls ./venv_py3 >/dev/null 2>&1|| virtualenv -p $$(which python3) venv_py3;\
	  source setenv;\
	  cat ./misc/requirement.txt | awk '{print "pip install",$$0}' | bash)
utest:
	(source setenv;\
	pytest -vv ./$(project_name)/tests/utests/test*.py;\
	py.test --cov-report term-missing --cov=$(project_name) ./$(project_name)/;)
itest:
	(source setenv;\
	pytest -vv ./$(project_name)/tests/itests/itest.py)

locust:
	(source setenv;\
	cd $(project_name)/tests/loadtests;\
	locust --host=$(service_ip):$(service_port))

benchmark:
	(source setenv;\
	./example_cmd_for_sanity_test.py;\
	ab -c 500 -n 5000 -s 90 $(server_ip):35555/get/b7d1c31f1654ddf1043260b571e9d8ba)

redis:
	docker-compose -f ./compose_files/redis.yml up

redis-cli:
	redis-cli -h $(server_ip) -p 10000

uwsgi:
	(source setenv;\
	uwsgi ./uwsgi.ini)
