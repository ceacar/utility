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




class UnitedStates(HolidayBase): # https://en.wikipedia.org/wiki/Public_holidays_in_the_United_States 

    STATES = ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
              'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
              'MD', 'MH', 'MA', 'MI', 'FM', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
              'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW',
              'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'VI',
              'WA', 'WV', 'WI', 'WY']

    def __init__(self, **kwargs):
        self.country = 'US'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        # New Year's Day
        if year > 1870:
            name = "New Year's Day"
        self[date(year, 1, 1)] = name
        if self.observed and date(year, 1, 1).weekday() == 6:
            self[date(year, 1, 1) + rd(days=+1)] = name + " (Observed)"
        elif self.observed and date(year, 1, 1).weekday() == 5:
            # Add Dec 31st from the previous year without triggering
            # the entire year to be added
            expand = self.expand
            self.expand = False
            self[date(year, 1, 1) + rd(days=-1)] = name + " (Observed)"
            self.expand = expand
        # The next year's observed New Year's Day can be in this year
        # when it falls on a Friday (Jan 1st is a Saturday)
        if self.observed and date(year, 12, 31).weekday() == 4:
            self[date(year, 12, 31)] = name + " (Observed)"

        # Epiphany
        if self.state == 'PR':
            self[date(year, 1, 6)] = "Epiphany"

        # Three King's Day
        if self.state == 'VI':
            self[date(year, 1, 6)] = "Three King's Day"

        # Lee Jackson Day
        name = "Lee Jackson Day"
        if self.state == 'VA' and year >= 2000:
            dt = date(year, 1, 1) + rd(weekday=MO(+3)) + rd(weekday=FR(-1))
            self[dt] = name
        elif self.state == 'VA' and year >= 1983:
            self[date(year, 1, 1) + rd(weekday=MO(+3))] = name
        elif self.state == 'VA' and year >= 1889:
            self[date(year, 1, 19)] = name

        # Inauguration Day
        if self.state in ('DC', 'LA', 'MD', 'VA') and year >= 1789:
            name = "Inauguration Day"
            if (year - 1789) % 4 == 0 and year >= 1937:
                self[date(year, 1, 20)] = name
                if date(year, 1, 20).weekday() == 6:
                    self[date(year, 1, 21)] = name + " (Observed)"
            elif (year - 1789) % 4 == 0:
                self[date(year, 3, 4)] = name
                if date(year, 3, 4).weekday() == 6:
                    self[date(year, 3, 5)] = name + " (Observed)"

        # Martin Luther King, Jr. Day
        if year >= 1986:
            name = "Martin Luther King, Jr. Day"
            if self.state == 'AL':
                name = "Robert E. Lee/Martin Luther King Birthday"
            elif self.state in ('AS', 'MS'):
                name = ("Dr. Martin Luther King Jr. "
                        "and Robert E. Lee's Birthdays")
            elif self.state in ('AZ', 'NH'):
                name = "Dr. Martin Luther King Jr./Civil Rights Day"
            elif self.state == 'GA' and year < 2012:
                name = "Robert E. Lee's Birthday"
            elif self.state == 'ID' and year >= 2006:
                name = "Martin Luther King, Jr. - Idaho Human Rights Day"
            self[date(year, 1, 1) + rd(weekday=MO(+3))] = name

        # Lincoln's Birthday
        name = "Lincoln's Birthday"
        if (self.state in ('CT', 'IL', 'IA', 'NJ', 'NY') and year >= 1971) \
                or (self.state == 'CA' and year >= 1971 and year <= 2009):
            self[date(year, 2, 12)] = name
            if self.observed and date(year, 2, 12).weekday() == 5:
                self[date(year, 2, 11)] = name + " (Observed)"
            elif self.observed and date(year, 2, 12).weekday() == 6:
                self[date(year, 2, 13)] = name + " (Observed)"

        # Susan B. Anthony Day
        if (self.state == 'CA' and year >= 2014) \
                or (self.state == 'FL' and year >= 2011) \
                or (self.state == 'NY' and year >= 2004) \
                or (self.state == 'WI' and year >= 1976):
            self[date(year, 2, 15)] = "Susan B. Anthony Day"

        # Washington's Birthday
        name = "Washington's Birthday"
        if self.state == 'AL':
            name = "George Washington/Thomas Jefferson Birthday"
        elif self.state == 'AS':
            name = "George Washington's Birthday and Daisy Gatson Bates Day"
        elif self.state in ('PR', 'VI'):
            name = "Presidents' Day"
        if self.state not in ('DE', 'FL', 'GA', 'NM', 'PR'):
            if year > 1970:
                self[date(year, 2, 1) + rd(weekday=MO(+3))] = name
            elif year >= 1879:
                self[date(year, 2, 22)] = name
        elif self.state == 'GA':
            if date(year, 12, 24).weekday() != 2:
                self[date(year, 12, 24)] = name
            else:
                self[date(year, 12, 26)] = name
        elif self.state in ('PR', 'VI'):
            self[date(year, 2, 1) + rd(weekday=MO(+3))] = name

        # Mardi Gras
        if self.state == 'LA' and year >= 1857:
            self[easter(year) + rd(days=-47)] = "Mardi Gras"

        # Guam Discovery Day
        if self.state == 'GU' and year >= 1970:
            self[date(year, 3, 1) + rd(weekday=MO)] = "Guam Discovery Day"

        # Casimir Pulaski Day
        if self.state == 'IL' and year >= 1978:
            self[date(year, 3, 1) + rd(weekday=MO)] = "Casimir Pulaski Day"

        # Texas Independence Day
        if self.state == 'TX' and year >= 1874:
            self[date(year, 3, 2)] = "Texas Independence Day"

        # Town Meeting Day
        if self.state == 'VT' and year >= 1800:
            self[date(year, 3, 1) + rd(weekday=TU)] = "Town Meeting Day"

        # Evacuation Day
        if self.state == 'MA' and year >= 1901:
            name = "Evacuation Day"
            self[date(year, 3, 17)] = name
            if date(year, 3, 17).weekday() in (5, 6):
                self[date(year, 3, 17) + rd(weekday=MO)] = name + " (Observed)"

        # Emancipation Day
        if self.state == 'PR':
            self[date(year, 3, 22)] = "Emancipation Day"
            if self.observed and date(year, 3, 22).weekday() == 6:
                self[date(year, 3, 23)] = "Emancipation Day (Observed)"

        # Prince Jonah Kuhio Kalanianaole Day
        if self.state == 'HI' and year >= 1949:
            name = "Prince Jonah Kuhio Kalanianaole Day"
            self[date(year, 3, 26)] = name
            if self.observed and date(year, 3, 26).weekday() == 5:
                self[date(year, 3, 25)] = name + " (Observed)"
            elif self.observed and date(year, 3, 26).weekday() == 6:
                self[date(year, 3, 27)] = name + " (Observed)"

        # Steward's Day
        name = "Steward's Day"
        if self.state == 'AK' and year >= 1955:
            self[date(year, 4, 1) + rd(days=-1, weekday=MO(-1))] = name
        elif self.state == 'AK' and year >= 1918:
            self[date(year, 3, 30)] = name

        # Cesar Chavez Day
        name = "Cesar Chavez Day"
        if self.state == 'CA' and year >= 1995:
            self[date(year, 3, 31)] = name
            if self.observed and date(year, 3, 31).weekday() == 6:
                self[date(year, 4, 1)] = name + " (Observed)"
        elif self.state == 'TX' and year >= 2000:
            self[date(year, 3, 31)] = name

        # Transfer Day
        if self.state == 'VI':
            self[date(year, 3, 31)] = "Transfer Day"

        # Emancipation Day
        if self.state == 'DC' and year >= 2005:
            name = "Emancipation Day"
            self[date(year, 4, 16)] = name
            if self.observed and date(year, 4, 16).weekday() == 5:
                self[date(year, 4, 15)] = name + " (Observed)"
            elif self.observed and date(year, 4, 16).weekday() == 6:
                self[date(year, 4, 17)] = name + " (Observed)"

        # Patriots' Day
        if self.state in ('ME', 'MA') and year >= 1969:
            self[date(year, 4, 1) + rd(weekday=MO(+3))] = "Patriots' Day"
        elif self.state in ('ME', 'MA') and year >= 1894:
            self[date(year, 4, 19)] = "Patriots' Day"

        # Holy Thursday
        if self.state == 'VI':
            self[easter(year) + rd(weekday=TH(-1))] = "Holy Thursday"

        # Good Friday
        if self.state in ('CT', 'DE', 'GU', 'IN', 'KY', 'LA',
                          'NJ', 'NC', 'PR', 'TN', 'TX', 'VI'):
            self[easter(year) + rd(weekday=FR(-1))] = "Good Friday"

        # Easter Monday
        if self.state == 'VI':
            self[easter(year) + rd(weekday=MO)] = "Easter Monday"

        # Confederate Memorial Day
        name = "Confederate Memorial Day"
        if self.state in ('AL', 'GA', 'MS', 'SC') and year >= 1866:
            if self.state == 'GA' and year >= 2016:
                name = "State Holiday"
            self[date(year, 4, 1) + rd(weekday=MO(+4))] = name
        elif self.state == 'TX' and year >= 1931:
            self[date(year, 1, 19)] = name

        # San Jacinto Day
        if self.state == 'TX' and year >= 1875:
            self[date(year, 4, 21)] = "San Jacinto Day"

        # Arbor Day
        if self.state == 'NE' and year >= 1989:
            self[date(year, 4, 30) + rd(weekday=FR(-1))] = "Arbor Day"
        elif self.state == 'NE' and year >= 1875:
            self[date(year, 4, 22)] = "Arbor Day"

        # Primary Election Day
        if self.state == 'IN' and \
                ((year >= 2006 and year % 2 == 0) or year >= 2015):
            dt = date(year, 5, 1) + rd(weekday=MO)
            self[dt + rd(days=+1)] = "Primary Election Day"

        # Truman Day
        if self.state == 'MO' and year >= 1949:
            name = "Truman Day"
            self[date(year, 5, 8)] = name
            if self.observed and date(year, 5, 8).weekday() == 5:
                self[date(year, 5, 7)] = name + " (Observed)"
            elif self.observed and date(year, 5, 8).weekday() == 6:
                self[date(year, 5, 10)] = name + " (Observed)"

        # Memorial Day
        if year > 1970:
            self[date(year, 5, 31) + rd(weekday=MO(-1))] = "Memorial Day"
        elif year >= 1888:
            self[date(year, 5, 30)] = "Memorial Day"

        # Jefferson Davis Birthday
        name = "Jefferson Davis Birthday"
        if self.state == 'AL' and year >= 1890:
            self[date(year, 6, 1) + rd(weekday=MO)] = name

        # Kamehameha Day
        if self.state == 'HI' and year >= 1872:
            self[date(year, 6, 11)] = "Kamehameha Day"
            if self.observed and year >= 2011:
                if date(year, 6, 11).weekday() == 5:
                    self[date(year, 6, 10)] = "Kamehameha Day (Observed)"
                elif date(year, 6, 11).weekday() == 6:
                    self[date(year, 6, 12)] = "Kamehameha Day (Observed)"

        # Emancipation Day In Texas
        if self.state == 'TX' and year >= 1980:
            self[date(year, 6, 19)] = "Emancipation Day In Texas"

        # West Virginia Day
        name = "West Virginia Day"
        if self.state == 'WV' and year >= 1927:
            self[date(year, 6, 20)] = name
            if self.observed and date(year, 6, 20).weekday() == 5:
                self[date(year, 6, 19)] = name + " (Observed)"
            elif self.observed and date(year, 6, 20).weekday() == 6:
                self[date(year, 6, 21)] = name + " (Observed)"

        # Emancipation Day in US Virgin Islands
        if self.state == 'VI':
            self[date(year, 7, 3)] = "Emancipation Day"

        # Independence Day
        if year > 1870:
            name = "Independence Day"
            self[date(year, 7, 4)] = name
            if self.observed and date(year, 7, 4).weekday() == 5:
                self[date(year, 7, 4) + rd(days=-1)] = name + " (Observed)"
            elif self.observed and date(year, 7, 4).weekday() == 6:
                self[date(year, 7, 4) + rd(days=+1)] = name + " (Observed)"

        # Liberation Day (Guam)
        if self.state == 'GU' and year >= 1945:
            self[date(year, 7, 21)] = "Liberation Day (Guam)"

        # Pioneer Day
        if self.state == 'UT' and year >= 1849:
            name = "Pioneer Day"
            self[date(year, 7, 24)] = name
            if self.observed and date(year, 7, 24).weekday() == 5:
                self[date(year, 7, 24) + rd(days=-1)] = name + " (Observed)"
            elif self.observed and date(year, 7, 24).weekday() == 6:
                self[date(year, 7, 24) + rd(days=+1)] = name + " (Observed)"

        # Constitution Day
        if self.state == 'PR':
            self[date(year, 7, 25)] = "Constitution Day"
            if self.observed and date(year, 7, 25).weekday() == 6:
                self[date(year, 7, 26)] = "Constitution Day (Observed)"

        # Victory Day
        if self.state == 'RI' and year >= 1948:
            self[date(year, 8, 1) + rd(weekday=MO(+2))] = "Victory Day"

        # Statehood Day (Hawaii)
        if self.state == 'HI' and year >= 1959:
            self[date(year, 8, 1) + rd(weekday=FR(+3))] = "Statehood Day"

        # Bennington Battle Day
        if self.state == 'VT' and year >= 1778:
            name = "Bennington Battle Day"
            self[date(year, 8, 16)] = name
            if self.observed and date(year, 8, 16).weekday() == 5:
                self[date(year, 8, 15)] = name + " (Observed)"
            elif self.observed and date(year, 8, 16).weekday() == 6:
                self[date(year, 8, 17)] = name + " (Observed)"

        # Lyndon Baines Johnson Day
        if self.state == 'TX' and year >= 1973:
            self[date(year, 8, 27)] = "Lyndon Baines Johnson Day"

        # Labor Day
        if year >= 1894:
            self[date(year, 9, 1) + rd(weekday=MO)] = "Labor Day"

        # Columbus Day
        if self.state not in ('AK', 'DE', 'FL', 'HI', 'NV'):
            if self.state == 'SD':
                name = "Native American Day"
            elif self.state == 'VI':
                name = "Columbus Day and Puerto Rico Friendship Day"
            else:
                name = "Columbus Day"
            if year >= 1970:
                self[date(year, 10, 1) + rd(weekday=MO(+2))] = name
            elif year >= 1937:
                self[date(year, 10, 12)] = name

        # Alaska Day
        if self.state == 'AK' and year >= 1867:
            self[date(year, 10, 18)] = "Alaska Day"
            if self.observed and date(year, 10, 18).weekday() == 5:
                self[date(year, 10, 18) + rd(days=-1)] = name + " (Observed)"
            elif self.observed and date(year, 10, 18).weekday() == 6:
                self[date(year, 10, 18) + rd(days=+1)] = name + " (Observed)"

        # Nevada Day
        if self.state == 'NV' and year >= 1933:
            dt = date(year, 10, 31)
            if year >= 2000:
                dt += rd(weekday=FR(-1))
            self[dt] = "Nevada Day"
            if self.observed and dt.weekday() == 5:
                self[dt + rd(days=-1)] = "Nevada Day (Observed)"
            elif self.observed and dt.weekday() == 6:
                self[dt + rd(days=+1)] = "Nevada Day (Observed)"

        # Liberty Day
        if self.state == 'VI':
            self[date(year, 11, 1)] = "Liberty Day"

        # Election Day
        if (self.state in ('DE', 'HI', 'IL', 'IN', 'LA',
                           'MT', 'NH', 'NJ', 'NY', 'WV') and
                year >= 2008 and year % 2 == 0) \
                or (self.state in ('IN', 'NY') and year >= 2015):
            dt = date(year, 11, 1) + rd(weekday=MO)
            self[dt + rd(days=+1)] = "Election Day"

        # All Souls' Day
        if self.state == 'GU':
            self[date(year, 11, 2)] = "All Souls' Day"

        # Veterans Day
        if year > 1953:
            name = "Veterans Day"
        else:
            name = "Armistice Day"
        if 1978 > year > 1970:
            self[date(year, 10, 1) + rd(weekday=MO(+4))] = name
        elif year >= 1938:
            self[date(year, 11, 11)] = name
            if self.observed and date(year, 11, 11).weekday() == 5:
                self[date(year, 11, 11) + rd(days=-1)] = name + " (Observed)"
            elif self.observed and date(year, 11, 11).weekday() == 6:
                self[date(year, 11, 11) + rd(days=+1)] = name + " (Observed)"

        # Discovery Day
        if self.state == 'PR':
            self[date(year, 11, 19)] = "Discovery Day"
            if self.observed and date(year, 11, 19).weekday() == 6:
                self[date(year, 11, 20)] = "Discovery Day (Observed)"

        # Thanksgiving
        if year > 1870:
            self[date(year, 11, 1) + rd(weekday=TH(+4))] = "Thanksgiving"

        # Day After Thanksgiving
        # Friday After Thanksgiving
        # Lincoln's Birthday
        # American Indian Heritage Day
        # Family Day
        # New Mexico Presidents' Day
        if (self.state in ('DE', 'FL', 'NH', 'NC', 'OK', 'TX', 'WV') and
                year >= 1975) \
                or (self.state == 'IN' and year >= 2010) \
                or (self.state == 'MD' and year >= 2008) \
                or self.state in ('NV', 'NM'):
            if self.state in ('DE', 'NH', 'NC', 'OK', 'WV'):
                name = "Day After Thanksgiving"
            elif self.state in ('FL', 'TX'):
                name = "Friday After Thanksgiving"
            elif self.state == 'IN':
                name = "Lincoln's Birthday"
            elif self.state == 'MD' and year >= 2008:
                name = "American Indian Heritage Day"
            elif self.state == 'NV':
                name = "Family Day"
            elif self.state == 'NM':
                name = "Presidents' Day"
            dt = date(year, 11, 1) + rd(weekday=TH(+4))
            self[dt + rd(days=+1)] = name

        # Robert E. Lee's Birthday
        if self.state == 'GA' and year >= 1986:
            if year >= 2016:
                name = "State Holiday"
            else:
                name = "Robert E. Lee's Birthday"
            self[date(year, 11, 29) + rd(weekday=FR(-1))] = name

        # Lady of Camarin Day
        if self.state == 'GU':
            self[date(year, 12, 8)] = "Lady of Camarin Day"

        # Christmas Eve
        if self.state == 'AS' or \
                (self.state in ('KS', 'MI', 'NC') and year >= 2013) or \
                (self.state == 'TX' and year >= 1981) or \
                (self.state == 'WI' and year >= 2012):
            name = "Christmas Eve"
            self[date(year, 12, 24)] = name
            name = name + " (Observed)"
            # If on Friday, observed on Thursday
            if self.observed and date(year, 12, 24).weekday() == 4:
                self[date(year, 12, 24) + rd(days=-1)] = name
            # If on Saturday or Sunday, observed on Friday
            elif self.observed and date(year, 12, 24).weekday() in (5, 6):
                self[date(year, 12, 24) + rd(weekday=FR(-1))] = name

        # Christmas Day
        if year > 1870:
            name = "Christmas Day"
            self[date(year, 12, 25)] = "Christmas Day"
            if self.observed and date(year, 12, 25).weekday() == 5:
                self[date(year, 12, 25) + rd(days=-1)] = name + " (Observed)"
            elif self.observed and date(year, 12, 25).weekday() == 6:
                self[date(year, 12, 25) + rd(days=+1)] = name + " (Observed)"

        # Day After Christmas
        if self.state == 'NC' and year >= 2013:
            name = "Day After Christmas"
            self[date(year, 12, 26)] = name
            name = name + " (Observed)"
            # If on Saturday or Sunday, observed on Monday
            if self.observed and date(year, 12, 26).weekday() in (5, 6):
                self[date(year, 12, 26) + rd(weekday=MO)] = name
            # If on Monday, observed on Tuesday
            elif self.observed and date(year, 12, 26).weekday() == 0:
                self[date(year, 12, 26) + rd(days=+1)] = name
        elif self.state == 'TX' and year >= 1981:
            self[date(year, 12, 26)] = "Day After Christmas"
        elif self.state == 'VI':
            self[date(year, 12, 26)] = "Christmas Second Day"

        # New Year's Eve
        if (self.state in ('KY', 'MI') and year >= 2013) or \
                (self.state == 'WI' and year >= 2012):
            name = "New Year's Eve"
            self[date(year, 12, 31)] = name
            if self.observed and date(year, 12, 31).weekday() == 5:
                self[date(year, 12, 30)] = name + " (Observed)"


class USMarketHoliday(UnitedStates):
    def _populate(self, year):
        self.populating_year = year
        # New Year's Day
        self.gen_new_year_day()
        self.gen_martin_luther_king_day()
        self.gen_washington_birthday()
        self.gen_good_friday()
        self.gen_confederate_memorial_day()
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
        if self.state in ('CT', 'DE', 'GU', 'IN', 'KY', 'LA',
                          'NJ', 'NC', 'PR', 'TN', 'TX', 'VI'):
            self[easter(self.populating_year) + rd(weekday=FR(-1))] = "Good Friday"
    def gen_confederate_memorial_day(self):
        # Confederate Memorial Day
        name = "Confederate Memorial Day"
        if self.state in ('AL', 'GA', 'MS', 'SC') and self.populating_year >= 1866:
            if self.state == 'GA' and self.populating_year >= 2016:
                name = "State Holiday"
            self[date(self.populating_year, 4, 1) + rd(weekday=MO(+4))] = name
        elif self.state == 'TX' and self.populating_year >= 1931:
            self[date(self.populating_year, 1, 19)] = name

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


#print date(2015, 1, 1) in us_holidays
#
#print date(2015, 1, 1) in us_market_holidays

if __name__ == "__main__":
    if len(sys.argv)>1:
        if sys.argv[1]=="--market":
            year = int(sys.argv[2])
            holidays = USMarketHoliday(years= year, state="NY")
        else:
            year = int(sys.argv[1])
            holidays = UnitedStates(years= year, state="NY")
    else:
        raise ValueError("not enough argument")
    import pprint
    pprint.pprint(holidays)
