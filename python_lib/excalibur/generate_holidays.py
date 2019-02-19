#!/usr/bin/env python
import sys
from datetime import date, datetime
from dateutil.easter import easter
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta as rd
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
import six

class HolidayBase(dict):
    PROVINCES = []

    def __init__(self, years=[], expand=True, observed=True,
                 prov=None, state=None):
        self.observed = observed
        self.expand = expand
        if isinstance(years, int):
            years = [years, ]
        self.years = set(years)
        if not getattr(self, 'prov', False):
            self.prov = prov
        self.state = state
        for year in list(self.years):
            self._populate(year)

    def __setattr__(self, key, value):
        if key == 'observed' and len(self) > 0:
            dict.__setattr__(self, key, value)
            if value is True:
                # Add (Observed) dates
                years = list(self.years)
                self.years = set()
                self.clear()
                for year in years:
                    self._populate(year)
            else:
                # Remove (Observed) dates
                for k, v in list(self.items()):
                    if v.find("Observed") >= 0:
                        del self[k]
        else:
            return dict.__setattr__(self, key, value)

    def __keytransform__(self, key):
        if isinstance(key, datetime):
            key = key.date()
        elif isinstance(key, date):
            key = key
        elif isinstance(key, int) or isinstance(key, float):
            key = datetime.utcfromtimestamp(key).date()
        elif isinstance(key, six.string_types):
            try:
                key = parse(key).date()
            except:
                raise ValueError("Cannot parse date from string '%s'" % key)
        else:
            raise TypeError("Cannot convert type '%s' to date." % type(key))
        if self.expand and key.year not in self.years:
            self.years.add(key.year)
            self._populate(key.year)
        return key

    def __contains__(self, key):
        return dict.__contains__(self, self.__keytransform__(key))

    def __getitem__(self, key):
        return dict.__getitem__(self, self.__keytransform__(key))

    def __setitem__(self, key, value):
        if key in self:
            if self.get(key).find(value) < 0 \
                    and value.find(self.get(key)) < 0:
                value = "%s, %s" % (value, self.get(key))
            else:
                value = self.get(key)
        return dict.__setitem__(self, self.__keytransform__(key), value)

    def update(self, *args):
        args = list(args)
        for arg in args:
            if isinstance(arg, dict):
                for key, value in list(arg.items()):
                    self[key] = value
            elif isinstance(arg, list):
                for item in arg:
                    self[item] = "Holiday"
            else:
                self[arg] = "Holiday"

    def append(self, *args):
        return self.update(*args)

    def get(self, key, default=None):
        return dict.get(self, self.__keytransform__(key), default)

    def get_list(self, key):
        return [h for h in self.get(key, "").split(", ") if h]

    def pop(self, key, default=None):
        if default is None:
            return dict.pop(self, self.__keytransform__(key))
        return dict.pop(self, self.__keytransform__(key), default)

    def __eq__(self, other):
        return (dict.__eq__(self, other) and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return (dict.__ne__(self, other) or self.__dict__ != other.__dict__)

    def __add__(self, other):
        if isinstance(other, int) and other == 0:
            # Required to sum() list of holidays
            # sum([h1, h2]) is equivalent to (0 + h1 + h2)
            return self
        elif not isinstance(other, HolidayBase):
            raise TypeError()
        HolidaySum = createHolidaySum(self, other)
        country = (getattr(self, 'country', None) or
                   getattr(other, 'country', None))
        if self.country and other.country and self.country != other.country:
            c1 = self.country
            if not isinstance(c1, list):
                c1 = [c1]
            c2 = other.country
            if not isinstance(c2, list):
                c2 = [c2]
            country = c1 + c2
        prov = getattr(self, 'prov', None) or getattr(other, 'prov', None)
        if self.prov and other.prov and self.prov != other.prov:
            p1 = self.prov if isinstance(self.prov, list) else [self.prov]
            p2 = other.prov if isinstance(other.prov, list) else [other.prov]
            prov = p1 + p2
        return HolidaySum(years=(self.years | other.years),
                          expand=(self.expand or other.expand),
                          observed=(self.observed or other.observed),
                          country=country, prov=prov)

    def __radd__(self, other):
        return self.__add__(other)

    def _populate(self, year):
        pass



class NYSEMarketHoliday(HolidayBase):
    def _populate(self, year):
        self.populating_year = year
        # New Year's Day
        self.gen_new_year_day()
        self.gen_martin_luther_king_day()
        self.gen_washington_birthday()
        self.gen_good_friday()
        self.gen_memorial_day()
        self.gen_independence_day()
        self.gen_labor_day()
        self.gen_thanks_giving()
        self.gen_chrismas_day()

    def gen_new_year_day(self):
        if self.populating_year > 1870:
            name = "New Year's Day"
        self[date(self.populating_year, 1, 1)] = name
        if self.observed and date(self.populating_year, 1, 1).weekday() == 6:
            self[date(self.populating_year, 1, 1) + rd(days=+1)] = name + " (Observed)"
        elif self.observed and date(self.populating_year, 1, 1).weekday() == 5:
            # Add Dec 31st from the previous year without triggering
            # the entire year to be added
            expand = self.expand
            self.expand = False
            self[date(self.populating_year, 1, 1) + rd(days=-1)] = name + " (Observed)"
            self.expand = expand
        # The next self.populating_year's observed New Year's Day can be in this year
        # when it falls on a Friday (Jan 1st is a Saturday)
        if self.observed and date(self.populating_year, 12, 31).weekday() == 4:
            self[date(self.populating_year, 12, 31)] = name + " (Observed)"

    def gen_martin_luther_king_day(self):
        # Martin Luther King, Jr. Day
        if self.populating_year >= 1986:
            name = "Martin Luther King, Jr. Day"
            if self.state == 'AL':
                name = "Robert E. Lee/Martin Luther King Birthday"
            elif self.state in ('AS', 'MS'):
                name = ("Dr. Martin Luther King Jr. "
                        "and Robert E. Lee's Birthdays")
            elif self.state in ('AZ', 'NH'):
                name = "Dr. Martin Luther King Jr./Civil Rights Day"
            elif self.state == 'GA' and self.populating_year < 2012:
                name = "Robert E. Lee's Birthday"
            elif self.state == 'ID' and self.populating_year >= 2006:
                name = "Martin Luther King, Jr. - Idaho Human Rights Day"
            self[date(self.populating_year, 1, 1) + rd(weekday=MO(+3))] = name

    def gen_washington_birthday(self):
        # Washington's Birthday
        name = "Washington's Birthday"
        if self.state == 'AL':
            name = "George Washington/Thomas Jefferson Birthday"
        elif self.state == 'AS':
            name = "George Washington's Birthday and Daisy Gatson Bates Day"
        elif self.state in ('PR', 'VI'):
            name = "Presidents' Day"
        if self.state not in ('DE', 'FL', 'GA', 'NM', 'PR'):
            if self.populating_year > 1970:
                self[date(self.populating_year, 2, 1) + rd(weekday=MO(+3))] = name
            elif self.populating_year >= 1879:
                self[date(self.populating_year, 2, 22)] = name
        elif self.state == 'GA':
            if date(self.populating_year, 12, 24).weekday() != 2:
                self[date(self.populating_year, 12, 24)] = name
            else:
                self[date(self.populating_year, 12, 26)] = name
        elif self.state in ('PR', 'VI'):
            self[date(self.populating_year, 2, 1) + rd(weekday=MO(+3))] = name

    def gen_good_friday(self):
        # Good Friday
        self[easter(self.populating_year) + rd(weekday=FR(-1))] = "Good Friday"

    def gen_memorial_day(self):
        # Memorial Day
        if self.populating_year> 1970:
            self[date(self.populating_year, 5, 31) + rd(weekday=MO(-1))] = "Memorial Day"
        elif self.populating_year>= 1888:
            self[date(populating_year, 5, 30)] = "Memorial Day"

    def gen_independence_day(self):
        # Independence Day
        if self.populating_year > 1870:
            name = "Independence Day"
            self[date(self.populating_year, 7, 4)] = name
            if self.observed and date(self.populating_year, 7, 4).weekday() == 5:
                self[date(self.populating_year, 7, 4) + rd(days=-1)] = name + " (Observed)"
            elif self.observed and date(self.populating_year, 7, 4).weekday() == 6:
                self[date(self.populating_year, 7, 4) + rd(days=+1)] = name + " (Observed)"

    def gen_labor_day(self):
        # Labor Day
        if self.populating_year >= 1894:
            self[date(self.populating_year, 9, 1) + rd(weekday=MO)] = "Labor Day"

    def gen_thanks_giving(self):
        # Thanksgiving
        if self.populating_year > 1870:
            self[date(self.populating_year, 11, 1) + rd(weekday=TH(+4))] = "Thanksgiving"

    def gen_chrismas_day(self):
        # Christmas Day
        if self.populating_year > 1870:
            name = "Christmas Day"
            self[date(self.populating_year, 12, 25)] = "Christmas Day"
            if self.observed and date(self.populating_year, 12, 25).weekday() == 5:
                self[date(self.populating_year, 12, 25) + rd(days=-1)] = name + " (Observed)"
            elif self.observed and date(self.populating_year, 12, 25).weekday() == 6:
                self[date(self.populating_year, 12, 25) + rd(days=+1)] = name + " (Observed)"

def gen_nyse_holidays(year: int) -> [datetime.date]:
    holidays = NYSEMarketHoliday(years= year, state="NY")
    return sorted(holidays)

if __name__ == "__main__":
    if len(sys.argv)>1:
        year = int(sys.argv[1])
        holidays = NYSEMarketHoliday(years= year, state="NY")
    else:
        raise ValueError("not enough argument")

    for k in sorted(holidays):
        print(k)
