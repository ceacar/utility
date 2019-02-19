import unittest
import excalibur
import datetime

class TestGenerateHolidays(unittest.TestCase):
    def test_gen_nyse_holidays(self):
        holidays = excalibur.gen_nyse_holidays(2018)
        assert holidays == [
			datetime.date(2018, 1, 1),
			datetime.date(2018, 1, 15), datetime.date(2018, 2, 19),
			datetime.date(2018, 3, 30), datetime.date(2018, 5, 28),
			datetime.date(2018, 7, 4), datetime.date(2018, 9, 3),
			datetime.date(2018, 11, 22), datetime.date(2018, 12, 25)]

