import pytest

from selene.api import browser, s, be, by

from .pages.front_search_form import FrontSearchForm
from .pages.app_bar import AppBar

pytestmark = [ pytest.mark.google,
               pytest.mark.search,
               pytest.mark.parallel,
             ]


class TestFrontPageSearch(object):

    @pytest.fixture(autouse=True)
    def setup(self, url, browser_config):
        """Navigate to the front page
        """

        # navigate to the front page
        browser.open_url(url)


    def test_search_1(self):
        """Fill in the search form, press the search button, check for results
        """

        # import pdb; pdb.set_trace()

        # type "cheese" into the search field
        s(by.css('[name="q"]')) \
            .set_value('cheese')

        # click the "Google Search" button
        s(by.css('[name="btnK"]')) \
            .click()

        # check that results are shown
        s(by.css('#resultStats')) \
            .should(be.visible)


    def test_search_2(self):
        """Fill in the search form, press the search button, check for results
        """

        # type "cheese" into the search field
        s('[name="q"]') \
            .set_value('cheese')

        # click the "Google Search" button
        s('[name="btnK"]') \
            .click()

        # check that results are shown
        s('#resultStats') \
            .should(be.visible)


    def test_search_3(self):
        """Fill in the search form, press the search button, check for results
        """

        # search for "cheese"
        FrontSearchForm() \
            .populate_form({'search_box' : 'cheese'}) \
            .submit_form()

        # check that results are shown
        AppBar() \
            .result_stats.should(be.visible)


    def test_search_4(self):
        """Fill in the search form, press the search button, check for results
        """

        # search for "cheese"
        form = FrontSearchForm()
        form.search_box.set_value('cheese')
        form.submit.click()

        # check that results are shown
        AppBar() \
            .result_stats.should(be.visible)
