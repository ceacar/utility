#!/usr/bin/env python
__version__=0.02
#updated holidays from 2012 -> 2020

import dateutil.parser as parser
import sets
import sys
import generate_holidays
import datetime

#holidays=[
#    "1-Jan-12",
#    "1-Jan-13",
#    "1-Jan-14",
#    "1-Jan-15",
#    "1-Jan-16",
#    "1-Jan-17",
#    "1-Jan-18",
#    "1-Jan-19",
#    "1-Jan-20",
#    "16-Jan-12",
#    "21-Jan-13",
#    "20-Jan-14",
#    "19-Jan-15",
#    "18-Jan-16",
#    "16-Jan-17",
#    "15-Jan-18",
#    "21-Jan-19",
#    "20-Jan-20",
#    "20-Feb-12",
#    "18-Feb-13",
#    "17-Feb-14",
#    "16-Feb-15",
#    "15-Feb-16",
#    "20-Feb-17",
#    "19-Feb-18",
#    "18-Feb-19",
#    "17-Feb-20",
#    "6-Apr-12",
#    "29-Mar-13",
#    "18-Apr-14",
#    "3-Apr-15",
#    "25-Mar-16",
#    "14-Apr-17",
#    "30-Mar-18",
#    "19-Apr-19",
#    "10-Apr-20",
#    "28-May-12",
#    "27-May-13",
#    "26-May-14",
#    "25-May-15",
#    "30-May-16",
#    "29-May-17",
#    "28-May-18",
#    "27-May-19",
#    "25-May-20",
#    "4-Jul-12",
#    "4-Jul-13",
#    "4-Jul-14",
#    "4-Jul-15",
#    "4-Jul-16",
#    "4-Jul-17",
#    "4-Jul-18",
#    "4-Jul-19",
#    "4-Jul-20",
#    "3-Sep-12",
#    "2-Sep-13",
#    "1-Sep-14",
#    "7-Sep-15",
#    "5-Sep-16",
#    "4-Sep-17",
#    "3-Sep-18",
#    "2-Sep-19",
#    "7-Sep-20",
#    "22-Nov-12",
#    "28-Nov-13",
#    "27-Nov-14",
#    "26-Nov-15",
#    "24-Nov-16",
#    "23-Nov-17",
#    "22-Nov-18",
#    "28-Nov-19",
#    "26-Nov-20",
#    "25-Dec-12",
#    "25-Dec-13",
#    "25-Dec-14",
#    "25-Dec-15",
#    "25-Dec-16",
#    "25-Dec-17",
#    "25-Dec-18",
#    "25-Dec-19",
#    "25-Dec-20",
#    "01 Jan 2010",
#    "18 Jan 2010",
#    "15 Feb 2010",
#    "02 Apr 2010",
#    "31 May 2010",
#    "05 Jul 2010",
#    "06 Sep 2010",
#    "25 Nov 2010",
#    "24 Dec 2010",
#    "01 Jan 2009",
#    "19 Jan 2009",
#    "16 Feb 2009",
#    "10 Apr 2009",
#    "25 May 2009",
#    "03 Jul 2009",
#    "07 Sep 2009",
#    "26 Nov 2009",
#    "25 Dec 2009",
#    "01 Jan 2008",
#    "21 Jan 2008",
#    "18 Feb 2008",
#    "21 Mar 2008",
#    "26 May 2008",
#    "04 Jul 2008",
#    "01 Sep 2008",
#    "27 Nov 2008",
#    "25 Dec 2008",
#    "01 Jan 2007",
#    "02 Jan 2007",
#    "15 Jan 2007",
#    "19 Feb 2007",
#    "06 Apr 2007",
#    "28 May 2007",
#    "04 Jul 2007",
#    "03 Sep 2007",
#    "22 Nov 2007",
#    "25 Dec 2007",
#    "02 Jan 2006",
#    "16 Jan 2006",
#    "20 Feb 2006",
#    "14 Apr 2006",
#    "29 May 2006",
#    "04 Jul 2006",
#    "04 Sep 2006",
#    "23 Nov 2006",
#    "25 Dec 2006",
#    "17 Jan 2005",
#    "21 Feb 2005",
#    "25 Mar 2005",
#    "30 May 2005",
#    "04 Jul 2005",
#    "05 Sep 2005",
#    "24 Nov 2005",
#    "26 Dec 2005",
#    "01 Jan 2004",
#    "19 Jan 2004",
#    "16 Feb 2004",
#    "09 Apr 2004",
#    "31 May 2004",
#    "11 Jun 2004",
#    "05 Jul 2004",
#    "06 Sep 2004",
#    "25 Nov 2004",
#    "24 Dec 2004",
#    "01 Jan 2003",
#    "20 Jan 2003",
#    "17 Feb 2003",
#    "18 Apr 2003",
#    "26 May 2003",
#    "04 Jul 2003",
#    "01 Sep 2003",
#    "27 Nov 2003",
#    "25 Dec 2003",
#    "01 Jan 2002",
#    "21 Jan 2002",
#    "18 Feb 2002",
#    "29 Mar 2002",
#    "27 May 2002",
#    "04 Jul 2002",
#    "02 Sep 2002",
#    "28 Nov 2002",
#    "25 Dec 2002",
#    "01 Jan 2001",
#    "15 Jan 2001",
#    "19 Feb 2001",
#    "13 Apr 2001",
#    "28 May 2001",
#    "04 Jul 2001",
#    "03 Sep 2001",
#    "11 Sep 2001",
#    "12 Sep 2001",
#    "13 Sep 2001",
#    "14 Sep 2001",
#    "22 Nov 2001",
#    "25 Dec 2001"
#]


def _gen_holidays(start_year, end_year):
    res = []
    for year in xrange(int(start_year), int(end_year)):
        holidays_date = generate_holidays.NYSEMarketHoliday(years = year, state="NY")
        holidays_str = [ date_object.strftime("%Y%m%d") for date_object in holidays_date]
        #_holidays.extend(generate_holidays.NYSEMarketHoliday(years = year, state="NY"))
        res.extend(holidays_str)
    return sorted(res)

_holidays = _gen_holidays(2003,2025)

def get_holidays(year):
    year = int(year)
    return _gen_holidays(year,year+1)



def convert_to_date(holidays):
    res = []
    for d in holidays:
        #convert to date type
        res.append(parser.parse(d).date())
    return sets.Set(res)

def datetime_rescue(date_input):
    import pandas
    success = False
    converted = None
    try:
        converted = pandas.Timestamp(inp).to_pydatetime().date()
        success = True
    except Exception as e:
        pass
    if success:
        return converted
    else:
        raise ValueError("cannot convert %s"%date_input)

def _filter(date_input, converted_holidays):

    if isinstance(date_input, basestring):
        date_input = date_input.rstrip()
        try:
            converted_input_date = parser.parse(date_input).date()
        except:
            converted_input_date = datetime_rescue(date_input)
    elif isinstance(date_input, datetime.datetime):
        converted_input_date = date_input
    else:
        raise Exception("Error converting {0}".format(date_input))

    converted_input_date = converted_input_date.strftime("%Y%m%d")

    if converted_input_date not in converted_holidays:
        return converted_input_date


def filter_dates(source_input= sys.stdin, converted_holidays = _holidays):
    res = []
    for date_input in source_input:

        valid_date = _filter(date_input, converted_holidays)
        if valid_date:
            res.append(valid_date)
    return res

if __name__ == "__main__":
   res = filter_dates()
   for single_res in res:
        print res
