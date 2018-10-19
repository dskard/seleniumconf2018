# Selenium Tests

## Getting Started

You'll need the following commands available on your system to run the test cases:
  * bash
  * coreutils (id, rm, cd, cat, printf, ...)
  * docker
  * docker-compose
  * git
  * make
  * python 2.7+
  * vncviewer (macosx users can launch vnc from spotlight, or the ```open```
    command in the terminal)

Make sure you also have a copy of the this repository. You can get a copy by
executing the following commands in your terminal.

```
cd ${REPOBASE};
git clone https://github.com/dskard/seleniumconf2018.git dskard-seleniumconf2018;
cd dskard-seleniumconf2018;
```

Where ```${REPOBASE}``` is the directory where you download repositories to.


## Running the Tests

The Selenium based tests in this directory use web browsers provided by
Selenium Grid Docker containers. These Docker containers can be launched and
torn down, separate from running the tests, by using the `test-env-up` and
`test-env-down` local Makefile targets.

A typical workflow for running tests may look like this:

```
# launch the Selenium Grid containers once
# at the beginning of the testing session
make test-env-up

# run all of the test
make test

# run a single test multiple times
make test PYTESTOPTS="t/test_front_page_search.py::TestFrontPageSearch::test_search_1"
make test PYTESTOPTS="t/test_front_page_search.py::TestFrontPageSearch::test_search_1"
make test PYTESTOPTS="t/test_front_page_search.py::TestFrontPageSearch::test_search_1"

# tear down the Selenium Grid containers
# at the end of the testing session
make test-env-down
```

In this example workflow, we launch the Selenium Grid containers, which host
the Firefox and Chrome web browsers, once at the beginning of the testing
session by using the `test-env-up` Makefile target. The `test-env-up` target is
responsible for launching all Docker containers that make up the testing
environment. That includes the web browser containers from the Selenium Grid
along with any other support containers that may be needed to run the tests
like mail servers, LDAP servers, and databases.

With the support containers launched, test cases can be run by using the `test`
Makefile target. The `test` target launches a separate Docker container that
hosts the `pytest` test runner process. The container communicates with the
other support containers over a virtual Docker network.  Attributes of the
`test` target can be tuned by setting a number of environment and Makefile
variables. The most often used of these variables is `PYTESTOPTS`, used to set
flags for the `pytest` test runner, like filtering the test cases to be run. A
list of all available variables is shown in the next section. Test cases can be
run multiple times against the same support containers and system under test.
This is helpful when trying to write or debug test cases during the development
cycle, where the developer may need to rerun tests multiple times without the
cost of launching the tearing down the test environment.

When the testing session has finished, the support containers can be torn down
by using the `test-env-down` Makefile target. This target is responsible for
shutting down all of the Docker containers that were launched with the
`test-env-up` target.


### Test Runner Flags

Under the hood, the Makefile's `test` target uses `pytest` as the test runner.
You can pass custom `pytest` flags via `PYTESTOPTS`. Here we are passing `-v`
which enables verbosity and `-x` which enables fast fail.

```
make test PYTESTOPTS="-xv"
```

If you want to test a specific feature, you can also use the `PYTESTOPTS`
Makefile variable to select a collection of tests.

```
# test a directory
make test PYTESTOPTS="t"

# test a specific file
make test PYTESTOPTS="t/test_front_page_search.py"

# test a class within a file
make test PYTESTOPTS="t/test_front_page_search.py::TestFrontPageSearch"

# test a specific test within a class of a specific file
make test PYTESTOPTS="t/test_front_page_search.py::TestFrontPageSearch::test_search_1"
```

##### Common pytest flags

You can find an exhaustive list of pytest flags in the [pytest
documentation](https://docs.pytest.org/en/latest/usage.html). In the table
below are listed the handful of pytest flags that pop up frequently in daily
use for configuring how and which test cases are executed.


| Flag | Description | Example | Link |
|------|-------------|---------|------|
| -x   | Stop execution after the first (or N) failures | `PYTESTOPTS="-x"` | [Learn more](https://docs.pytest.org/en/latest/usage.html#stopping-after-the-first-or-n-failures) |
| -k expression  | Run tests by keyword expressions | `PYTESTOPTS="-k ClassName and not (method1 or method2)"` | [Learn more](https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests) |
| -m expression  | Run tests by marker expressions, markers are set as `@pytest.mark.marker1` or `@pytest.mark.marker2` | `PYTESTOPTS="-m marker1 or marker2"` | [Learn more](https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests) |
| --pdb | Drop into PDB (Python Debugger) on failures | `PYTESTOPTS="--pdb"` | [Learn more](https://docs.pytest.org/en/latest/usage.html#dropping-to-pdb-python-debugger-on-failures) |
| --count=10 | Repeat each test case 10 times | `PYTESTOPTS="--count=10"` | [Learn more](https://pypi.org/project/pytest-repeat/) |
| --durations=0 | Profile test case execution. Print the time duration of each test case. | `PYTESTOPTS="--durations=0"` | [Learn more](https://docs.pytest.org/en/latest/usage.html#profiling-test-execution-duration) |
| --rerun=4 | Rerun test case failures a maximum of 4 additional times, waiting for success | `PYTESTOPTS="--rerun=4"` | [Learn more](https://github.com/pytest-dev/pytest-rerunfailures) |
| --test-group-count=10 | Specify the number of test groups. Must be used with `--test-group` flag. Primarily used for running test cases in parallel on different Jenkins nodes. | `PYTESTOPTS="--test-group-count=10"` | [Learn more](https://pypi.org/project/pytest-test-groups/) |
| --test-group=2 | Specify which group of tests to execute. Must be used with `--test-group-count`. Primarily used for running test cases in parallel on different Jenkins nodes. | `PYTESTOPTS="--test-group=2"` | [Learn more](https://pypi.org/project/pytest-test-groups/) |
| --test-group-random-seed=12345 | Randomize the grouping of test cases. Must be used with `--test-group-count` and `--test-group` flags. Primarily used for running test cases in parallel on different Jenkins nodes. | `PYTESTOPTS="--test-group-count=10 --test-group=2 --test-group-random-seed=12345"` | [Learn more](https://pypi.org/project/pytest-test-groups/) |

Although it is not a pytest command line flag, when placed inside a test case,
`import pdb; pdb.set_trace()` sets a Python Debugger breakpoint within the test
case. When the Python interpreter reaches this breakpoint, it will drop into
the Python Debugger and allow you to interactively step through the test case
code and print the values of variables. You can learn more about its use in the
[Setting
breakpoints](https://docs.pytest.org/en/latest/usage.html#setting-breakpoints)
section of the [pytest
documentation](https://docs.pytest.org/en/latest/usage.html)


### Testing by browser

You can use the `BROWSER` Makefile variable to set the web browser used in the
test run.  By default, we test against the Firefox web browser by setting
`BROWSER=firefox`. Valid option for the `BROWSER` variable are `firefox` and
`chrome`.

This feature can be combined with the any of the other test running techniques
discussed previously.

#### Test everything, using the Chrome web browser

```bash
make test BROWSER=chrome
```

#### Test a single module, using the Firefox web browser

```bash
make test PYTESTOPTS="t/test_login.py" BROWSER=firefox
```

## Using a debug container

The Makefile includes a `run` target that can be used to launch a Docker
container running on the same Docker network as the Selenium Grid and the
system under test. Enter the debug container with the command:

```bash
make run
```

The default command for the debug container is `bash`, but this can be changed
by setting the `COMMAND` Makefile variable. Another common command is to start
a Python3 interpreter:

```bash
make run COMMAND=ipython3
```

From the Python3 interpreter, Python commands can be executed to open a web
browser and navigate it to the system under test:

```python
# import the Selenium library to automate the web browser
from selenium import webdriver

# import the Selene library to help simplify browser automation
# Selene uses the Selenium library
from selene.api import browser, s, ss, be, have, by

# set the url of the system under test
url = 'http://google.com'

# launch the web browser
driver = webdriver.Remote("http://selenium-hub:4444/wd/hub", webdriver.DesiredCapabilities.FIREFOX.copy())

# associate the WebDriber object with the Selene library
browser.set_driver(driver)

# navigate the web browser to the system under test
browser.open_url(url)

# load functions from conftest
# not used in this example
from conftest import log_web_error

# use the Selene library directly to interact with the web page

# navigate the web browser to the system under test
browser.open_url(url)

# type "cheese" into the search field
s(by.css('[name="q"]')) \
  .set_value('cheese')

# click the "Google Search" button
s(by.css('[name="btnK"]')) \
  .click()

# check that results are shown
s(by.css('#resultStats')) \
  .should(be.visible)

# use page objects to interact with the web page

# load page objects
from t.pages.front_search_form import FrontSearchForm
from t.pages.app_bar import AppBar

# navigate the web browser to the google search page
browser.open_url(url)

# search for "cheese"
form = FrontSearchForm()
form.search_box.set_value('cheese')
form.submit.click()

# check that results are shown
appbar = AppBar()
appbar.result_stats.should(be.visible)

# close the web browser
browser.quit()
```

## Tuning the Test Environment

A number of environment and Makefile variables are available to tune the test
environment. Adjusting these variables change things like the types and number
of web browsers available for testing, the hostname and port of the Selenium
Grid, and the options accepted by the test runner program.

##### BROWSER

Specify the web browser to use for testing, `chrome` or `firefox`.

Default Value: "firefox"

Example usage:
```
make test BROWSER=firefox
```

##### COMMAND

Command to run inside of the debug container started with the `make run`
command.

Default Value: `bash`

Example usage:
```
make run COMMAND=python3
```

##### DCYML_GRID

File path of the Selenium Grid Docker Compile YAML config file.

Default Value: `./docker/grid/docker-compose.yml`

Example usage:
```
make test-env-up DCYML_GRID=./docker/grid/docker-compose.yml
```

##### DEBUG

Setup the test environment for debugging tests. For example, disable
GRID_TIMEOUT by setting it to 0. See below for details on GRID_TIMEOUT.

Default Value: 0

Example usage
```
DEBUG=1 make test-env-up
```

##### DOCKER_RUN_COMMAND

Command to launch a Docker container for both `make test` and `make run`
commands. This variable does not include the command that will run inside of
the Docker container. In most cases you will not need to change this variable.

Default Value:
```
DOCKER_RUN_COMMAND=docker run -it --rm --init \
    --name=tre-${HOURMINSEC} \
    --network=$(NETWORK) \
    --volume=${CURDIR}/../..:${CONNECT_DIR} \
    --user=`id -u`:`id -g` \
    --workdir=${CONNECT_DIR}/test/selenium \
    -e PYTHONPATH="${CONNECT_DIR}/test" \
    ${SELENIUM_IMAGE}
```

Example usage:
Not meant to be changed

##### GRID_HOST

Name of the Docker container hosting the Selenium Grid hub.

Default Value: `selenium-hub`

Example usage:
```
make test GRID_HOST=selenium-hub
```

##### GRID_PORT

Port number of the Docker container hosting the Selenium Grid hub.

Default Value: 4444

Example usage:
```
make test GRID_PORT=4444
```

##### GRID_TIMEOUT

Number of milliseconds the Selenium Grid Hub should wait before automatically
closing a web browser due to inactivity. This value is also set by the DEBUG
variable.

Default Value: 30000

Example usage:
```
make test-env-up GRID_TIMEOUT=30000
```

##### HOURMINSEC

Timestamp used as a part of a Docker container name.

Default Value: `date +'%H%M%S'`

Example usage:
```
make run HOURMINSEC=`date +'%y%m%d-%H%M%S'`
```

##### LOGS_DIR

Directory where log files should be store. Primarily used by `wait_for_systems_up.sh`

Default Value: `${WORKDIR}`

Example usage:
```
make LOGS_DIR=\${WORKDIR}
```

##### NETWORK

Full name of the virtual Docker network, based on PROJECT variable

Default Value: `${PROJECT}_default`

Example usage:
```
make test-env-up NETWORK=templatenet_default
```

##### PROJECT

Name used as the base of the virtual Docker network

Default Value: `templatenet`

Example usage:
```
make test-env-up PROJECT=templatenet
```

##### PYTESTLOG

Name of the file to store pytest stdout into.

Default Value: `selenium_tests.log`

Example usage:
```
make test PYTESTLOG=selenium_tests.log
```

##### PYTESTOPTS

Flags and filters to pass to the test runner program. These flags can change
the behavior of the test runner program by helping to determine which test
cases to run, what to do when a test case fails, or by injecting data into the
test runner.

Default Value: ""

Example usage:
```
make test PYTESTOPTS="t/test_front_page_search.py::TestFrontPageSearch::test_search_1"
make test PYTESTOPTS="t/test_front_page_search.py::TestFrontPageSearch::test_search_1"
make test PYTESTOPTS="-k test_search_1 -xv"
```

##### RERUN_FAILURES

Number of times to try rerunning a test failure. When a test failure occurs,
this value tells the test runner how many times to rerun the test in an attempt
to get a successful run. If all rerun attempts fail, the test will show up as
failed in the results. If one attempt passes, the failed attempts will show up
in the test results as reruns, but the results will show that the test passed.
This variable accepts zero and positive integers. Setting this value may hide
flaky test failures.

Default Value: 0

Example usage:
```
make test RERUN_FAILURES=4
```

##### RESULT_XML

Name of the file holding pytest's junit style xml results.

Default Value:`result.xml`

Example usage:
```
make test RESULT_XML=result.xml
```

##### SCALE

Number of Firefox and Chrome web browsers to launch

Default Value: 1

Example usage:
```
make test-env-up SCALE=1
```

##### SCALE_CHROME

Number of Chrome web browsers to launch, does not affect Firefox web browsers

Default Value: `${SCALE}`

Example usage:
```
make test-env-up SCALE_CHROME=2
```

##### SCALE_FIREFOX

Number of Firefox web browsers to launch, does not affect Chrome web browsers

Default Value: `${SCALE}`

Example usage:
```
make test-env-up SCALE_FIREFOX=2
```

##### SELENIUM_VERSION

Version of the Selenium Grid Docker images

Default Value: `3.8.1-dubnium`

Example usage:
```
make test-env-up SELENIUM_VERSION=3.8.1-dubnium
```

##### SUT_HOST

URI hostname of the system under test

Default Value: `www.google.io`

Example usage:
```
make test SUT_HOST=www.google.io
```

##### SUT_PORT

URI port number of the system under test

Default Value: 443

Example usage:
```
make test SUT_PORT=443
```

##### SUT_SCHEME

URI scheme of the system under test

Default Value: `https`

Example usage:
```
make test SUT_SCHEME=https
```

##### TEST_RUNNER_COMMAND

Command to launch the test runner program.

Default Value:
```
pytest \
    --junitxml=${RESULT_XML} \
    --driver=Remote \
    --host=${GRID_HOST} \
    --port=${GRID_PORT} \
    --capability browserName ${BROWSER} \
    --bundles-dir=${CONNECT_BUNDLES} \
    --url=${URL} \
    --verbose \
    ${PYTESTOPTS} \
    .
```

Example usage:
```
make test TEST_RUNNER_COMMAND="pytest"
```

##### TMP_PIPE

Name of the temporary pipe file used to capture stdout from pytest.
Do not change.

Default Value: `tmp.pipe`

Example usage:
```
make test TMP_PIPE=tmp.pipe
```

##### TRE_IMAGE

Name of the Test Runner Environment (TRE) Docker image. This image hosts the
test runner, `pytest`, and should include all software needed to run the test
cases.

Default Value: `dskard/tew:0.1.0`

Example usage:
```
make test TRE_IMAGE=dskard/tew:0.1.0
```
