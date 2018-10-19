from selene.api import s, by

from .form_base import FormBase

class FrontSearchForm(FormBase):

    def __init__(self):
        self._locators = {
            "search_box"    : by.css("[name='q']"),
            "submit"        : by.css("[name='btnK']"),
            "lucky"         : by.css("[name='btnI']"),
        }

        self._fields = ['search_box']


    @property
    def search_box(self):
        return s(self._locators['search_box'])


    @property
    def submit(self):
        return s(self._locators['submit'])


    @property
    def lucky(self):
        return s(self._locators['lucky'])
