BROWSER?=firefox
COMMAND=bash
DCYML_GRID=${CURDIR}/docker/grid/docker-compose.yml
GRID_HOST=selenium-hub
GRID_PORT=4444
GRID_SCHEME=http
GRID_TIMEOUT=30000
HOURMINSEC=`date +'%H%M%S'`
LOGS_DIR=${WORKDIR}
NETWORK=${PROJECT}_default
PROJECT=templatenet
PROXY=
PYTESTLOG?=selenium_tests.log
PYTESTOPTS?=
RERUN_FAILURES?=0
RESULT_XML?=result.xml
SCALE=1
SCALE_CHROME=${SCALE}
SCALE_FIREFOX=${SCALE}
SELENIUM_VERSION=3.8.1-dubnium
SUT_HOST=google.com
SUT_PORT=80
SUT_SCHEME=http
TMP_PIPE=tmp.pipe
TRE_IMAGE?=dskard/tew:0.1.0
WORKDIR=/opt/work

# Allocate a tty and keep stdin open when running locally
# Jenkins nodes don't have input tty, so we set this to ""
DOCKER_TTY_FLAGS?=-it

DOCKER_RUN_COMMAND=docker run --rm --init \
	    ${DOCKER_TTY_FLAGS} \
	    --name=tre-${HOURMINSEC} \
	    --network=$(NETWORK) \
	    --volume=${CURDIR}:${WORKDIR} \
	    --user=`id -u`:`id -g` \
	    --workdir=${WORKDIR} \
	    ${TRE_IMAGE}

TEST_RUNNER_COMMAND=pytest \
	    --junitxml=${RESULT_XML} \
	    --driver=Remote \
	    --host=${GRID_HOST} \
	    --port=${GRID_PORT} \
	    --capability browserName ${BROWSER} \
	    --proxy "${PROXY}" \
	    --url=${SUT_SCHEME}://${SUT_HOST}:${SUT_PORT} \
	    --verbose \
	    --tb=short \
	    --reruns=${RERUN_FAILURES} \
	    -m "not (fail or systemstat)" \
	    ${PYTESTOPTS}

ifdef DEBUG
	GRID_TIMEOUT=0
endif

# NOTE: This Makefile does not support running with concurrency (-j XX).
.NOTPARALLEL:

all: test

clean:
	rm -f *.png *.log ${RESULT_XML} ${TMP_PIPE};
	rm -rf .pytest_cache;

distclean: clean

# The test target launches a Docker container to run the test cases.
# Prior to launching the Docker container, we check that the prerequisite
# systems (selenium grid, system under test) are up and accepting requests.
# We also launch a named pipe to capture output from the pytest process.
# The output is sent to stdout and a log file. After the test cases run,
# we remove the named pipe, which also ends the pytest output from being
# printed to stdout through the tee command.

test: wait-for-systems-up prepare-logging
	${DOCKER_RUN_COMMAND} ${TEST_RUNNER_COMMAND} > ${TMP_PIPE} || EXITCODE=$$?; \
	rm -f ${TMP_PIPE}; \
	exit $$EXITCODE

# Create a named pipe (mkfifo) where we can forward stdout from a process.
# Then use the tee command to read from the pipe, printing the output
# to stdout and saving it to a log file. tee will terminate when it gets
# to the end of stdin, or in this case, when our named pipe is closed
# and removed.

prepare-logging:
	rm -f ${TMP_PIPE}
	mkfifo ${TMP_PIPE}
	tee ${PYTESTLOG} < ${TMP_PIPE} &

run:
	@${DOCKER_RUN_COMMAND} ${COMMAND}

test-env-up: grid-up

test-env-down: network-down

wait-for-systems-up:
	@docker run --rm \
	    --name=systemstat \
	    --network=$(NETWORK) \
	    --volume=${CURDIR}:${WORKDIR} \
	    --user=`id -u`:`id -g` \
	    --workdir=${WORKDIR} \
	    ${TRE_IMAGE} \
	    ./wait_for_systems_up.sh \
	        -g '${GRID_SCHEME}://${GRID_HOST}:${GRID_PORT}' \
	        -n $$(( ${SCALE_FIREFOX} + ${SCALE_CHROME} )) \
	        -l ${LOGS_DIR} \
	        -s '${SUT_SCHEME}://${SUT_HOST}:${SUT_PORT}'

grid-up: network-up
	NETWORK=${NETWORK} \
	GRID_TIMEOUT=${GRID_TIMEOUT} \
	SELENIUM_VERSION=${SELENIUM_VERSION} \
	docker-compose -f ${DCYML_GRID} -p ${PROJECT} up -d --scale firefox=${SCALE_FIREFOX} --scale chrome=${SCALE_CHROME}

grid-down:
	NETWORK=${NETWORK} \
	GRID_TIMEOUT=${GRID_TIMEOUT} \
	SELENIUM_VERSION=${SELENIUM_VERSION} \
	docker-compose -f ${DCYML_GRID} -p ${PROJECT} down

grid-restart:
	NETWORK=${NETWORK} \
	GRID_TIMEOUT=${GRID_TIMEOUT} \
	SELENIUM_VERSION=${SELENIUM_VERSION} \
	docker-compose -f ${DCYML_GRID} -p ${PROJECT} restart

network-up:
	$(eval NETWORK_EXISTS=$(shell docker network inspect ${NETWORK} > /dev/null 2>&1 && echo 0 || echo 1))
	@if [ "${NETWORK_EXISTS}" = "1" ] ; then \
	    echo "Creating network: ${NETWORK}"; \
	    docker network create --driver bridge ${NETWORK} ; \
	fi;

network-down: grid-down
	$(eval NETWORK_EXISTS=$(shell docker network inspect ${NETWORK} > /dev/null 2>&1 && echo 0 || echo 1))
	@if [ "${NETWORK_EXISTS}" = "0" ] ; then \
	    for i in `docker network inspect -f '{{range .Containers}}{{.Name}} {{end}}' ${NETWORK}`; do \
	        echo "Removing container \"$${i}\" from network \"${NETWORK}\""; \
	        docker network disconnect -f ${NETWORK} $${i}; \
	    done; \
	    echo "Removing network: ${NETWORK}"; \
	    docker network rm ${NETWORK}; \
	fi;

mitmproxy-up:
	docker run --rm --init -d \
	    ${DOCKER_TTY_FLAGS} \
	    --name=mitmproxy-${PROJECT} \
	    --network=$(NETWORK) \
	    --volume ~/.mitmproxy:/home/mitmproxy/.mitmproxy \
	    -p 2030:8080 \
	    -p 127.0.0.1:2031:8081 \
	    mitmproxy/mitmproxy \
	        mitmweb --web-iface 0.0.0.0

mitmproxy-down:
	$(eval MITMPROXY_EXISTS=$(shell docker container inspect mitmproxy-${PROJECT} > /dev/null 2>&1 && echo 0 || echo 1))
	@if [ "${MITMPROXY_EXISTS}" = "0" ] ; then \
        echo -n "Stopping mitmproxy-${PROJECT} ..."; \
        docker stop mitmproxy-${PROJECT} 1>/dev/null; \
        echo " done"; \
    fi;


.PHONY: all
.PHONY: clean
.PHONY: distclean
.PHONY: grid-down
.PHONY: grid-restart
.PHONY: grid-up
.PHONY: network-down
.PHONY: network-up
.PHONY: prepare-logging
.PHONY: test
.PHONY: test-env-down
.PHONY: test-env-up
.PHONY: wait-for-systems-up
