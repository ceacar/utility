#!/usr/bin/env python
__version__=0.01

import dateutil.parser as parser
import sets
import sys
holidays=[
    "01 Jan 2010",
    "18 Jan 2010",
    "15 Feb 2010",
    "02 Apr 2010",
    "31 May 2010",
    "05 Jul 2010",
    "06 Sep 2010",
    "25 Nov 2010",
    "24 Dec 2010",
    "01 Jan 2009",
    "19 Jan 2009",
    "16 Feb 2009",
    "10 Apr 2009",
    "25 May 2009",
    "03 Jul 2009",
    "07 Sep 2009",
    "26 Nov 2009",
    "25 Dec 2009",
    "01 Jan 2008",
    "21 Jan 2008",
    "18 Feb 2008",
    "21 Mar 2008",
    "26 May 2008",
    "04 Jul 2008",
    "01 Sep 2008",
    "27 Nov 2008",
    "25 Dec 2008",
    "01 Jan 2007",
    "02 Jan 2007",
    "15 Jan 2007",
    "19 Feb 2007",
    "06 Apr 2007",
    "28 May 2007",
    "04 Jul 2007",
    "03 Sep 2007",
    "22 Nov 2007",
    "25 Dec 2007",
    "02 Jan 2006",
    "16 Jan 2006",
    "20 Feb 2006",
    "14 Apr 2006",
    "29 May 2006",
    "04 Jul 2006",
    "04 Sep 2006",
    "23 Nov 2006",
    "25 Dec 2006",
    "17 Jan 2005",
    "21 Feb 2005",
    "25 Mar 2005",
    "30 May 2005",
    "04 Jul 2005",
    "05 Sep 2005",
    "24 Nov 2005",
    "26 Dec 2005",
    "01 Jan 2004",
    "19 Jan 2004",
    "16 Feb 2004",
    "09 Apr 2004",
    "31 May 2004",
    "11 Jun 2004",
    "05 Jul 2004",
    "06 Sep 2004",
    "25 Nov 2004",
    "24 Dec 2004",
    "01 Jan 2003",
    "20 Jan 2003",
    "17 Feb 2003",
    "18 Apr 2003",
    "26 May 2003",
    "04 Jul 2003",
    "01 Sep 2003",
    "27 Nov 2003",
    "25 Dec 2003",
    "01 Jan 2002",
    "21 Jan 2002",
    "18 Feb 2002",
    "29 Mar 2002",
    "27 May 2002",
    "04 Jul 2002",
    "02 Sep 2002",
    "28 Nov 2002",
    "25 Dec 2002",
    "01 Jan 2001",
    "15 Jan 2001",
    "19 Feb 2001",
    "13 Apr 2001",
    "28 May 2001",
    "04 Jul 2001",
    "03 Sep 2001",
    "11 Sep 2001",
    "12 Sep 2001",
    "13 Sep 2001",
    "14 Sep 2001",
    "22 Nov 2001",
    "25 Dec 2001"
]

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

def filter_dates(converted_holidays):
    for date_raw_str in sys.stdin:
        try:
            converted_input_date = parser.parse(date_raw_str).date()
        except:
            converted_input_date = datetime_rescue(date_raw_str)

        if converted_input_date in converted_holidays:
            continue
        else:
            print converted_input_date.strftime("%Y%m%d")

def main():
    converted_holidays = convert_to_date(holidays)
    filter_dates(converted_holidays)

if __name__ == "__main__":
    main()
