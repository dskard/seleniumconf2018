from selene.api import s, by


class AppBar(object):

    def __init__(self):
        self._locators = {
            "result_stats"   : by.css("#resultStats"),
        }


    @property
    def result_stats(self):

        return s(self._locators['result_stats'])

