import argparse
import collections
import logging
import os
import pytest
import secrets
import selene
import selene.browser
import selene.config
import string
import time
import urllib.parse

from selenium.webdriver.common.proxy import *

# set the default selene reports folder
# to the present working directory
selene.config.reports_folder = os.getcwd()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


class ReportsAction(argparse.Action):
    """Custom action to update Selene's reports_folder configuration option"""

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        selene.config.reports_folder = namespace.selene_reports


class TimeoutAction(argparse.Action):
    """Custom action to update Selene's timeout configuration option"""

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        selene.config.timeout = namespace.selene_timeout


def pytest_addoption(parser):
    """Define and parse command line options"""

    parser.addoption(
        "--proxy",
        action="store",
        default="",
        help="host and port of the proxy to setup in web browser")

    parser.addoption(
        "--selene-reports",
        action=ReportsAction,
        help="parent directory for storing selene test reports")

    parser.addoption(
        "--selene-timeout",
        action=TimeoutAction,
        default=4,
        type=int,
        help="set the default timeout in selene")

    parser.addoption(
        "--url",
        action="store",
        default="http://www.google.com/",
        help="URI of the system under test")


def log_web_error(msg):
    """Take a screenshot of a web browser based error

    Use this function to capture a screen shot of the web browser
    when using Python's `assert` keyword to perform assertions.
    """

    screenshot = selene.helpers.take_screenshot(selene.browser.driver(),)
    msg = '''{original_msg}
        screenshot: file://{screenshot}'''.format(original_msg=msg, screenshot=screenshot)
    return msg


@pytest.fixture(scope="session")
def url(request):
    """Retrieve the url of the system under test"""

    return request.config.getoption("--url")


@pytest.fixture(scope="function")
def browser_config(driver):
    """Setup the core driver for the browser object

    The driver is managed by the pytest-selenium plugin, which handles
    setting up which browser to use, based on command line options.

    This fixture must stay function scoped because driver is function scoped.
    """

    # driver.set_window_size(1280,1024)
    driver.maximize_window()
    selene.browser.set_driver(driver)


@pytest.fixture(scope="session")
def proxy(request):
    """Retrieve the proxy settings"""

    return request.config.getoption("--proxy")


@pytest.fixture(scope='session')
def session_capabilities(proxy, session_capabilities):
    """Adding more capabilities for all web browsers"""

    if proxy != "":
        # add proxy settings from the command line to the web browser
        proxy_details = {
            'proxyType': 'manual',
            'httpProxy': proxy,
            'ftpProxy': proxy,
            'sslProxy': proxy,
        }
        session_capabilities['proxy'] = proxy_details

    return session_capabilities
